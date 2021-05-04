
import pandas as pd
import numpy as np
import datetime
from exchange.Exchange import Exchange
from exchange.CrawData import CrawData
from server.market_adapter import MarketAdapter
from server.eventProcess import  meanIndicator,dualMeanStrategy
from exchange.BackTest import BackTest
from exchange.RealSimulation import RealSimulation


def main():
    # data=pd.read_excel(r'./bitcoin.xlsx',index_col=0)
    # backtest=BackTest(data,"60s")
    # backtest.backtest()
    realsimulation=RealSimulation("20s")
    realsimulation.simulation()


if __name__=="__main__":
    main()

