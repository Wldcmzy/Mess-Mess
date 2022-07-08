from tkinter.filedialog import askopenfilename, askdirectory
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from tkinter import *
import os

READ_SIZE = (1 << 27) # 128MB


root = Tk()
root.title("加密小工具(AES-ECB)")
path = StringVar()
outpath = StringVar()

MemoryVar = StringVar()
MemoryVar.set('00G 00M')

KeyVar = StringVar()
statusVar = StringVar()

WORKING = False

def make_top(_type : str, msg : str) -> None:
    '''弹窗提示'''
    top=Toplevel()
    top.title(_type)
    top.attributes('-alpha',0.9) 
    msg=Message(top,text=msg,width=300)
    msg.pack() 

def change_Memory_show(Bs : int) -> None:
    GBs = Bs // (1 << 30)
    MBs = (Bs // (1 << 20)) % (1 << 10)
    MemoryVar.set(f'{GBs}G {MBs}M')

def encrypt_AES_ECB() -> None:
    '''
    使用密钥key, 以ECB模式使用AES加密origin_file文件, 输出为target_file
    key : 密钥
    origin_file : 源文件路径
    read_size : 单次读取数据的大小
    '''
    global WORKING
    try:
        print('加密')

        if WORKING: raise Exception('有任务尚未完成')
        key = KeyVar.get().strip()
        if len(key) != 16: raise Exception('密钥长度不对')
        key = key.encode('utf-8')
        WORKING = True
        origin_file = path.get().strip()
        target_file = outpath.get().strip() + '\\' + origin_file.split('\\')[-1] + '.myAES'
        
        cipher = AES.new(key, AES.MODE_ECB)
        with open(origin_file, 'rb') as fin:
            fout, Bcounter = open(target_file, 'wb'), 0
            while True:
                block = fin.read(READ_SIZE - 1)
                if not len(block): break
                block = pad(block, AES.block_size, style='pkcs7')
                Bcounter += len(block)

                fout.write(cipher.encrypt(block))
                change_Memory_show(Bcounter)
                print(f'已处理量:{MemoryVar.get()}')

                if not (Bcounter % (1 << 30)):
                    fout.close()
                    fout = open(target_file, 'ab')
            fout.close()
            #make_top('提示', '加密完成')
            print('加密完成')
    except Exception as ee:
        make_top('错误信息', str(type(ee)) + str(ee))
        
    WORKING = False

def decrypt_AES_ECB() -> None:
    '''
    使用密钥key, 以ECB模式使用AES解密cipher_file文件, 输出为target_file
    key : 密钥
    origin_file : 加密文件路径
    '''
    global WORKING
    try:
        print('解密')
        if WORKING: raise Exception('有任务尚未完成')
        key = KeyVar.get().strip()
        if len(key) != 16: raise Exception('密钥长度不对')
        key = key.encode('utf-8')
        cipher_file = path.get().strip()
        if len(cipher_file) >= 6 and cipher_file[-6 : ] != '.myAES': 
            raise Exception('要解密的文件应当以".myAES"结尾')
        WORKING = True
        target_file = outpath.get().strip() + '\\' + cipher_file[ : -6].split('\\')[-1]
        cipher = AES.new(key, AES.MODE_ECB)

        with open(cipher_file, 'rb') as fin:
            fout, Bcounter = open(target_file, 'wb'), 0
            while True:
                block = fin.read(READ_SIZE)
                if not len(block): break
                Bcounter += len(block)

                block = cipher.decrypt(block)
                try:
                    block = unpad(block, AES.block_size, style='pkcs7')
                except Exception as e:
                    print(f'unpad不成功,对密文第{Bcounter}B之前128bit的解密可能有问题 {type(e)} | {str(e)}')
                fout.write(block)
                change_Memory_show(Bcounter)
                print(f'已处理量:{MemoryVar.get()}')

                if not (Bcounter % (1 << 30)):
                    fout.close()
                    fout = open(target_file, 'ab')
            fout.close()
            #make_top('提示', '解密完成')
            print('解密完成')
    except Exception as ee:
        make_top('错误', str(type(ee)) + str(ee))
    
    WORKING = False

def selectPath():
    path.set(askopenfilename().replace("/", "\\"))
def selectOutPath():
    outpath.set(askdirectory().replace("/", "\\"))
    


def openPath():
    dir = os.path.dirname(path.get().strip()+"\\")
    os.system('start ' + dir)
def openOutPath():
    dir = os.path.dirname(outpath.get().strip()+"\\")
    os.system('start ' + dir)


Label(root, text="文件路径:").grid(row=0, column=0)
Entry(root, textvariable=path,state="readonly").grid(row=0, column=1,ipadx=200)
Label(root, text="输出路径:").grid(row=1, column=0)

# e.insert(0,os.path.abspath("."))
Button(root, text="文件选择", width = 10, command=selectPath).grid(row=0, column=2)
Button(root, text="打开文件位置", width = 10, command=openPath).grid(row=0, column=3)
Button(root, text="目录选择", width = 10, command=selectOutPath).grid(row=1, column=2)
Button(root, text="打开目录位置", width = 10, command=openOutPath).grid(row=1, column=3)

# Label(root, text = '已处理量:').grid(row = 3, column = 0)
# Label(root, textvariable = MemoryVar).grid(row = 3, column = 1)
Entry(root, textvariable=outpath,state="readonly").grid(row=1, column=1,ipadx=200)
Button(root, text = '加密', width = 10, command=encrypt_AES_ECB).grid(row = 2, column = 2)
Button(root, text = '解密', width = 10, command=decrypt_AES_ECB).grid(row = 2, column = 3)

Label(root, text = '128bit密钥:').grid(row = 2, column = 0)
Entry(root, textvariable=KeyVar).grid(row=2, column=1,ipadx=200)

root.mainloop()




