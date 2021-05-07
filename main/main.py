
import pandas as pd
import numpy as np
import datetime
from exchange.Exchange import Exchange
from exchange.CrawData import CrawData
from server.market_adapter import MarketAdapter
from exchange.BackTest import BackTest
from exchange.RealSimulation import RealSimulation


def main():
    #运行这一段即历史数据回测,历史数据已经就位
    # data=pd.read_excel(r'./bitcoin.xlsx',index_col=0)
    # backtest=BackTest(data,"60s")
    # backtest.backtest()

    #运行这一段即模拟实盘测算，用户只需设定bar time即可，格式即数字加"s"的str格式，这里表示多少秒，只允许用秒做单位
    realsimulation=RealSimulation("10s")
    realsimulation.simulation()


if __name__=="__main__":
    main()

