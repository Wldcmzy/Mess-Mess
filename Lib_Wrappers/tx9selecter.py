import os
import cv2
import numpy as np
from Wrappers.Affix import Affix_OnlyZeroExample

af = Affix_OnlyZeroExample()
picpath = '偷星九月天IMAGES'
htmlpath = '偷星九月天HTMLS'

def a():
    cnt = 0
    for i, each in enumerate(os.listdir(picpath)):
        src = f'{picpath}/{each}/image001.jpg'
        y = cv2.imdecode(np.fromfile(src,dtype=np.uint8),cv2.IMREAD_COLOR)
        r, c, d = y.shape
        x = cv2.resize(y, (c // 2, r // 2))
        print(i)
        cv2.imshow('tx', x)
        key=cv2.waitKey(0)
        cv2.destroyWindow('tx')
        print('进行到: ', i)
        if key == 32:
            cnt += 1
            spath = f'extra/ex{af.add_prefix(str(cnt), 3)}.jpg'
            cv2.imwrite(spath, y)
        print(key)
