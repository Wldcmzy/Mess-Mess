class AffixBase:

    class MethodException(Exception):
        def __init__(self, *args) -> None:
            super().__init__(*args)

    def __0_prefix_cycle_padding(string: str, length: int, pad: str) -> str:
        '''0: 以pad为前缀循环填充'''
        extra_string = (pad * ((length - len(string)) // len(pad) + 1))[ : (length - len(string))]
        return extra_string + string

    def __1_suffix_cycle_padding(string: str, length: int, pad: str) -> str:
        '''1: 以pad为前缀循环填充'''
        extra_string = (pad * ((length - len(string)) // len(pad) + 1))[ : length - len(string)]
        return string + extra_string

    METHODS = {
        0 : __0_prefix_cycle_padding,
        1 : __1_suffix_cycle_padding,
    }

    def __init__(self) -> None:
        pass

    def add_pad(self, string: str, length: int, pad: str = '0', method: int = 0) -> str:
        '''
        用字符串pad以method方法填充字符串string使其长度达到length
        
        参数string的长度不能大于leng

        string:
            初始字符串
        length:
            目标长度
        pad:
            填充字符串
        method:
            填充方法
        return:
            填充后的字符串
        '''
        assert len(string) <= length

        if method not in self.METHODS:
            raise self.MethodException(f'方法错误,不存在值"{method}"对应的方法')
        return self.METHODS[method](string, length, pad)
    
    def add_prefix(self, string: str, length: int, pad: str):
        '''填充前缀'''
        return self.add_pad(string, length, pad, 0)

    def add_suffix(self, string: str, length: int, pad: str):
        '''填充后缀'''
        return self.add_pad(string, length, pad, 1)
    
    def add_affix(self, string: str, length: int, pad: str):
        '''填充词缀(前后缀同时添加,前缀优先1字符长度)'''
        string = self.add_pad(string, (length + len(string)) // 2, pad, 1)
        string = self.add_pad(string, length, pad, 0)
        return string


class Affix_OnlyZeroExample(AffixBase):

    def __init__(self) -> None:
        super().__init__()

    def add_prefix(self, string: str, length: int, *args: None) -> str:
        '''填充前缀0'''
        return self.add_pad(string, length, '0', 0)

    def add_suffix(self, string: str, length: int, *args: None) -> str:
        '''填充后缀0'''
        return self.add_pad(string, length, '0', 1)
    
    def add_affix(self, string: str, length: int, *args: None) -> str:
        '''填充词缀0(前后缀同时添加,前缀优先1字符长度)'''
        string = self.add_pad(string, (length + len(string)) // 2, '0', 1)
        string = self.add_pad(string, length, '0', 0)
        return string

class Affix_ReverseExtraExample(AffixBase):

    def __2_reverse_prefix_cycle_padding(string: str, length: int, pad: str) -> str:
        '''2: 以pad的循环为前缀的反转进行填充'''
        extra_string = (pad * ((length - len(string)) // len(pad) + 1))[length - len(string) - 1 : : -1]
        return extra_string + string

    def __3_reverse_suffix_cycle_padding(string: str, length: int, pad: str) -> str:
        '''3: 以pad的循环为后缀的反转进行填充'''
        extra_string = (pad * ((length - len(string)) // len(pad) + 1))[length - len(string) - 1: : -1]
        return string + extra_string

    METHODS = AffixBase.METHODS | {
        2 : __2_reverse_prefix_cycle_padding,
        3 : __3_reverse_suffix_cycle_padding,
    }

    def __init__(self) -> None:
        super().__init__()
    
    def add_mirror_affix(self, string: str, length: int, pad: str) -> str:
        '''填充对称词缀(前后缀同时添加,前缀优先1字符长度)'''
        string = self.add_pad(string, (length + len(string)) // 2, pad, 3)
        string = self.add_pad(string, length, pad, 0)
        return string
