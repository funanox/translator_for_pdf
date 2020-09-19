import glob
import os

from docx import Document
from pdf2docx import parse

input_path = os.path.join(os.path.dirname(__file__), "../anderson/")
temp_path = os.path.join(os.path.dirname(__file__), "../temp/")
output_path = os.path.join(os.path.dirname(__file__), "../anderson-word-EN/")


def get_filename(pdf_path):
    return os.path.splitext(os.path.basename(pdf_path))[0]


def modify_doc(document):
    dic = {u"\ufffd": u"\u0066\u0066\u0069", u"\u21B5": u"\u0066\u0066", u"\u270f": u"\u0066\u0066\u006c"}
    for paragraph in document.paragraphs:
        inline = paragraph.runs
        for i in range(len(inline)):
            text = inline[i].text
            for ch in text:
                for key in dic.keys():
                    if ch == key:
                        text = text.replace(ch, dic[key])
            inline[i].text = text
    return document


if __name__ == '__main__':
    if not os.path.isdir(output_path):
        os.mkdir(output_path)

    # PDFをWordに変換
    pdf_paths = glob.glob(input_path + "*.pdf")
    for pdf_path in pdf_paths:
        filename = get_filename(pdf_path)
        if filename == "SEv3-ch5-7sep":
            continue
        docx_temp_path = temp_path + filename + "_before_" + ".docx"
        if os.path.isfile(docx_temp_path):
            print('{} : Already PDF2WORD !!'.format(filename))
            continue
        # convert pdf to docx
        parse(pdf_path, docx_temp_path)

    # Wordファイルのリガチャの修正
    word_paths = glob.glob(temp_path + "*.docx")
    for word_path in word_paths:
        filename = get_filename(word_path).replace("_before_", "")
        document = Document(word_path)
        document = modify_doc(document)
        docx_path = output_path + filename + ".docx"
        document.save(docx_path)
