
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
from exchange.Exchange import Exchange
from exchange.CrawData import CrawData
from server.market_adapter import MarketAdapter
from server.eventProcess_ma import  meanIndicator,dualMeanStrategy
from server.eventProcess_KDJ import  KDJ
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


class RealSimulation:
    """RealSimulation
    开展实盘模拟，爬下实时数据并传入exchange，进行模拟交易。
    """
    def __init__(self,
                 bar_time:str='30s',
                 strategy:str='ma'):
        """
        parameter
        param bar_time:提前设定好一个bar的时间，这里要求是时间加"s"并以str格式传入
        """
        self.bar_time=bar_time
        self.strategy=strategy


    def simulation(self):
        """
        开展实盘模拟
        """
        app1 = application()
        app1.gui()
        df_account = pd.DataFrame()
        df = pd.DataFrame()
        crawdata = CrawData(self.bar_time)
        start_time=crawdata.integrate_data().index[1].strftime('%Y-%m-%d %H:%M:%S')
        for t in pd.date_range(start=start_time, periods=300, freq=self.bar_time):
            print(t+timedelta(hours=8))
            if t == pd.Timestamp(start_time):
                data = crawdata.integrate_data()
                df = pd.concat([df, data])
                df = df[~df.index.duplicated(keep='first')]
                exchange = Exchange(df, True)
            else:
                while df.index[-1] < t:
                    data = crawdata.integrate_data()
                    df = pd.concat([df, data])
                    df = df[~df.index.duplicated(keep='first')]
                    time.sleep(int(self.bar_time.strip('s')))
                exchange = Exchange(df, False)
            open = exchange.get_open_price(t)
            high = exchange.get_high_price(t)
            low = exchange.get_low_price(t)
            close = exchange.get_close_price(t)
            if t == pd.Timestamp(start_time):
                market_adapter = MarketAdapter(open, high, low, close, t, True)
            else:
                market_adapter = MarketAdapter(open, high, low, close, t, False)
            Df = market_adapter.storage()
            if self.strategy=='ma':
                meanIndicator.calculate(Df)
                order = dualMeanStrategy.orderMake()
            elif self.strategy=='KDJ':
                kdj = KDJ(df)
                order = kdj.order()
            exchange.trade_l(order, t)  # 传入交易所订单并进行交易
            print(order)

            Total_banlance = exchange.get_account_info()['Total_banlance']
            bitcoin_num = exchange.get_account_info()['Bitcoin_num']
            if t<=pd.date_range(start=start_time, periods=300, freq=self.bar_time)[10]:
                df_account.loc[t, 'close'] = Total_banlance
                df_account.loc[t, 'return'] = df_account['close'].pct_change()[-1]
                app1.plot(t+timedelta(hours=8),bitcoin_num, Total_banlance, 0,
                          0, 0,0)
            else:
                df_account.loc[t, 'close'] = Total_banlance
                df_account.loc[t, 'return'] = df_account['close'].pct_change()[-1]
                df_account = df_account.dropna()
                indicator = IndicatorCalculator(df_account, int(self.bar_time.strip('s')))
                app1.plot(t+timedelta(hours=8),bitcoin_num, Total_banlance, indicator.cum_Return(),
                          indicator.hourSharpratio(), indicator.max_Drawdown(),indicator.hour_Return())
                print('hour return', indicator.hour_Return())
                print('cumulative return', indicator.cum_Return())
                print('max drawdown', indicator.max_Drawdown())
                print('hour sharp ratio', indicator.hourSharpratio())
            print('total banlance', Total_banlance)
            print('number of bitcoin', bitcoin_num)
            print('')
