from bs4 import BeautifulSoup
import re
from Wrappers import logger, remove_invalid_element_in_windows_path, try_except_ensure
from Wrappers.Affix import Affix_OnlyZeroExample
from Wrappers.HTMLwrapper import Image_HTMLwrapper_Lv2
import os
import aiohttp
import asyncio


class SpiderX:
    DOMIN: str = 'https://www.didiaomh.com/'

    def __init__(
        self,
        catalog_url: str,
        outpath_name: str = 'out',
        capture_format: str = 'capture{arg}',
        image_format: str = 'image{arg}.jpg',
        max_capture_number_length: int = 3,
        max_page_number_length: int = 3,
        work_span: tuple[int] = (0, -1),
        concurrency: int = 5,
        myproxy = None,
        # headers: dict = {},
    ) -> None:
        '''
        catalog_url:
            目录页链接
        outpath_name:
            输出路径名
        capture_format:
            章节格式
        image_format:
            图片格式
        max_capture_number_length: 
            最大章节序号长度
        max_page_number_length:
            最大图片序号长度
        work_span: tuple[int]:
            爬取章节范围(小, 大)
            默认爬取所有
        concurrency:
            同时进行的任务数量
        proxies:
            代理服务器信息
        '''
        self.catalog_url = catalog_url if catalog_url[ : len(self.DOMIN)] == self.DOMIN else self.DOMIN + catalog_url
        self.outpath_name = outpath_name
        self.check_path(self.outpath_name)
        self.capture_format = capture_format
        self.image_format = image_format
        self.max_capture_number_length = max_capture_number_length
        self.max_page_number_length = max_page_number_length
        self.work_span = work_span
        self.myproxy = myproxy

        self.page_counter = 0
        self.affix = Affix_OnlyZeroExample()

        self.semaphore = asyncio.Semaphore(concurrency)
        self.session = aiohttp.ClientSession()


    def toreload_format_page_name(self, index: int):
        return self.image_format.format(arg = self.affix.add_prefix(str(index), self.max_page_number_length))
    def toreload_format_capture_name(self, index: int, capture_title: str):
        return self.capture_format.format(arg = self.affix.add_prefix(str(index), self.max_page_number_length) + capture_title)

    def check_path(self, path: str) -> None:
        '''检查目录存在性,若目录没有, 则创建'''
        if not os.path.exists(path):
            os.mkdir(path)
            logger.debug(f'建立目录:{path}...')

    async def get_html(self, url: str) -> str:
        '''抓取网页html信息'''
        async with self.semaphore:
            async with self.session.get(url, proxy = self.myproxy) as response:
                return await response.text()

    async def get_catalog(self) -> dict[int, tuple[str, str]]:
        '''
        生成漫画目录 (章节-url 映射)
        return: 
            { index : (url, capture_title), }
        '''
        html = await self.get_html(self.catalog_url)
        soup = BeautifulSoup(html) 
        li_tag_list: list[BeautifulSoup] = soup.find('ul', class_ = 'chapter-list clearfix').findAll('li')
        catalog = {}
        for i, each in enumerate(li_tag_list):
            catalog[i + 1] = self.DOMIN + each.a['href'], each.a.string 
        return catalog

    async def save_image(self, pathname: str, data: bytes) -> None:
        '''保存一张图片'''
        with open(pathname, 'wb') as f:
            f.write(data)

    async def download_one_image(self, url: str, pathname: str) -> None:
        '''下载一张图片'''
        async with self.session.get(url) as res:
            await self.save_image(pathname, await res.read())

    async def download_one_capture_perpage(self, soup: BeautifulSoup, foldername: str) -> None:
        '''下载一html页的图片'''
        li_tag_list: list[BeautifulSoup] = soup.find('div', class_ = 'comiclist').findAll('div', class_ = 'comicpage')
        tasks = []
        for each in li_tag_list:
            url: str = each.img['src']
            self.page_counter += 1
            filename = remove_invalid_element_in_windows_path(self.toreload_format_page_name(self.page_counter))
            tasks.append(asyncio.ensure_future(self.download_one_image(url, f'{self.outpath_name}/{foldername}/{filename}')))
        await asyncio.wait(tasks)
    
    async def download_one_capture(self, url: str, foldername: str) -> None:
        '''下载一章图片'''
        self.check_path(f'{self.outpath_name}/{foldername}')
        self.page_counter = 0
        html = await self.get_html(url)
        soup = BeautifulSoup(html)
        total_pages = int(re.search('第[0-9]+/([0-9]+)页', soup.find('select', class_ = 'selectpage').option.string).group(1))
        logger.log('html page 1')
        await self.download_one_capture_perpage(soup, foldername)
        for i in range(2, total_pages + 1):
            logger.log(f'html page {i}')
            html = await self.get_html(url.replace('.html', f'?page={i}'))
            soup = BeautifulSoup(html)
            await self.download_one_capture_perpage(soup, foldername)

    async def download_all_caputres(self) -> None:
        '''下载漫画所有图片'''
        catalog = await self.get_catalog()
        work_span_low, work_span_high = self.work_span
        flag = work_span_high >= work_span_low
        logger.debug(f'work span flag:{flag}, low:{work_span_low}, high:{work_span_high}')
        if flag:
            catalog = dict(filter(lambda x: x[0] >= work_span_low and x[0] <= work_span_high, catalog.items()))
        for key, value in catalog.items():
            logger.log(f'章节进度:{key}/{len(catalog)}')
            url, capture_title = value
            capture_name = remove_invalid_element_in_windows_path(self.toreload_format_capture_name(key, capture_title))
            await self.download_one_capture(url, capture_name)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    x = SpiderX(
        'https://www.didiaomh.com/manhua/6500.html',
        outpath_name = '偷星九月天IMAGES',
        # work_span=(1, 1),
    )
    
    try:
        loop.run_until_complete(x.download_all_caputres())
    except Exception as e:
        logger.error(f'{type(e)}|{str(e)}')
    finally:
        loop.close()

#===========================================================================

    class TX9MOONSKY(Image_HTMLwrapper_Lv2):
        def __init__(
            self, 
            root: str,
            html_path: str,
            html_vital_element: str,
            html_collection_name,
            prefix_LvRoot: str, 
            prefix_Lv2: str,
        ) -> None:
            super().__init__(
                root, 
                html_path, 
                html_vital_element, 
                html_collection_name,
                prefix_LvRoot,
                prefix_Lv2
            )
        
        def toreload_parse_diff_element_title(self, folder_name: str) -> str:
            return super().toreload_parse_diff_element_title(folder_name)
        
        def toreload_parse_diff_element_P(self, folder_name: str) -> str:
            return super().toreload_parse_diff_element_P(folder_name)[3 : ]


    y = TX9MOONSKY(
        root = '偷星九月天IMAGES',
        html_path = '偷星九月天HTMLS',
        html_vital_element= '偷星九月天 {arg}',
        html_collection_name= ' 偷星九月天 全集 ',
        prefix_LvRoot='capture',
        prefix_Lv2='image'
    )
    y.create_htmls()