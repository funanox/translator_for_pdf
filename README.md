# translator_for_pdf
英語のpdfを日本語のwordに変換して出力するアプリ
 
# About
"translator_for_pdf"の実行ステップ

1. PDFをダウンロード (anderson/)
2. PDFからテキストを抽出
3. テキストの整形(temp/)
4. テキストのGoogle翻訳
5. Word(.docx)形式への出力(anderson-ja/)

各実行ステップとプログラムの関係

* 1 - download.py
* 2,3,4,5 - translate.py
 
# Requirement
実行時の環境
* python 3.6.9
* python3-venv
* pip 20.2.3

# Installation
```bash
git clone https://github.com/funanox/translator_for_pdf
cd translator_for_pdf

python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt 
```

# Usage
```bash
# Downloading pdf data from https://www.cl.cam.ac.uk/~rja14/book.html
python3 src/download.py
# Translate pdf file
python3 src/translate.py
```
# Note
開発途中なので無料で利用可能なGoogle翻訳を利用しています。
（どうせならdeepLを使いたいのですがAPIが有料なので断念...）
まだ、文字列の整形がうまく行っていないのでそれに付随する形で翻訳もいまいちです。
アドバイスいただけると嬉しいです！

(2020/09/16)
 
# Author
* funanox
* Waseda University
 
# License 
This software is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).