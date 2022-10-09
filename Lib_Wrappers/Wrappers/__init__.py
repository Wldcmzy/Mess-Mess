import re
import logging

__handlerF = logging.FileHandler('Easylog.log')
__handlerF.setLevel(logging.DEBUG)
__handlerC = logging.StreamHandler()
__handlerC.setLevel(logging.INFO)
__formatter = logging.Formatter('%(asctime)s <%(levelname)s>: %(message)s')
__handlerF.setFormatter(__formatter)
__handlerC.setFormatter(__formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(__handlerF)
logger.addHandler(__handlerC)


def try_except_ensure(func):
    def _(*args):
        try:
            return func(*args)
        except Exception as e:
            def __(e : Exception, *args) -> None: 
                logger.error(str(type(e)) + '|' + str(e))
            return __(e, *args)
    return _

def replace_invalid_element_in_windows_path(path_str: str, to_replace: str = '') -> str:
    return re.sub(r'[\\|/|:|*|?|\"|<|>|\|]', to_replace, path_str)

def remove_invalid_element_in_windows_path(path_str: str) -> str:
    return replace_invalid_element_in_windows_path(path_str)