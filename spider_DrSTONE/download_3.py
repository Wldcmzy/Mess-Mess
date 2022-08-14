from base64 import urlsafe_b64decode
import requests
import re
import bs4
import time
import os
import typing

class Easylogger:
    def __init__(self, path: str = './', filename = 'DownloadLOG.log') -> None:
        self.path = path
        self.filename = filename
        self.makelog('MyEasylogger类被实例化', 'MyEasylogger', False)

    def makelog(self, data: str, tag: str = 'default', ifprint: bool = True) -> None:
        if ifprint:
            print(data)
        ifexist = os.path.exists(self.filename)
        with open(self.path + self.filename, 'a+') as f:
            if not ifexist:
                f.write(f'==> {str(time.localtime()[ : 6])} | [MyEasylogger] 日志建立\n')
            f.write(f'==> {str(time.localtime()[ : 6])} | [{tag}] {data}\n')

    def log(self, data: str, ifprint = True):
        self.makelog(data, 'log', ifprint)

    def debug(self, data: str, ifprint = True):
        self.makelog(data, 'debug', ifprint)

    def error(self, data: str, ifprint = True):
        self.makelog(data, 'error', ifprint)
logger = Easylogger()

def try_except_ensure(func):
    def _(*args):
        try:
            return func(*args)
        except Exception as e:
            def __(e : Exception, *args) -> None: 
                logger.error(str(type(e)) + '|' + str(e))
            return __(e, *args)
    return _

class Downloader:
    DOMIN = 'http://rimanb.com/'

    HTML = '''
<!DOCTYPE html>
<html>
<head>
	<title>{capture}</title>
	<meta charset="utf-8">
    <style>
        body{{
            background-color: black;
        }}
		div#pages{{
            text-align: center;
		}}
        p#p{{
            font-size: 35px;
            text-align: center;
            color: #66ffff;
        }}
        span#capture_number{{
            color: #ff66ff;
        }}
	</style>
    
</head>
<body>
{args}
</body>
</html>
'''
    IMAGE = '    <div id="pages"><img onload="if(this.width >= document.documentElement.clientWidth){{this.width = document.documentElement.clientWidth}}" align="middle" src="{page}"></img></div>\n'
    P = '   <p id="p"><strong>{caricature_name} 第 <span id="capture_number">{p}</span> 话</strong></p>\n'
    SEP = '    <br><br>\n    <hr style="FILTER:alpha(opacity=100,finishopacity=0,style=3)" width="95%"color=#00FF7F SIZE=5>'
    def __init__(
        self,
        catalog_url: str = 'http://rimanb.com/book/2407',
        start_end: tuple[int, int] = (0, -1),
        image_format: str = '.jpg',
        outpath_root: str = './out/',
        htmlpath: str = './html/',
        caricature_name: str = 'Dr.STONE石纪元',
        page_number_length:int = 2,
        capture_number_length: int = 3,
        headers: dict = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47', 
        }, 
    ) -> None:
        '''
        catalog_url:
            漫画的章节列表页面url
        start_end:
            爬取漫画的起始和终止章节
        image_format:
            图片保存格式
        outpath_root:
            输出根路径, 以/结尾
        htmlpath:
            以便于观看的html文件整合图片,html文件的输出路径
        caricature_name:
            漫画名称, 用于html要素命名
        page_number_length:
            命名图片序号所需的字符串长度
        capture_number_length:
            命名章节序号所需的字符串长度
        headers:
            请求头信息
        '''
        self.start, self.end = start_end
        self.catalog_url = catalog_url
        self.image_format = image_format
        self.outpath_root = outpath_root
        self.htmlpath = htmlpath
        self.caricature_name = caricature_name
        self.page_number_length = page_number_length
        self.capture_number_length = capture_number_length
        self.headers = headers
        if not os.path.exists(self.outpath_root):
            os.mkdir(self.outpath_root)
            logger.debug(f'输出目录{self.outpath_root}不存在, 已经成功建立...')

    def prefix_zero(self, ss: typing.Union[str, int], leng: int) -> str:
        '''
        为字符串ss填充前导0使其达到长度leng
        ss:
            初始字符串
        leng:
            目标长度
        '''
        ss = str(ss)
        assert len(ss) <= leng
        if len(ss) < leng:
            ss = '0' * (leng - len(ss))  + ss
        return ss

    def format_page_number(self, page: str) -> None:
        '''
        把页码前面补0扩展到正确长度
        page: 
            页码字符串
        '''
        return self.prefix_zero(page, self.page_number_length)

    def format_capture_number(self, cap: str) -> None:
        '''
        把章节前面补0扩展到正确长度
        cap: 
            章节码字符串
        '''
        return self.prefix_zero(cap, self.capture_number_length)

    def get_url_dict(self) -> dict[int, str]:
        '''
        获得漫画每一章的url
        return: dic
            漫画的所有章节的章节号-url映射表
            {章节号 : url}
        '''
        res = requests.get(self.catalog_url, headers = self.headers)
        soup = bs4.BeautifulSoup(res.text)
        lst = soup.findAll('span', class_ = 'works-chapter-item')
        dic = {}
        for each in lst:
            id = re.search('第([0-9]+)话', str(each.a['title'])).group(1)
            href = each.a['href']
            dic[int(id)] = Downloader.DOMIN +  href
        return dic

    def parse_capture(self, url: str) -> list[tuple[int, str]]:
        '''
        获取漫画特定章节的所有图片的链接
        url: 
            漫画特定章节的url
        return: lst
            url对应漫画章节的所有图片链接
            [(图片序号, url), ]
        '''
        res = requests.get(url, headers = self.headers)
        soup = bs4.BeautifulSoup(res.text)
        imgs = soup.find('ul', id = 'comicContain', class_ = 'comic-contain').findAll('li')
        lst = []
        for i, each in enumerate(imgs):
            lst.append((i + 1, Downloader.DOMIN + each.img['src']))
        return lst

    def download_one_picture(self, url: str, filepath: str, filename: str) -> None:
        '''
        下载一张图片
        url: 
            图片地址
        filepath: 
            文件路径, 以"/"结尾
        filename: 
            文件名
        '''
        res = requests.get(url, headers = self.headers)
        with open(f'{filepath}{filename}.{self.image_format}', 'wb') as f:
            f.write(res.content)
        logger.log(f'下载图片并保存为{filepath}{filename}.{self.image_format}完成...')

    @try_except_ensure
    def run(self) -> None:
        '''
        下载图片
        下载的漫画链接为: self.catalog_url
        下载的起始章节为: self.start
        下载的结束章节为: self.end
        下载的图片保存为: self.outpath_root/capture章节号/page图片号.self.imageformat
        '''
        logger.log(f'开始下载,漫画目录s链接为:{self.catalog_url}')
        logger.log('正在获取章节目录...')
        self.url_dict = self.get_url_dict()
        logger.log(f'章节目录获取完成,共{len(self.url_dict)}个项目...')
        for capture in range(self.start, self.end + 1):
            logger.log(f'!!!章节进度: {capture}({self.start}-{self.end}) ({capture - self.start + 1}/{self.end - self.start + 1})')
            outpath = f'{self.outpath_root}capture{self.format_capture_number(capture)}/'
            if not os.path.exists(outpath):
                logger.debug(f'创建目录{outpath}')
                os.mkdir(outpath)
            if capture not in self.url_dict:
                logger.error(f'在章节目录中没有第{capture}章的记录(KeyError:{capture})')
                continue
            image_list = self.parse_capture(self.url_dict[capture])
            for pid, purl in image_list:
                logger.log(f'!图片进度: ({pid}/{len(image_list)})')
                self.download_one_picture(purl, outpath,'page' + self.format_page_number(pid))
        logger.log('下载结束...')

    def combie_one_caputre_images_to_html(self, folder_name: int) -> str:
        '''
        把一整章的图片链接都整合为html语言图片块
        folder_name:
            特定章节对应的文件夹名
        return: html
            拥有folder_name文件夹中所有以page链接的html文件格式字符串
        '''
        pages = [each for each in os.listdir(self.outpath_root + folder_name) if each[ : 4] == 'page']
        pages = sorted(pages)
        html = ''
        image_src = '../' + self.outpath_root + folder_name + '/'
        for each in pages:
            html += Downloader.IMAGE.format(page = image_src + each)
        return html
    
    def create_one_html(self, name: str, html: str, collection: bool = False) -> None:
        '''
        生成一章漫画的html文件
        name:
            要生成的html文件名称
        html:
            本章漫画图片的html格式字符串
        collection:
            本次是否生成总集
        '''
        index = f'第{int(name[7 : ])}话' if not collection else '总集篇'
        with open(self.htmlpath + self.caricature_name + '_' + name + '.html', 'w', encoding='utf-8') as f:
            f.write(Downloader.HTML.format(capture = f'{self.caricature_name} {index}', args = html))
    
    def create_htmls(self, collection: bool = True) -> None:
        '''
        为漫画所有章节生成html文件
        collection:
            是否生成总集篇文件
        '''
        if not os.path.exists(self.htmlpath):
            os.mkdir(self.htmlpath)
            logger.debug(f'{self.htmlpath}不存在, 建立成功')
        logger.log(f'开始为漫画创建html文件, {"" if collection else "不"}包括创建总集篇')
        capture_folders = [each for each in os.listdir(self.outpath_root) if each[ : 7] == 'capture']
        totalhtml = ''
        for each in capture_folders:
            html = Downloader.SEP
            html += Downloader.P.format(p = int(each[7 : ]), caricature_name = self.caricature_name)
            html += self.combie_one_caputre_images_to_html(each)
            self.create_one_html(each, html)
            logger.log(each + 'html创建完成...')
            if collection:
                totalhtml += html
        if collection:
            self.create_one_html('ALL CAPTURES', totalhtml, True)
            logger.log('总集篇html创建完成...')


if __name__ == '__main__':
    d = Downloader()
    d.run()
    #d.create_htmls()

