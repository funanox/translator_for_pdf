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
バグの修正
* リガチャ（ff,ffi）の修正
* チャプター、章番号の表示の修正

課題
* 翻訳の精度
    * 文の整形はできているのにもかかわらず翻訳の精度がイマイチ...。
    おそらくはGoogle翻訳に１度に送る文字数が5000字と限られていることにより文が切れてしまうことにより生じる、
    文全体の文脈の齟齬が原因として考えられます。
    * deepLを利用すればもうすこし自然な翻訳になるかも
        * 参考：deepLのAPIは有料プランで月額630円（テキスト100万字あたり2500円の追加徴収）

(2020/09/17)

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