import glob
import os
import re

from docx import Document
from docx.shared import Pt

word_path = os.path.join(os.path.dirname(__file__), "../pdf2docx/")
output_path = os.path.join(os.path.dirname(__file__), "../anderson-word-EN/")


def get_filename(pdf_path):
    return os.path.splitext(os.path.basename(pdf_path))[0]


def modify_doc(document):
    # チャプター
    def is_chapter(text):
        # チャプター数
        if text.font.size == Pt(20.5):
            return True
        # チャプタータイトル
        if text.font.size == Pt(24.5):
            return True
        return False

    # 章番号
    def is_title(inline):
        text = ""
        for i in range(len(inline)):
            text += inline[i].text
        text = text.replace("\n", "")
        if re.search("^\d{1,2}(\.\d)+(\s|\t)+", text) is not None:
            return True
        return False

    # リガチャ
    ligatures = {u"\ufb03": u"\u0066\u0066\u0069", u"\u21b5": u"\u0066\u0066", u"\u270f": u"\u0066\u0066\u006c", u"\ufb01": u"\u0066\u0069"}

    def remove_ligature(text):
        for key in ligatures.keys():
            if key in text:
                text = text.replace(key, ligatures[key])
        if "o ces" in text:
            text = text.replace("o ces", "offices")
        if "O ce365" in text:
            text = text.replace("O ce365", "Office365")
        return text

    # 改行
    def remove_lf(text):
        if "- " in text:
            text = text.replace("- ","")
        return text

    for paragraph in document.paragraphs:
        # 各パラグラフのインライン処理
        inline = paragraph.runs

        # 章番号
        if is_title(inline):
            for i in range(len(inline)):
                inline[i].bold = True
            continue

        for i in range(len(inline)):
            text = inline[i].text
            # チャプター・章番号の検知
            if is_chapter(inline[i]):
                inline[i].bold = True
                continue
            # リガチャの削除
            text = remove_ligature(text)
            # 改行の削除
            text = remove_lf(text)
            inline[i].text = text

    return document


if __name__ == '__main__':
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    # PDFからWordへの変換
    # URL : https://document.online-convert.com/convert/pdf-to-docx
    # pdf2docx/に保存済み

    # Wordファイルの整形
    word_files = glob.glob(word_path + "*.docx")
    for word_file in word_files:
        filename = get_filename(word_file)
        print(filename)
        document = Document(word_file)
        document = modify_doc(document)
        docx_path = output_path + filename + ".docx"
        document.save(docx_path)
