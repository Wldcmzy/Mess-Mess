import requests
import bs4
import os


BASEURL = 'https://www.didiaomh.com/chapter/{num}?page={p}'
NUM1 = 121018
FOLDER = 'reboot_out/'

def downone(url, path: str) -> None:
    res = requests.get(url)
    with open(path, 'wb') as f:
        f.write(res.content)
    print(path)

def parse_url(url) -> list:
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text)
    lst = soup.findAll('img', class_ = 'comicimg')
    lst = [each['src'] for each in lst]
    return lst

def run():
    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)
    for i in range(9):
        cnt = 0
        cpath = f'{FOLDER}capture{i + 1}/'
        if not os.path.exists(cpath):
            os.mkdir(cpath)
        mid_url = BASEURL.format(num = NUM1 + i, p = '{p}')
        for j in range(1, 4):
            url = mid_url.format(p = j)
            lst = parse_url(url)
            for each in lst:
                cnt += 1
                page = str(cnt)
                if len(page) <= 1:
                    page = '0' + page
                downone(each, cpath + 'page' + page + '.jpg')

#run()

from download_3 import Downloader

d = Downloader(
    outpath_root = './reboot_out/',
    htmlpath = './reboot_html/',
    caricature_name= 'Dr.STONE石纪元 外传 Reboot-白夜',
)
d.create_htmls()
