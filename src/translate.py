import glob
import os
import re
import shutil
import time

import fitz
from docx import Document
from googletrans import Translator
from tqdm import tqdm

input_path = os.path.join(os.path.dirname(__file__), "../anderson/")
output_path = os.path.join(os.path.dirname(__file__), "../anderson-ja/")
temp = os.path.join(os.path.dirname(__file__), "../temp/")


def remove_temp(temp, debug=False):
    if debug:
        return
    shutil.rmtree(temp)


def get_filename(pdf_path):
    return os.path.splitext(os.path.basename(pdf_path))[0]


def get_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.getText()
    return text


def write_text(text_path, text):
    with open(text_path, "w", encoding="utf-8") as txt:
        txt.write(text)


def convert_text(text_path, convert_path):
    # ヘッダー
    def is_header(line):
        line = line.replace("\n", "")
        if line == "Preface to the Third Edition":
            return True
        if re.fullmatch("\d{1,2}\.\d+\.(\s|[A-Z]|\?|-)+", line) is not None:
            return True
        return False

    # フッター
    def is_footer(line):
        line = line.replace("\n", "")
        for footer in ['Security Engineering', 'Ross Anderson']:
            if line == footer:
                return True
        if line.isdecimal():
            return True
        return False

    # 章番号
    def is_title(line):
        line = line.replace("\n", "")
        if line == "Preface to the Third Edition":
            return True
        if re.fullmatch("\d{1,2}(\.\d)+", line) is not None:
            return True
        return False

    def convert_title(title_number, title_name):
        text = "\n" + title_number.replace("\n", " ") + title_name
        return text

    # チャプター
    def is_chapter(line):
        line = line.replace("\n", "")
        if re.fullmatch("^Chapter\s\d{1,2}", line) is not None:
            return True
        return False

    def convert_chapter(chapter_number, chapter_name):
        text = chapter_number.replace("\n", " ") + chapter_name
        return text

    # 偉人の名言
    def is_wise_saying(line):
        line = line.replace("\n", "")
        if re.fullmatch("^–\s(\s|[A-Z]|\[|\]|[0-9])+", line) is not None:
            return True
        return False

    def convert_line(line):
        # リガチャの処理
        def remove_ligature(line):
            text = line.replace(u"\ufffd", u"\u0066\u0066\u0069").replace(u"\u21B5", u"\u0066\u0066")
            return text

        line = remove_ligature(line)

        text = line.replace("\n", " ")
        text = text.replace("fig.", "fig").replace("Fig.", "Fig")
        text = text.replace(". ", ". \n").replace(")", ")\n").replace("?", "?\n")
        for i in range(1, 7):
            text = text.replace(" " * i, " ")

        return text

    title_next = False
    chapter_next = False

    with open(text_path, "r", encoding="utf-8") as txt:
        with open(convert_path, "w", encoding="utf-8") as convert_txt:
            for line in txt:
                # ヘッダーとフッターの除去
                if is_header(line) or is_footer(line):
                    continue

                # チャプター
                if is_chapter(line):
                    chapter_next = True
                    chapter_number = line
                    continue
                # タイトル
                if is_title(line):
                    title_next = True
                    title_number = line
                    continue
                # タイトルの次の要素を章番号と結合
                if title_next:
                    text = convert_title(title_number, line)
                    title_next = False
                elif chapter_next:
                    text = convert_chapter(chapter_number, line)
                    chapter_next = False
                # 偉人の名言
                elif is_wise_saying(line):
                    text = line + "\n"
                # 本文
                else:
                    text = convert_line(line)
                convert_txt.write(text)


def translate_google(text_path):
    trans_text = ""
    translated_text = ""
    with open(text_path, "r", encoding="utf-8") as convert_text:
        for line in convert_text:
            trans_text += convert_text.readline()
            if len(trans_text) >= 4000:
                translated_text += Translator().translate(trans_text, dest="ja").text
                trans_text = ""
                time.sleep(3)
        translated_text += Translator().translate(trans_text, dest="ja").text
    return translated_text


def save_word(translated_text, filename):
    doc = Document()
    doc.add_paragraph(translated_text)
    doc.save(output_path + filename + "_ja.docx")


if __name__ == '__main__':
    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    if not os.path.isdir(temp):
        os.mkdir(temp)

    pdf_paths = glob.glob(input_path + "*.pdf")
    pbar = tqdm(pdf_paths)
    for pdf_path in pbar:
        filename = get_filename(pdf_path)
        text_path = temp + filename + "_pdf_text.txt"
        convert_path = temp + filename + "_convert_text.txt"
        pbar.set_description("Translating {} ".format(filename))

        # PDFファイルからテキストを抽出
        text = get_text_from_pdf(pdf_path)
        # 抽出したテキストをtxtファイルに書き込み
        write_text(text_path, text)
        # 整形
        convert_text(text_path, convert_path)
        # 翻訳（Google翻訳を利用）
        translated_text = translate_google(convert_path)
        # Wordに出力
        save_word(translated_text, filename)

    # 最後にtempを消去（デバック時は消さない)
    remove_temp(temp, debug=True)
