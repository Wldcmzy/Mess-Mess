import os
import hashlib

path = 'out/'
folders = os.listdir(path)
lst404 = []
for folder in folders:
    pages = os.listdir(path + folder + '/')
    dic = {}
    for page in pages:
        with open(path + folder + '/' + page, 'rb') as f:
            hasher = hashlib.md5(f.read())
            hash = hasher.hexdigest()
        if hash not in dic: 
            dic[hash] = 1
        else:
            lst404.append(folder)
            print(folder)
            break
with open('404captures.txt', 'w') as f:
    for each in lst404:
        f.write(each + '\n')