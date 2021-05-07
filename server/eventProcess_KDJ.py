
import pandas as pd
import time
import numpy as np
import pickle

class KDJ:
    """
    根据KDJ策略进行择时，金叉买入，死叉卖出。
    """
    def __init__(self,data:pd.DataFrame,n:int=9):
        """
        param data:dataframe whose index is datetime and columns are ohlc.
        param n:选择多久做周期。
        """
        self.data=data
        self.n=n

    def getKDJ(self):
        """
        计算得到KDJ指标
        """
        data=self.data.copy()
        Hn = data['high'].rolling(self.n).max()
        Ln = data['low'].rolling(self.n).min()
        close=data['close']
        data['RSV']=100*(close-Ln)/(Hn-Ln)
        data=data.dropna(axis=0,how='any').reset_index(drop=True)
        data.loc[0, 'RSV'] = 50
        data.loc[0, 'K'] = 50
        data['K'] = data['RSV'].ewm(com=2).mean()
        data['D'] = data['K'].ewm(com=2).mean()
        if len(data)>2:
            K=data.loc[data.index[-2]:data.index[-1],['K']]
            D=data.loc[data.index[-2]:data.index[-1],['D']]
            return K,D
        else:
            K=pd.DataFrame()
            D=pd.DataFrame()
            return K,D

    def order(self):
        K,D=KDJ.getKDJ(self)
        data=self.data.copy()
        if K.empty==True and D.empty==True:
            return {'type': 'hold'}
        else:
            if K.loc[K.index[-2],'K']<D.loc[D.index[-2],'D']  and K.loc[K.index[-1],'K']>D.loc[D.index[-1],'D']:
                return {'type': 'buy', 'shares': 1}
            elif K.loc[K.index[-2],'K']>D.loc[D.index[-2],'D']  and K.loc[K.index[-1],'K']<D.loc[D.index[-1],'D']:
                return {'type': 'sell', 'shares': 1}
            else:
                return {'type': 'hold'}

def main():
    with open(r'C:\Users\ASUS\Documents\Algo_trading\Algo-trading\storage\storage_ohlcv.pkl', 'rb') as f:
        df = pickle.load(f)
    df=df.loc[df.index[0]:df.index[1],:]
    kdj=KDJ(df)
    order=kdj.order()

if __name__=="__main__":
    main()