'''数据库操作API'''

import sqlite3
from pathlib import Path
from .PyTranslator import Search_words
from .log import logger
import tqdm
import re
import time
import numpy
from typing import Optional

def opendb(path: Path) -> sqlite3.Connection:
    if not path.exists():
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE WORD(
            EN           TEXT       PRIMARY KEY,
            CN           TEXT       ,
            PRONOUNCE    TEXT       ,
            COMBO        TEXT       ,
            LEVEL        INTEGER    ,
            E            INTEGER    ,
            FLAG         INTEGER    );
        ''')
    else:
        conn = sqlite3.connect(path)   
    return conn
    
def query(searcher: Search_words, word: str) -> Optional[tuple[str]]:
    try:
        res = searcher.Simple_search(word)

        en = res['Word']
        pron = ''
        if res['pronounce'] != []:
            if len(res['pronounce']) <= 1:
                pron = f"{res['pronounce'][0]}"
            else:
                pron = f"{res['pronounce'][0]} 英 & {res['pronounce'][1]} 美"
        cn = re.sub(' +', ' ', str(list(_ for _ in res['Simple-meaning']))[1 : -1].replace(',', '\n').replace('\'', '')).replace('\n ', '\n')
        combo = re.sub(' +', ' ', str(list(_[0] + re.sub('[\n| ]', '', _[1]) for _ in res['Phrase']))[1 : -1].replace(',', '\n').replace('\'', '')).replace('\n ', '\n')

        return en, cn, pron, combo
    except Exception as e:
        logger.error(f'{type(e)}|{str(e)}|word:{word}')   
        return None

def addone(
    cursor: sqlite3.Cursor, 
    en: str, 
    cn: str, 
    pronounce: str, 
    combo: str,
    level: int,
    exponential: int,
    flag: int,
    ) -> None:
    try:
        if cn == '':
            raise Exception(f'单词{en}无中文释义, 无音标={pronounce == ""}, 无组合={combo == ""}')
        cursor.execute(f'''
            INSERT INTO WORD (EN, CN, PRONOUNCE, COMBO, LEVEL, E, FLAG)
            VALUES ("{en}", "{cn}", "{pronounce}", "{combo}", "{level}", "{exponential}", "{flag}");
        ''')
    except Exception as e:
        logger.error(f'<at:database.sqlApi.addone>|{type(e)}|{str(e)}')

def addmany_BySearch(conn: sqlite3.Connection, wordlist: list[str], delay: int = 1) -> None:
    searcher=Search_words()
    cursor = conn.cursor()
    for i in tqdm.tqdm(range(len(wordlist))):
        word = wordlist[i]
        x = query(searcher, word)
        if x == None: continue
        en, cn, pron, combo = x
        addone(cursor, en, cn, pron, combo, 0, 0, 0)
        conn.commit()
        time.sleep(delay)
    

def addmany_ByFile(conn: sqlite3.Connection, wordlist: list[str]) -> None:
    pass

def select_ByLevel(conn: sqlite3.Connection, low: int, high: int) -> tuple[tuple[str, int]]:
    if low > high:
        raise Exception('Level区间错误')
    
    cur = conn.cursor()
    sql = f'select * from WORD where LEVEL between {low} and {high}'
    cur.execute(sql)

    return cur.fetchall()

def modifyone(conn: sqlite3.Connection, word: str, level: int, exponential: int) -> None:
    cur = conn.cursor()
    sql = f'update WORD set LEVEL = {level}, E = {exponential} where EN = "{word}"'
    cur.execute(sql)
    conn.commit()

def reset(conn: sqlite3.Connection):
    print('reset LEVEL, E, FLAG to 0')
    cur = conn.cursor()
    sql = 'update WORD set LEVEL = 0, E = 0, FLAG = 0'
    cur.execute(sql)
    conn.commit()