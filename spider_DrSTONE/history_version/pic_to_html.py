import os

PICTURE_PATH = 'out/'
HTML_PATH = 'html/'

def make_one_capture_to_html(folder_name: str) -> None:
    pages = [each for each in os.listdir(PICTURE_PATH + folder_name) if each[ : 4] == 'page']
    pages = sorted(pages)
    html = '''
<!DOCTYPE html>
<html>
<head>
	<title>temp</title>
	<meta charset="utf-8">
    <style>
		div#MrSTONEpages{{
            text-align: center;
		}}
	</style>
    
</head>
<body>
{images}
</body>
</html>
'''
    img = '    <div id="MrSTONEpages"><img onload="if(this.width >= document.documentElement.clientWidth){{this.width = document.documentElement.clientWidth}}" align="middle" src="{page}"></img></div>\n'
    imgs = ''
    RELATIVE_PATH = '../' + PICTURE_PATH + folder_name + '/'
    for each in pages:
        imgs += img.format(page = RELATIVE_PATH + each)
    with open(HTML_PATH + folder_name + '.html', 'w', encoding='utf-8') as f:
        f.write(html.format(images = imgs))



if __name__ == '__main__':
    if not os.path.exists(HTML_PATH): os.mkdir(HTML_PATH)
    capture_folders = [each for each in os.listdir(PICTURE_PATH) if each[ : 7] == 'capture']
    for each in capture_folders:
        make_one_capture_to_html(each)
    



