from .sqlAPI import *
from .config import *
from typing import Optional
import random
import numpy

CUT_LENGTH = 40

class Operator:
    '''主要用于操作数据库信息'''
    def __init__(self, dbname: str) -> None:
        dbpath = Path(__file__).parent.parent / DB_FORDER / dbname 
        self.conn = opendb(dbpath)

    def addwords_BySearch(self, filename: str) -> None:
        filepath = Path(__file__).parent.parent / TXT_FORDER / filename

        with open(filepath, 'r', encoding = 'utf-8') as f:
            wordlist = f.read().strip().split('\n')

        addmany_BySearch(self.conn, wordlist)
    
    def addwords_ByFile(self):
        pass

    def select_words(self, levellow: int, levelhigh: int, numbermax: int):
        res = select_ByLevel(self.conn, levellow, levelhigh)
        if len(res) > numbermax:
            idx = numpy.random.choice(len(res), numbermax, replace = False)
            res = tuple(res[i] for i in idx)
        return res
    
    def update_level(self, en: str, level: int, e: int):
        modifyone(self.conn, en, level, e)

    def reset(self):
        reset(self.conn)

class Word:
    '''单词类'''
    def __init__(self, wordmsg) -> None:
        self.en, self.cn, self.pron, self.combo, self.level, self.e = wordmsg
        self.errortimes = 0
        self.repeat = 0
    
    def __str__(self):
        return f'''
{self.en}
{self.cn}
{self.pron}
{self.combo}
level={self.level} E={self.e}
        '''.strip()
    
    def __repr__(self):
        return self.__str__()

    def enter_cut(self):
        def _(x: str):
            def __(y : str):
                if len(y) > CUT_LENGTH:
                    return y[ : CUT_LENGTH] + '\n' +  _(y[CUT_LENGTH : ])
                return y
            ret = ''
            for each in x.split('\n'):
                ret += __(each) + '\n'
            return ret.strip()
        return _(self.en), _(self.cn), _(self.pron), _(self.combo)

class Render:
    '''实现用户背单词的交互逻辑'''
    def __init__(self, dbname: str, level: int, maxnum: int) -> None:
        self.worker = Operator(dbname)
        self.wordlist = self.worker.select_words(0, level, maxnum)
        self.wordlist = [Word(i) for i in self.wordlist]

    def choice(self) -> Optional[Word]:
        try:
            i = random.randint(0, len(self.wordlist) - 1)
            word = self.wordlist[i]
            del self.wordlist[i]
        except ValueError:
            word = None
        return word
    
    def hasGrasp(self, word: Word):
        if word.errortimes > 2 and word.repeat < 4:
            word.repeat += 1
            self.wordlist.append(word)
            return
        if word.errortimes > 0 and word.repeat < 2:
            word.repeat += 1
            self.wordlist.append(word)
            return

        if word.errortimes < 1:
            word.e += 1
            word.level = random.randint(2 ** (word.e - 1), 2 ** word.e)
            print(f'set {word.en} level={word.level}, E={word.e}')
        self.worker.update_level(word.en, word.level, word.e)        

    def hasWrong(self, word:Word):
        word.e = 0
        word.level = 0
        word.errortimes += 1
        word.repeat = 0
        self.wordlist.append(word)
        print(f'set {word.en} level={word.level}, E={word.e}')
    

