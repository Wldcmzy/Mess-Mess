import requests
from bs4 import BeautifulSoup
import re
from Wrappers import logger, remove_invalid_element_in_windows_path, try_except_ensure
from Wrappers.Affix import Affix_OnlyZeroExample
from Wrappers.HTMLwrapper import Image_HTMLwrapper_Lv2
import os


class SpiderX:
    DOMIN: str = 'https://www.didiaomh.com/'

    def __init__(
        self,
        catalog_url: str,
        outpath_name: str = 'out',
        capture_format: str = 'capture{arg}',
        image_format:str = 'image{arg}.jpg',
        max_capture_number_length: int = 3,
        max_page_number_length: int = 3,
        work_span: tuple[int] = (0, 0),
    ) -> None:
        self.catalog_url = catalog_url if catalog_url[ : len(self.DOMIN)] == self.DOMIN else self.DOMIN + catalog_url
        self.outpath_name = outpath_name
        self.check_path(self.outpath_name)
        self.capture_format = capture_format
        self.image_format = image_format
        self.max_capture_number_length = max_capture_number_length
        self.max_page_number_length = max_page_number_length
        self.work_span = work_span
        self.affix = Affix_OnlyZeroExample()

        self.page_counter = 0
    
    def toreload_format_page_name(self, index: int):
        return self.image_format.format(arg = self.affix.add_prefix(str(index), self.max_page_number_length))
    def toreload_format_capture_name(self, index: int, capture_title: str):
        return self.capture_format.format(arg = self.affix.add_prefix(str(index), self.max_page_number_length) + capture_title)

    def check_path(self, path: str) -> None:
        if not os.path.exists(path):
            os.mkdir(path)
            logger.debug(f'建立目录:{path}...')

    def save_image(self) -> None:
        pass

    def get_html_soup(self, url: str) -> BeautifulSoup:
        res = requests.get(url)
        soup = BeautifulSoup(res.text)
        return soup

    def get_catalog(self) -> dict[int, tuple[str, str]]:
        '''return: dict[index, tuple[url, capture_title]]'''
        soup = self.get_html_soup(self.catalog_url)
        li_tag_list: list[BeautifulSoup] = soup.find('ul', class_ = 'chapter-list clearfix').findAll('li')
        catalog = {}
        for i, each in enumerate(li_tag_list):
            catalog[i + 1] = self.DOMIN + each.a['href'], each.a.string 
        return catalog

    def download_one_capture_perpage(self, soup: BeautifulSoup, foldername: str) -> None:
        li_tag_list: list[BeautifulSoup] = soup.find('div', class_ = 'comiclist').findAll('div', class_ = 'comicpage')
        for each in li_tag_list:
            url: str = each.img['src']
            res = requests.get(url)
            self.page_counter += 1
            filename = remove_invalid_element_in_windows_path(self.toreload_format_page_name(self.page_counter))
            with open(f'{self.outpath_name}/{foldername}/{filename}', 'wb') as f:
                f.write(res.content)
                #logger.log(f'{filename}')

            
    def download_one_capture(self, url: str, foldername: str) -> None:
        self.check_path(f'{self.outpath_name}/{foldername}')
        self.page_counter = 0
        soup = self.get_html_soup(url)
        total_pages = int(re.search('第[0-9]+/([0-9]+)页', soup.find('select', class_ = 'selectpage').option.string).group(1))
        logger.log('html page 1')
        self.download_one_capture_perpage(soup, foldername)
        for i in range(2, total_pages + 1):
            logger.log(f'html page {i}')
            soup = self.get_html_soup(url.replace('.html', f'?page={i}'))
            self.download_one_capture_perpage(soup, foldername)

    @try_except_ensure
    def download_all_caputres(self) -> None:
        catalog = self.get_catalog()
        work_span_low, work_span_high = self.work_span
        flag = work_span_high > work_span_low
        logger.debug(f'work span flag:{flag}, low:{work_span_low}, high:{work_span_high}')
        for key, value in catalog.items():
            if flag:
                if key > work_span_high or key < work_span_low:
                    continue
            logger.log(f'章节进度:{key}/{len(catalog)}')
            url, capture_title = value
            capture_name = remove_invalid_element_in_windows_path(self.toreload_format_capture_name(key, capture_title))
            self.download_one_capture(url, capture_name)


if __name__ == '__main__':
    x = SpiderX(
        'https://www.didiaomh.com/manhua/6500.html',
        outpath_name = '偷星九月天IMAGES',
    )
    x.download_all_caputres()

    class OPM(Image_HTMLwrapper_Lv2):
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


    y = OPM(
        root = '偷星九月天IMAGES',
        html_path = '偷星九月天HTMLS',
        html_vital_element= '偷星九月天 {arg}',
        html_collection_name= ' 偷星九月天 全集 ',
        prefix_LvRoot='capture',
        prefix_Lv2='image'
    )
    y.create_htmls()