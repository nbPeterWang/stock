import datetime
import tushare as ts
import pandas as pd
import numpy as np
#获取昨天日期
def getYesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return str(yesterday)
#获取数据
def getdata(code,date):
    yesterday = getYesterday()
    df = ts.get_k_data('%s'%code, start=date, end=yesterday)
    print(df)
    df.to_csv('d:/AnaStuff/stock/%s.csv'%code, columns=['code','date','open', 'high', 'close', 'low'],index=False,sep=',')
#处理数据
def processData(code):
    df = pd.read_csv('d:/AnaStuff/stock/%s.csv' % code)

    for i in range(1, 21, 1):
        df.loc[:, 'Close Minus ' + str(i)] = df['close'].shift(i)
    # 列名条件过滤，只要Close,及包含 有Close Minus字符串的列
    sp20 = df[[x for x in df.columns if 'Close Minus' in x or x == 'close']].iloc[20:, ]
    # 将列的顺序颠倒,从左到右就是最早时间到最晚时间
    sp20 = sp20.iloc[:, ::-1]
    sp20.to_csv('./clean/%s.csv'%code,index=False,sep=',')