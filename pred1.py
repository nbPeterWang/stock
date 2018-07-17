import pandas as pd
import numpy as np
from sklearn.svm import SVR
class pred1:
    #初始化数据
    def __init__(self,code):
        sp = pd.read_csv('d:/AnaStuff/stock/clean/%s.csv' % code)
        clf = SVR(kernel='linear')
        X_train = sp[:-200]
        y_train = sp['close'].shift(-1)[:-200]
        self.model = clf.fit(X_train, y_train)
        self.X_test = sp[-1:]
    #预测函数
    def predict1(self):
        return self.model.predict(self.X_test)[0]


   
