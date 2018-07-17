import tushare as ts
import sys
import io
import pandas as pd
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
class realtime:
    def __init__(self,code):
        self.df = ts.get_realtime_quotes(code)
    def real(self):
        #返回实时数据
        return self.df[['code','name','price','bid','ask','volume','amount','time']]
