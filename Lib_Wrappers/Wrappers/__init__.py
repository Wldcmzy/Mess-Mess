import time
import os

class Easylogger:
    def __init__(self, path: str = './', filename = 'EasyLOG.log') -> None:
        self.path = path
        self.filename = filename
        self.makelog('MyEasylogger类被实例化', 'MyEasylogger', False)

    def makelog(self, data: str, tag: str = 'default', ifprint: bool = True) -> None:
        if ifprint:
            print(data)
        ifexist = os.path.exists(self.filename)
        with open(self.path + self.filename, 'a+') as f:
            if not ifexist:
                f.write(f'==> {str(time.localtime()[ : 6])} | [MyEasylogger] 日志建立\n')
            f.write(f'==> {str(time.localtime()[ : 6])} | [{tag}] {data}\n')

    def log(self, data: str, ifprint = True):
        self.makelog(data, 'log', ifprint)

    def debug(self, data: str, ifprint = True):
        self.makelog(data, 'debug', ifprint)

    def error(self, data: str, ifprint = True):
        self.makelog(data, 'error', ifprint)
logger = Easylogger()

def try_except_ensure(func):
    def _(*args):
        try:
            return func(*args)
        except Exception as e:
            def __(e : Exception, *args) -> None: 
                logger.error(str(type(e)) + '|' + str(e))
            return __(e, *args)
    return _