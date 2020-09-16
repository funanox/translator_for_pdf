import os
import random
import time

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

base_url = "https://www.cl.cam.ac.uk/~rja14/"
extension = ".pdf"
path = "./anderson/"

# スクレイピング先URL (*.pdf)
url = "https://www.cl.cam.ac.uk/~rja14/book.html"


def get_download_urls(url):
    download_urls = []

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    links = soup.findAll('a')

    # URLの抽出
    for link in links:
        href = link.get('href')
        if extension and "SEv3-ch" in href:
            download_urls.append(href)
        if extension and "SEv3-pref" in href:
            download_urls.append(href)

    return download_urls


def download(download_url):
    if os.path.isfile(path + download_url.split("/")[-1]):
        return None

    r = requests.get(base_url + download_url)
    # 適当な時間スリープ
    time.sleep(random.random())
    return r.content


def create_filepath(url):
    return path + url.split("/")[-1]


def save_pdf(filename, pdf):
    with open(filename, "wb") as f:
        f.write(pdf)


if __name__ == '__main__':
    if not os.path.isdir(path):
        os.mkdir(path)

    download_urls = get_download_urls(url)
    pbar = tqdm(download_urls)
    for download_url in pbar:
        pbar.set_description("Downloading {} ".format(download_url.split("/")[-1]))
        pdf = download(download_url)
        if pdf is not None:
            filename = create_filepath(download_url)
            save_pdf(filename, pdf)
            time.sleep(random.random())
