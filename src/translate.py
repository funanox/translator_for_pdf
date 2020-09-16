import glob
import os
import shutil
import time

import fitz
from docx import Document
from googletrans import Translator
from tqdm import tqdm

input_path = "../anderson/"
output_path = "../anderson-ja/"
temp = "../temp/"


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
    emp = " "
    with open(text_path, "r", encoding="utf-8") as txt:
        with open(convert_path, "w", encoding="utf-8") as convert_txt:
            for line in txt:
                txt = line.replace("\n", "")
                txt = txt.replace("fig.", "fig").replace("Fig.", "Fig")
                txt = txt.replace(".", ".\n")
                for i in range(1, 7):
                    txt = txt.replace(emp * i, " ")
                convert_txt.write(txt)


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
