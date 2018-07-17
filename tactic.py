import tushare as ts
import pandas as pd
import numpy as np
import os
from sklearn.svm import SVR
class tactic:
    code = None
    spy = None

    # 交易策略1：每日交易策略，每日回报率=（当前的收盘价 - 上一交易日的收盘价）/上一交易日收盘价
    daily_rtn = None
    # 日间交易：收益 = 当天收盘价 - 当天开盘价
    id_rtn = None
    # 隔夜交易策略：隔夜交易收益率 = （当天开盘价 - 上一天收盘价）/上一天收盘价
    on_rtn = None

    model = None
    def __init__(self,code):
        self.code = code
        spy = pd.read_csv('d:/AnaStuff/stock/%s.csv' % code)
        self.id_rtn = ((spy['close'] - spy['open'])/spy['open'])*100
        self.on_rtn = ((spy['open'] - spy['close'].shift(1))/spy['close'].shift(1))*100
        self.daily_rtn = ((spy['close'] - spy['close'].shift(1))/spy['close'].shift(1))*100
       #长期持有
        self.long1 = ((spy['close'].iloc[-1] - spy['open'].iloc[1])/ spy['open'].iloc[1])*100
        self.longrtn = pd.DataFrame([self.long1])
        #自定义策略
        self.own = ((spy['close'] - spy['close'].shift(100))/spy['close'].shift(10))*100

    @staticmethod
    def get_stats(s, n=252):
        s = s.dropna()
    #盈利次数：获取每日收益率大于0的所有数据，并计算总数
        wins = len(s[s>0])
    #亏损次数：获取每日收益率小于0的所有数据，并计算总数
        losses = len(s[s<0])
    #盈亏平衡次数：获取每日收益率等于0的所有数据，并计算总数
        evens = len(s[s==0])
    #盈利平均值，round四舍五入，3为小数位数
        mean_w = round(s[s>0].mean(), 3)
    #亏损平均值
        mean_l = round(s[s<0].mean(), 3)
    #盈利亏损比例
        win_r = round(wins/losses, 3)
    #平均收益
        mean_trd = round(s.mean(), 3)
    #标准差
        sd = round(np.std(s), 3)
    #最大亏损
        max_l = round(s.min(), 3)
    #最大盈利
        max_w = round(s.max(), 3)
    #夏普比率：代表投资人每多承担一分风险，可以拿到几分超额报酬；若为正值，代表基金报酬率高过波动风险；若为负值，代表基金操作风险大过于报酬率。
    #每个投资组合都可以计算Sharpe Ratio,即投资回报与多冒风险的比例，这个比例越高，投资组合越佳。
    #夏普比率 = （ E(Rp) - Rf ）/ σp  其中E(Rp)：投资组合预期报酬率 Rf：无风险利率 σp：投资组合的标准差
    #夏普比率 = （平均收益/标准差）* n=252的平方根 , 最后四舍五入
    #注：年波动率等于收益率的标准差除以其均值，再除以交易日倒数的平方根，通常交易日取252 天。
        sharpe_r = round((s.mean()/np.std(s))*np.sqrt(n), 4)
    #交易次数
        cnt = len(s)
        return '''交易次数: %s
盈利次数: %s
亏损次数: %s
盈亏平衡次数: %s
盈利亏损比例: %s
盈利平均值: %s
亏损平均值: %s
平均收益: %s
标准差: %s
最大亏损: %s
最大盈利: %s
夏普比率: %s
''' % (cnt, wins, losses, evens, win_r, mean_w, mean_l, mean_trd, sd, max_l, max_w, sharpe_r)
    #返回各个策略的方法
    def get_stats_daily_rtn(self):
        return self.get_stats(self.daily_rtn)

    def get_stats_id_rtn(self):
        return self.get_stats(self.id_rtn)

    def get_stats_on_rtn(self):
        return self.get_stats(self.on_rtn)
    def get_stats_on_own(self):
        return self.get_stats(self.own)
    def get_stats_on_long(self):
        return self.get_stats(self.longrtn)

