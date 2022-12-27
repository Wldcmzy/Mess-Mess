from tkinter import *
from myutils.EngLiteBase import Render, Word

# 随机选择单词的等级范围[0 - LEVEL]
LEVEL = 0

#随机选择单词的数量
NUMBER = 2

#使用哪个数据库
DBNAME = 'civi.db'

TITLE = '拉跨的EngLite2'
WINDOW_SIZE = '1500x720'
WINDOW_POS = '+0+30'

PADX = 20
PADY = 10

FG_EN = 'brown'
FG_PRON = 'blue'
FG_CN = 'red'
FG_COMBO = 'black'

if __name__ == '__main__':
    word_service, word_reservists = None, None
    render = Render(DBNAME, LEVEL, NUMBER)

    root = Tk()
    frame = Frame(root)
    frame.pack()
    root.title(TITLE)
    root.geometry(WINDOW_SIZE + WINDOW_POS)
    root.resizable(20,20)

    en = StringVar()
    cn = StringVar()
    pron = StringVar()
    combo = StringVar()

    cn_shadow = StringVar()
    pron_shadow = StringVar()
    combo_shadow = StringVar()
    show_mod = 1

    en.set(f'点击开始背单词~\n\n 会就点左键, 不会就点右键~\n\n本次为您挑选了{NUMBER}个单词~')

    lb_en = Label(frame
            , textvariable = en
            ,padx = PADX ,pady = PADY
            ,fg = 'brown'
            ,font=('',50)
    )
    lb_en.grid(row = 5, column = 5)

    lb_pron = Label(frame
            , textvariable = pron
            ,padx = PADX ,pady = PADY
            ,fg = FG_PRON
            ,font=('',22)
    )
    lb_pron.grid(row = 10, column = 5)

    lb_cn = Label(frame
            , textvariable = cn
            ,padx = PADX ,pady = PADY
            ,fg = FG_CN
            ,font=('',22)
    )
    lb_cn.grid(row = 15, column = 5)

    lb_combo = Label(frame
            , textvariable = combo
            ,padx = PADX ,pady = PADY
            ,fg = FG_COMBO
            ,font=('',22)
    )
    lb_combo.grid(row = 20, column = 5)

    def set_word_preview(word: Word):
        cen, ccn, cpron, ccombo = word.enter_cut()
        en.set(cen)
        cn.set(ccn)
        pron.set(cpron)
        combo.set(ccombo)
    
    def exchange_show_mod():
        def swap(x: StringVar, y: StringVar):
            t = y.get()
            y.set(x.get())
            x.set(t)
        global show_mod
        global cn_shadow, cn
        global pron_shadow, pron
        global combo_shadow, combo
        swap(cn, cn_shadow)
        swap(pron, pron_shadow)
        swap(combo, combo_shadow)
        show_mod ^= 1

    def change_word():
        global word_service, word_reservists, render

        if word_reservists == None:
            word_service = render.choice()
        else:
            word_service = word_reservists
        word_reservists = render.choice()

        if word_service == None:
            set_word_preview(Word(('已经没有单词了~', '', '', '', None, None)))
        else:
            set_word_preview(word_service)
            print(word_service.en, f'level={word_service.level} E={word_service.e}')


    def user_reply(yes: bool):
        if word_service == None:
            return
        if yes == True:
            render.hasGrasp(word_service)
        else:
            render.hasWrong(word_service)

    def autochange(event, yes: bool):
        if show_mod:
            user_reply(yes)
            change_word()
        exchange_show_mod()
        
    
    root.bind('<Button-1>', lambda event : autochange(event, True))
    root.bind('<Button-3>', lambda event : autochange(event, False))

    frame.focus_set()

    mainloop()
