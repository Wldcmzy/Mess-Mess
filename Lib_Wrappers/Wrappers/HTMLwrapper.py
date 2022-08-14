from os import mkdir, listdir
from os.path import exists, isdir, isfile
import re
from .__init__ import logger, try_except_ensure

class Image_HTMLwrapper_Lv2:
    HTML: str = '''
<!DOCTYPE html>
<html>
<head>
	<title>{title}</title>
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
    IMAGE: str = '    <div id="pages"><img onload="if(this.width >= document.documentElement.clientWidth){{this.width = document.documentElement.clientWidth}}" align="middle" src="{image}"></img></div>\n'
    P_VITAL: str = '   <p id="p"><strong>{vital_element}</strong></p>\n'
    P_DIFF: str = '<span id="capture_number">{diff_element}</span>'
    SEP: str = '    <br><br>\n    <hr style="FILTER:alpha(opacity=100,finishopacity=0,style=3)" width="95%"color=#00FF7F SIZE=5>'

    def __init__(
        self, 
        root: str,
        html_path: str = 'Image_HTMLwrapper_Lv2.htmlfolder',
        html_vital_element: str = 'Images Index={arg}',
        html_collection_name: str = 'ALL',
        prefix_LvRoot: str = 'LvRoot', 
        prefix_Lv2: str = 'Lv2',
    ) -> None:
        '''
        root: 二级文件系统根目录(相对路径,不以斜线结尾)
        html_path: html文件存放目录名(与主程序文件同目录,仅名称)
        html_vital_element: 一个提炼精华的描述,作为html标题和文件名的一部分,必须含有字符串'{arg}'
        html_collection_name: 合集文件名称
        prefix_LvRoot: 一级目录中可处理目录的前缀(针对文件夹)
        prefix_Lv2: 二级目录中可处理文件前缀(针对文件)
        '''
        self.root = root
        self.html_path = re.sub(r'[\\|/|:|*|?|\"|<|>|\|]','', html_path)
        self.html_vital_element = re.sub(r'[\\|/|:|*|?|\"|<|>|\|]','', html_vital_element)
        self.html_collection_name = re.sub(r'[\\|/|:|*|?|\"|<|>|\|]','', html_collection_name)
        self.prefix_LvRoot = prefix_LvRoot
        self.prefix_Lv2 = prefix_Lv2
        self.html_vital_element_P = Image_HTMLwrapper_Lv2.P_VITAL.format(vital_element = self.html_vital_element)

    def toreload_parse_diff_element_title(self, folder_name: str) -> str:
        '''
        自定义title标签内容,也作为html文件命名参考
        folder_name:
            对应的二级目录名称
        return:
            自定义值,这里为去除二级目录前缀的剩余部分
        '''
        ret = folder_name[len(self.prefix_LvRoot) : ]
        return ret
    
    def toreload_parse_diff_element_P(self, folder_name: str) -> str:
        '''
        自定义p标签内容
        folder_name:
            对应的二级目录名称
        return:
            自定义值,这里为去除二级目录前缀的剩余部分
        '''
        ret = folder_name[len(self.prefix_LvRoot) : ]
        return ret


    def parse_one_Lv2_folder(self, folder_name: str) -> str:
        '''
        解析一个二级目录中所有的图片,把他们制作成html语言的<img>标签
        folder_name:
            对应的二级目录名称
        return:
            所有图片对应的html语言字符串
        '''
        images = [each for each in listdir(f'{self.root}/{folder_name}') if each[ : len(self.prefix_Lv2)] == self.prefix_Lv2 and isfile(f'{self.root}/{folder_name}/{each}')]
        images = sorted(images)
        html = ''
        image_src = f'../{self.root}/{folder_name}/'
        for each in images:
            html += Image_HTMLwrapper_Lv2.IMAGE.format(image = image_src + each)
        return html

    def create_one_html(self, name: str, html: str) -> None:
        '''
        创建一个HTML格式文件
        name:
            HTML文件名称
        html:
            若干图片对应的html语言字符串
            建议以parse_one_Lv2_folder方法的返回值作为参数
        '''
        name = re.sub(r'[\\|/|:|*|?|\"|<|>|\|]','', name)
        with open(f'{self.html_path}/{name}.html', 'w', encoding='utf-8') as f:
            f.write(Image_HTMLwrapper_Lv2.HTML.format(title = f'{name}', args = html))
        logger.log(f'{name}.html创建完成...')
    
    @try_except_ensure
    def create_htmls(self, collection: bool = True):
        '''
        为所有二级目录创建HTML格式文件
        collection:
            True = 创建合集HTML文件
            False = 不创建
        '''
        if not exists(self.html_path):
            mkdir(self.html_path)
        logger.debug(f'{self.html_path}不存在, 创建成功')
        folders = [each for each in listdir(self.root) if each[ : len(self.prefix_LvRoot)] == self.prefix_LvRoot and isdir(f'{self.root}/{each}')]
        totalhtml = ''
        for each in folders:
            title_name = self.html_vital_element.format(arg = self.toreload_parse_diff_element_title(each))
            inner_Ptag = self.html_vital_element_P.format(arg = Image_HTMLwrapper_Lv2.P_DIFF.format(diff_element = self.toreload_parse_diff_element_P(each)))
            html = Image_HTMLwrapper_Lv2.SEP
            html += inner_Ptag
            html += self.parse_one_Lv2_folder(each)
            self.create_one_html(title_name, html)
            if collection:
                totalhtml += html
        if collection:
            self.create_one_html(self.html_collection_name, totalhtml)