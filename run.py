from pandas_datareader import data as pdr
from flask import Flask, render_template, request,json,make_response
from flask import jsonify
import tushare as ts
import sys
import io
import data
import pred1
import tactic
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#获取实时信息
@app.route('/getreal', methods=['GET'])
def getreal():
    cod = request.values.get("a")
    cod1=cod.split(',')
    df1 = ts.get_realtime_quotes(cod1)
    df2=df1[['code','name','price','bid','ask','volume','amount','time']]
    return df2.to_json(orient='records',force_ascii=False)
#导出数据
@app.route('/exportdata', methods=['GET'])
def exportdata():
    code = request.values.get("current_code")
    d1=request.values.get("b1")
    data.getdata(code,d1)
    return "导出数据成功"
#加工数据
@app.route('/cleandata')
def cleandata():
    code = request.values.get("current_code")
    data.processData(code)
    return "加工数据成功"
#预测
@app.route('/myform1', methods=['GET'])
def predi():
    code = request.values.get("current_code")
    p1=pred1.pred1(code)
    p2=p1.predict1()
    return str(p2)
#实现策略比较
@app.route('/gettac', methods=['GET'])
def compare():
    code = request.values.get("current_code")
    statistics = dict()
    t = tactic.tactic(code)
    statistics['daily'] = t.get_stats_daily_rtn()
    statistics['id'] = t.get_stats_id_rtn()
    statistics['on'] = t.get_stats_on_rtn()
    statistics['own'] = t.get_stats_on_own()
    statistics['long'] = t.get_stats_on_long()
    return make_response(jsonify(statistics))
if __name__ == '__main__':
    app.run()
