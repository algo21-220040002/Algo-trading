
import pandas as pd
import numpy as np
import datetime
from exchange.Exchange import Exchange
from exchange.CrawData import CrawData
from server.market_adapter import MarketAdapter
from server.eventProcess import  meanIndicator,dualMeanStrategy
import time
from indicatorCalculator.IndicatorCalculator import IndicatorCalculator
from application.application import application

def load_obj(name):
    """
    :parameter
    :param name:The name of dictionary.
    :return: The dictionary.
    """
    with open(r'./' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


class BackTest:
    """BackTest
    根据历史交易数据进行回测
    """
    def __init__(self,
                 data:pd.DataFrame,
                 bar_time:str):
        """
        parameter
        param data:即历史交易信息，it's dataframe whose index is datetime and columns are ['close','high','low','close']
        param bar_time:提前设定好一个bar的时间，这里要求是时间加"s"并以str格式传入
        """
        self.data=data
        self.bar_time=bar_time


    def backtest(self):
        app1 = application()
        app1.gui()
        df_account=pd.DataFrame()
        exchange=Exchange(self.data)
        for date in self.data.index:
            print(date)
            open=exchange.get_open_price(date)
            high=exchange.get_high_price(date)
            low=exchange.get_low_price(date)
            close=exchange.get_close_price(date)
            market_adapter=MarketAdapter(open,high,low,close,date)
            df=market_adapter.storage()[-30:]
            meanIndicator.calculate(df)
            order = dualMeanStrategy.orderMake()
            exchange.trade_l(order,date)  #传入交易所订单并进行交易
            # exchange.trade_ls(order,date)
            Total_banlance=exchange.get_account_info()['Total_banlance']
            bitcoin_num=exchange.get_account_info()['Bitcoin_num']

            if date<=self.data.index[10]:
                df_account.loc[date, 'close'] = Total_banlance
                df_account.loc[date, 'return'] = df_account['close'].pct_change()[-1]
                app1.plot(date,bitcoin_num, Total_banlance, 0,
                          0, 0,0)
            else:
                df_account.loc[date, 'close'] = Total_banlance
                df_account.loc[date, 'return'] = df_account['close'].pct_change()[-1]
                df_account = df_account.dropna()
                indicator = IndicatorCalculator(df_account, int(self.bar_time.strip('s')))
                app1.plot(date,bitcoin_num, Total_banlance, indicator.cum_Return(),
                          indicator.hourSharpratio(),indicator.max_Drawdown(),indicator.hour_Return())
                print('hour return', indicator.hour_Return())
                print('cumulative return', indicator.cum_Return())
                print('max drawdown', indicator.max_Drawdown())
                print('hour sharp ratio', indicator.hourSharpratio())
            print('total banlance',Total_banlance)
            print('number of bitcoin',bitcoin_num)

            print("")