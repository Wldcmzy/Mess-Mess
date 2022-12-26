from typing import Any, Union

REFRESH_SEP = 4000
FILENAME = 'BStationElementSerach.txt'

mydict: dict[str, dict[str, Union[list[str], str]]] = {
    '文明': {
        'keywords': [
            '肝文明', '玩文明', '打文明', '文明4', '文明5', '文明6', '文明VI', '统治胜利', '科技胜利',
            '文化胜利', '外交胜利', '分数胜利', '宗教胜利', '老秦', '无战飞', '核动力圣地', '宗铺', 
            '商铺', '爆铺', '精铺', '极光之舞', '沙漠民俗', '主神纪念碑', '锻造之神', '雪特拉', '海特拉', 
            '泛滥平原', '合唱圣歌',
        ],
        'color': '#c929f5',
    },
    '洞口骑士': {
        'keywords': [
            '空洞骑士', '洞口骑士', '丝之鸽', '丝之歌', '苦痛之路', '辐辉', '佐特', '奎若', '蓝湖', 
            'r45', '小骑士', '辐光', '龙牙哥', '龙牙姐', '三螳螂', '力量快劈', '稳体', '四锁',
            '遗忘十字路', '苍绿之径', '真菌荒地', '雾之峡谷', '古老盆地', '皇家水道', '王国边缘', 
            '乌恩', '愚人竞技场', 'jjc3', '亡怒', '钢魂', '白色宫殿', '酸冲', '劈魂', '骨钉', '马爹',
            '毛里克', '下砸', '劈波', '扭波', '0白', '黑吼', '梦盾', '梦之盾', '梦钉', '假骑士'
        ],
        'color': '#2532e9',
    },
    '蔚蓝': {
        'keywords' : [
            '蔚蓝', '玛德琳', 'celeste', 'Celeste', '兔子跳', '蹭墙跳', '大跳', '凌波', 
            '无体力上墙', '春三', '春四', '春五', '春3', '春4', '春5', '金草莓', '心门', 
            'superdash', 'hyper', '连u', '反泡泡',
        ],
        'color': '#ff2e42',
    },
    '求批': {
        'keywords' : [
            '求生之路', '打求', 'tank', 'witch', '药抗', '药役', '挂边躲牛','evo', '1tc', 'mayuyu', 
            '秒妹', 'Anne', 'diandian', 'zonemod', '消耗克', 'hunter', '一位喷', 'charger', '特感',
            'jockey', 'spitter','smoker', 'boomer', 'RBT', 'VGT', 'nv', 'pubstar', 'amagami',
            '砍舌', '脸接25', '喋血蜃楼', '闪电突袭', '死亡中心', '黑色狂欢节', '黑色嘉年华', 'c2改',
            '沼泽激战', '暴风骤雨', '教区', '短暂时刻', '死亡丧钟', '坠机险途', '寂静时分', '刺骨寒溪',
            '临死一搏',
        ],
        'color': '#b93837',
    },
    # '小黑子':{
    #      'keywords' : [
    #         '鸡你太美', 'ikun', '蔡徐坤', '只因', '坤坤', '两年半', '个人练习生', '你干嘛', '唱跳rap', 
    #         '小黑子'
    #         ],
    #      'color': '#d7af0f',
    # },

}


MAIN_STRING = '''
// ==UserScript==
// @name         程序自动生成的B站成分查看脚本
// @namespace    ScriptForAutoGenerateBStationElementSearchScript
// @version      0.1
// @description  自动生成的B站成分查看脚本, 暂不支持混合标签
// @author       xulaupuz&nightswan&高贵乡公&脚本使用者
// @match        https://www.bilibili.com/video/*
// @match        https://www.bilibili.com/bangumi/play/*
// @match        https://t.bilibili.com/*
// @match        https://space.bilibili.com/*
// @match        https://space.bilibili.com/*
// @match        https://www.bilibili.com/read/*
// @icon         https://static.hdslb.com/images/favicon.ico
// @connect      bilibili.com
// @grant        GM_xmlhttpRequest
// @license MIT
// @run-at document-end
// ==/UserScript==
 

(function () {{
    'use strict';
    const unknown = new Set()
 
    //成分，可自定义
    const nor = new Set()
    {CODE_define_set}

 
    //关键词，可自定义
    {CODE_define_keyword}

    //贴上标签，可自定义
    const tag_nor = " [普通]"
    {CODE_define_tag}
 
 
    const blog = 'https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space?&host_mid='
    const is_new = document.getElementsByClassName('item goback').length != 0 // 检测是不是新版
 
    //标签颜色，可自定义，默认为B站会员色
    const tag_nor_Inner = "<b style='color: #11DD77'>" + tag_nor + "</b>"
    {CODE_define_Inner}
 
 
    const get_pid = (c) => {{
        if (is_new) {{
            return c.dataset['userId']
        }} else {{
            return c.children[0]['href'].replace(/[^\d]/g, "")
        }}
    }}
 
    const get_comment_list = () => {{
        if (is_new) {{
            let lst = new Set()
            for (let c of document.getElementsByClassName('user-name')) {{
                lst.add(c)
            }}
            for (let c of document.getElementsByClassName('sub-user-name')) {{
                lst.add(c)
            }}
            return lst
        }} else {{
            return document.getElementsByClassName('user')
        }}
    }}
 
 
    console.log(is_new)
    console.log("正常加载")
 
 
    let jiance = setInterval(() => {{
        let commentlist = get_comment_list()
        if (commentlist.length != 0) {{
            // clearInterval(jiance)
            commentlist.forEach(c => {{
                let pid = get_pid(c)

                {CODE_add_Inner}

                if (nor.has(pid)) {{
                    if (c.textContent.includes(tag_nor) === false) {{
                        c.innerHTML += tag_nor_Inner
                    }}
                    return
                }}

                unknown.add(pid)
                //console.log(pid)
                let blogurl = blog + pid
                // let xhr = new XMLHttpRequest()
                GM_xmlhttpRequest({{
                    method: "get",
                    url: blogurl,
                    data: '',
                    headers: {{
                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
                    }},
                    onload: function (res) {{
                        if (res.status === 200) {{
                            //console.log('成功')
                            let st = JSON.stringify(JSON.parse(res.response).data)
                            
                            unknown.delete(pid)
                            
                            let tag_flag = false

                            {CODE_add_tag}

                            //添加纯良标签
                            if (!tag_flag) {{
                                c.innerHTML += tag_nor_Inner
                                nor.add(pid)
                            }}
                        }} else {{
                            console.log('失败')
                            console.log(res)
                        }}
                    }},
                }});
            }});
        }}
    }}, {refresh_sep})
}})();

'''

def define_one_set(tag_name: str) -> str:
    _ = f'const set_{tag_name} = new Set()\n'
    return _

def define_one_tag(tag_name: str) -> str:
    _ = f'const tag_{tag_name} = " [{tag_name}]"\n'
    return _

def define_one_keyword(keyword_name: str) -> str:
    _ = f'const keyword_{keyword_name} = "{keyword_name}"\n'
    return _

def define_one_Inner(tag_name: str, color = None) -> str:
    style = '' if not color else f'style=\'color: {color}\''
    _ = f'const tag_Inner_{tag_name} = "<b {style}>" + tag_{tag_name} + "</b>"\n'
    return _
    

def add_one_tag(tag_name: str):
    lst: list[str] = mydict[tag_name]['keywords']
    _keywords_judge = f'st.includes(keyword_{lst[0]})'
    for each_keyword in lst[1 : ]:
        _keywords_judge += f' || st.includes(keyword_{each_keyword})'

    _ = '''
    if ({CODE_keywords_judge}) {{
        c.innerHTML += {CODE_Inner}
        {CODE_set}.add(pid)
        tag_flag = true
    }}
    '''.format(
        CODE_keywords_judge = _keywords_judge,
        CODE_Inner = f'tag_Inner_{tag_name}',
        CODE_set = f'set_{tag_name}',
    )
    return _

def add_one_Inner(tag_name: str) -> str:
    _='''
        if ({CODE_set}.has(pid)) {{
            if (c.textContent.includes({CODE_tag}) === false) {{
                c.innerHTML += {CODE_Inner}
            }}
            return
        }}
    '''.format(
        CODE_set = f'set_{tag_name}',
        CODE_tag = f'tag_{tag_name}',
        CODE_Inner = f'tag_Inner_{tag_name}',
    )
    return _

def install_tags() -> str: 
    CODE_define_set = ''
    CODE_define_keyword = ''
    CODE_define_tag = ''
    CODE_define_Inner = ''
    CODE_add_tag = ''
    CODE_add_Inner = ''

    unique_keyword = set()

    for key, value in mydict.items():
        keywords, color = value['keywords'], value['color']

        CODE_define_set += define_one_set(key)
        CODE_define_tag += define_one_tag(key)
        CODE_define_Inner += define_one_Inner(key, color)
        for each_keyword in keywords:
            if each_keyword not in unique_keyword:
                CODE_define_keyword += define_one_keyword(each_keyword)
                unique_keyword.add(each_keyword)
        
        CODE_add_tag += add_one_tag(key)
        CODE_add_Inner += add_one_Inner(key)
    
    _ = MAIN_STRING.format(
        CODE_define_set = CODE_define_set,
        CODE_define_tag = CODE_define_tag,
        CODE_define_Inner = CODE_define_Inner,
        CODE_define_keyword = CODE_define_keyword,
        CODE_add_tag = CODE_add_tag,
        CODE_add_Inner = CODE_add_Inner,
        refresh_sep = REFRESH_SEP
    )
    return _
        
def run() -> None:
    global FILENAME
    with open(FILENAME, 'w', encoding='utf-8') as f:
        f.write(install_tags())

if __name__ == '__main__':
    run()
