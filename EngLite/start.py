from tkinter import *
import random
activeFile = 'computerEng/computerEngU9A.xyz'
#activeFile = 'z_temp.txt'
OK = []
NO = []
def load():
    global OK, NO
    with open(activeFile, 'r', encoding='utf-8') as file:
        lst = [each.split(' ') for each in file.read().strip().split('\n')]
        OK = [each for each in lst if each[2] != '0']
        NO = [each for each in lst if each[2] == '0']
def dump():
    global OK, NO
    with open(activeFile, 'w', encoding='utf-8') as file:
        for each in OK:
            file.write(each[0] + ' ' + each[1] + ' ' + each [2] + '\n')
        for each in NO:
            file.write(each[0] + ' ' + each[1] + ' ' + each [2] + '\n')
def changeWord(arg):
    global word, zi, vb, zi2
    vb = None if len(NO) == 0 else random.choice(NO)
    word.set('__None__' if vb == None else vb[0])
    zi.set('__None__' if vb == None else ' ')
    zi2 = vb[1] if vb != None else ' '
def kill(arg):
    if(len(NO) == 0): return
    tt = [word.get(), zi.get(), '0']
    if tt not in NO:
        tt[1] = zi2
    NO.remove(tt)
    tt[2] = '1'
    OK.append(tt)
    changeWord(1)
def show_hide(arg):
    global zi, zi2
    tmp = zi.get()
    zi.set(zi2)
    zi2 = tmp
def exit(arg):
    global root
    root.quit()
if __name__ == '__main__':
    load()
    root = Tk()
    frame = Frame(root)
    frame.pack()
    root.title('拉跨的背单词软件')
    root.geometry('1500x760')
    root.resizable(20,20)
    word = StringVar()
    zi = StringVar()
    zi2 = ''
    img = PhotoImage(file = 'warpper/RD3.png')
    lb = Label(frame
            #, text = 'as'
            , textvariable = word
            #, img = ''
            #, image = img
            ,padx = 20 ,pady = 10
            ,fg = 'blue'
            ,font=('',35)
    )
    lb.grid(row = 1, column = 3)
    lb = Label(frame
            #, text = 'as'
            , textvariable = zi
            #, img = ''
            #, image= img
            ,padx = 20 ,pady = 10
            ,fg = 'red'
            ,font=('',35)
    )
    lb.grid(row = 2, column = 3)
    Label(frame, image = img).grid(row = 50, column = 3)
    frame.focus_set()
    frame.bind('<Shift-KeyPress-Q>', exit)
    frame.bind('<Shift-KeyPress-D>', changeWord)
    frame.bind('<Shift-KeyPress-S>', kill)
    frame.bind('<Shift-KeyPress-F>', show_hide)
    root.bind('<Button-1>', changeWord)
    root.bind('<Button-3>', show_hide)
    root.bind('<Button-2>', kill)
    #root.bind('<Button-1>', exit)
    changeWord(1)
    mainloop()
    dump()