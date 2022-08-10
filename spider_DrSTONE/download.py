
import requests
from bs4 import BeautifulSoup
import re
from time import localtime
from os import mkdir
from os.path import exists
import asyncio

class Mylogger:
    def __init__(self) -> None:
        pass

    # def inactive(self) -> None:
    #     self.fp.close()

    def log(self, data: str, ifprint = True) -> None:
        if ifprint:
            print(data)

        #换异步后可能报错 log可禁用
        #return None
        with open('DownloadLOG.log', 'a+') as f:
            f.write(f'==> {str(localtime()[ : 6])} | {data}\n')

class Downloader:

    #DrSTONE_ADDR = 25638 - 1
    DrSTONE_ADDR = 239049 - 1

    # 页码长度
    PAGE_NUMBER_LENGTH = 2

    # 章节长度
    CAPTURE_NUMBER_LENGTH = 3

    # 起始，截至章节
    CAPTURE_START, CAPTURE_END = 233, 233

    # 基础漫画地址
    BASE_URL = r'https://omyschool.com/article_detail/152/{addr}/Dr.STONE%20%E7%9F%B3%E7%BA%AA%E5%85%83/{cap}%E8%A9%B1/'

    # 请求头信息
    MY_HEADERS = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47', 

    }

    # 保存路径
    PATH = './out/'

    def __init__(self) -> None:
        self.logger = Mylogger()
        if not exists(Downloader.PATH):
            mkdir(Downloader.PATH)

    def prefix_zero(self, ss: str, leng: int) -> str:
        '''为字符串ss填充前导0使其达到长度leng'''
        ss = str(ss)
        if len(ss) < leng:
            ss = '0' * (leng - len(ss))  + ss
        return ss

    def format_page_number(self, page: str) -> None:
        '''
        把页码前面补0扩展到正确长度
        page: 页码字符串
        '''
        return self.prefix_zero(page, Downloader.PAGE_NUMBER_LENGTH)

    def format_capture_number(self, cap: str) -> None:
        '''
        把章节前面补0扩展到正确长度
        cap: 章节码字符串
        '''
        return self.prefix_zero(cap, Downloader.CAPTURE_NUMBER_LENGTH)

    def form_capture_url(self, capture: int) -> str:
        '''
        返回第capture章的网页地址
        capture: 章序号
        '''
        str_capture = str(capture)
        str_addr = str(Downloader.DrSTONE_ADDR + capture)
        if capture < 10: str_capture = '0' + str_capture
        return Downloader.BASE_URL.format(cap = str_capture, addr = str_addr)

    async def download_one_picture(self, url: str, filepath: str, filename: str) -> None:
        '''
        下载一张图片
        url: 图片地址
        filepath: 文件路径, 以"/"结尾
        filenamer: 文件名
        page: 页码号 用于显示进度
        '''
        try:
            #print(url)
            fileformat = url.split('.')[-1]
            res = requests.get(url, headers=Downloader.MY_HEADERS)
            with open(f'{filepath}{filename}.{fileformat}', 'wb') as f:
                f.write(res.content)
            print(f'{filepath}{filename}.{fileformat}完成...')
        except Exception as e:
            self.logger.log(f'{type(e)} | {str(e)} | 下载图片{filepath}{filename}时出错。')

    def parse_one_capture(self, capture_number: int) -> list[tuple[str, str]]:
        '''
        解析第capture_number章的内容, 返回这一章所有图片的链接和序号
        capture_number: 章序号
        '''
        try:
            #url = self.form_capture_url(capture_number)
            url = self.NEW__form_capture_url(capture_number)
            print(url)
            res = requests.get(url, headers=Downloader.MY_HEADERS)
            soup = BeautifulSoup(res.text.replace('amp-img', 'amp_img'))
            data_list = soup.find_all('div', {'data-id': True})
            image_list = []
            for each in data_list:
                picture_url = each.amp_img['src']
                picture_id = re.search('第([0-9]+)页', each.amp_img['alt']).group(1)
                image_list.append((picture_url, picture_id))
            return image_list
        except Exception as e:
            self.logger.log(f'{type(e)} | {str(e)} | 解析第{capture_number}章链接时出错，可能部分或全部图片未正确下载。')
            return []

    def run(self):
        '''主方法'''

        self.link_dict = self.NEW_get_random_capture_url()


        #try:
        print('开始下载...')
        for capture in range(Downloader.CAPTURE_START, Downloader.CAPTURE_END + 1):
            print(f'章进度:{capture - Downloader.CAPTURE_START + 1} / {Downloader.CAPTURE_END + 1 - Downloader.CAPTURE_START}')
            path = f'{Downloader.PATH}capture{self.format_capture_number(capture)}/'
            if not exists(path):
                mkdir(path)
            image_list = self.parse_one_capture(capture)
            if not image_list: continue
            tasks = []
            for picture_url, picture_id in image_list:
                tasks.append(asyncio.ensure_future(
                    self.download_one_picture(
                    picture_url, 
                    path,
                    'page' + self.format_page_number(picture_id)
                    )
                ))
            loop = asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))
        print('下载结束...')
        # except Exception as e:
        #     self.logger.log(f'{type(e)} | {str(e)} | run方法遇到未知错误')



    #def NEW__get_random_capture_url() -> list[tuple[str, str]]:
    def NEW_get_random_capture_url(self) -> dict[int, str]:
        '''获取Mr.STONE所有章节的链接'''
        print('获取章节目录开始...')
        DOMIN = 'https://omyschool.com'
        DrSTONE_url = r'https://omyschool.com/article_list/152/Dr.STONE%20%E7%9F%B3%E7%BA%AA%E5%85%83/'
        res = requests.get(DrSTONE_url, headers=Downloader.MY_HEADERS)
        soup = BeautifulSoup(res.text)
        lst = soup.findAll('div', {"class": "chapter"})
        #ret = []
        ret_d = {}
        for each in lst:
            href = each.a["href"]
            if 'Dr.STONE' in href:
                id = re.search('([0-9]+)[话|話]', str(each)).group(1)
        #         ret.append((DOMIN + href, id))
        # return sorted(ret, key = lambda x: int(x[1]))
                ret_d[int(id)] = DOMIN + href
        print('获取章节目录完成...')
        return ret_d

    def NEW__form_capture_url(self, capture: int) -> str:
        '''
        返回第capture章的网页地址
        capture: 章序号
        '''
        return self.link_dict[capture]




if __name__ == '__main__':
    d = Downloader()
    d.run()
