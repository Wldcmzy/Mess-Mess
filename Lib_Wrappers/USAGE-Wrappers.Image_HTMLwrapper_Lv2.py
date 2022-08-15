from Wrappers.HTMLwrapper import Image_HTMLwrapper_Lv2

'''
Image_HTMLwrapper_Lv2使用案例

>>>预设情景:
1.  你现在拥有漫画Dr.STONE的所有图片,但是一张张翻页和放大看很累,所以你想制作一个html方便观看
2.  与本脚本同目录的./Dr.STONEpages文件夹以二级目录的形式储存了漫画Dr.STONE的所有图片, 文件目录格式形如:
    ====================
    |-Dr.STONEpages
    |   |capture001
    |   |   |page01.jpg
    |   |   |page02.jpg
    |   |   |page03.jpg
    |   |capture002
    |   |   |page01.jpg
    |   |   |page02.jpg
    |   |   |page03.jpg
    |   |capture003
    (以此类推)
    ====================

>>>实现方法:
1.  首先你要确保你的文件目录格式对于Image_HTMLwrapper_Lv2类来说是可处理的, 即符合如下描述的格式:
    ====================
    (可以参考情景预设理解)
    第一级目录的所有需处理的文件夹都有相同的前缀(如情景预设中的capture)
    第二级目录的所有需处理的文件都有相同的前缀(如情景预设中的page)
    ====================

2.  你可以通过[继承]写一个新类来实现需求,也可以直接使用Image_HTMLwrapper_Lv2类,两者略有差别,稍后解释,
    但不论使用哪一种方法,你只需要在[实例化]对象的时传入正确的[参数],然后调用create_htmls()方法即可实现目标,
    所以接下来会对[参数]进行说明
    
3.  构造函数参数解析
    (建议结合下方代码构造函数的默认参数理解)
    这些参数均类型均为str
    root:
        你的二级目录的根目录[相对路径],结尾不带'/'
    html_path:
        生成html文件的保存目录[名称],不是[路径], 这个目录可以自动创建,不必手动创建
    html_vital_element:
        以你自己的经验对这些图片集的内容简要概括,会用于命名html文件,填充title标签和部分p标签
        这个参数中必须包含字符串'{arg}',这个'{arg}'会根据二级目录名称被格式化为不同的内容以区分不同的html文件
    html_collection_name:
        合集html文件的文件名
        (合集html文件指:包含所有可处理二级目录中的所有可处理图片的html文件)
    prefix_LvRoot:
        一级目录中可处理目录的前缀
    prefix_Lv2:
        二级目录中可处理文件的前缀

4.使用Image_HTMLwrapper_Lv2类实现目标
    先实例化一个对象,保证参数填入正确,然后直接调用create_htmls()方法即可
    使用这种方法,生成的html文件的名称与其对应的二级目录名称相同,不可更改,想要更改需要通过[继承]创建新类

5.通过[继承]自定义新类继承Image_HTMLwrapper_Lv2类实现目标
    生成的html文件的命名方式为:去除其对应的二级目录前缀,剩下的部分经过一个自定义方法的变换,然后代替'{arg}'
    在Image_HTMLwrapper_Lv2类中,自定义方法被设计成原封不动返回传入参数,所以html文件名称与其对应的二级目录名称相同
    
    可以在[子类]中重写两个自定义方法,实现两种自定义'{arg}'内容:
    i.  toreload_parse_diff_element_title 这个方法决定html文件的名称和title标签内容
        输入: 二级目录名称
        输出: 你自定义算法的结果
    ii. toreload_parse_diff_element_P 这个方法决定html文件中p标签的内容
        输入: 二级目录名称
        输出: 你自定义算法的结果

    例如,下方代码中,html文件的标题为和title标签为
    [Dr.STONE石纪元第 001 话]
    而html文件中p标签为
    [Dr.STONE石纪元<第 1 话>]   (见6.ii)

6. 其他内容
    i.  create_htmls方法有一个collection参数,表示是否创建合集html文件,默认为True
        (合集html文件指:包含所有可处理二级目录中的所有可处理图片的html文件)
        当collection = True, 创建合集html文件
        当collection = False, 不创建合集html文件, 此时构造函数的html_collection_name参数失去意义
    ii. 不能作为windows系统文件名的字符在文件命名时会被剔除

7.  一些建议
    i.  html文件中的图片索引根据相对路径, 建议二级目录文件也和脚本文件在同目录, 
        方便html文件夹与原图文件夹(二级目录)一起移动
'''

if __name__ == '__main__':

    class DrSTONE(Image_HTMLwrapper_Lv2):
        def __init__(
            self, 
            root: str = './Dr.STONEpages',
            html_path: str = 'Dr.STONEhtmls:\\/?*:|<>',
            html_vital_element: str = 'Dr.STONE石纪元<第 {arg} 话>',
            html_collection_name: str = 'Dr.STONE石纪元 全集',
            prefix_LvRoot: str = 'capture', 
            prefix_Lv2: str = 'page',
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
            ret = folder_name[len(self.prefix_LvRoot) : ]
            return ret
        
        def toreload_parse_diff_element_P(self, folder_name: str) -> str:
            return str(int(super().toreload_parse_diff_element_P(folder_name)))
            
    x = DrSTONE()
    x.create_htmls()


# 截止到这里功能案例需求可以实现
#====================================


#====================================
# 其他示例

    x = DrSTONE(
        root = './Dr.STONEpages',
        html_path = 'Dr.STONEhtmls',
        html_vital_element = 'Dr.STONE石纪元 第 {arg} 话',
        html_collection_name = ' Dr.STONE石纪元 全集',
        prefix_LvRoot = 'capture', 
        prefix_Lv2 = 'page',
    )
    x.create_htmls()

    x = DrSTONE(
        root = './Dr.STONEREBOOTpages',
        html_path = 'Dr.STONEhtmls',
        html_vital_element = 'Dr.STONE石纪元外传-Reboot:百夜 第 {arg} 话',
        html_collection_name = ' Dr.STONE石纪元外传-Reboot:百夜 全集',
        prefix_LvRoot = 'capture', 
        prefix_Lv2 = 'page',
    )
    x.create_htmls()