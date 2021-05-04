import pandas as pd
import numpy as np
from scipy.stats.mstats import gmean
import math
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
plt.rc("font",family='YouYuan')

class IndicatorCalculator:
    """
     A IndicatorCalculator is used to calculate the indicator of the financial data,including
     annualStd,sharpeRatio,maxDrawdown,calmarRatio,annualDownsideStd,sortinoRatio,skewness,
     kurtosis,averageTop5MaxDrawdown,annualReturn,cumReturn
    """

    def __init__(self,
                 df:pd.DataFrame,
                 bar_time:int):
        """
        param df:df from dataframe,index is datetime and columns are close and return.
        param bar_time:The bar time, here it's the num of seconds.
        """
        self.df=df
        self.bar_time=bar_time

    def hour_Return(self):
        """
        return: The hour return.
        """
        hourReturn = gmean(self.df['return'] + 1) **(3600/self.bar_time) - 1  # 得到年化收益率
        return hourReturn

    def hour_Std(self):
        """
        :return: The hour standard deviation.
        """
        bar_timeStd = self.df['return'].std()  # 得到bar波动率
        hourStd = bar_timeStd* math.sqrt(3600/self.bar_time)  # 得到年化波动率
        return hourStd

    def cum_Return(self):
        """
        :return: The cumulative return.
        """
        cumReturn=(self.df.loc[self.df.index[-1],'close']-self.df.loc[self.df.index[0],'close'])/self.df.loc[self.df.index[0],'close']
        return cumReturn

    def max_Drawdown(self):
        """
        :return: Max drawdown of the financial series.
        """
        roll_max = self.df['close'].expanding().max()
        maxDrawdown = -1 * np.min(self.df['close'] / roll_max - 1)  # 计算得到最大回撤
        return maxDrawdown

    def hourSharpratio(self):
        """
        return :The hour sharp ratio.
        """
        hourReturn=IndicatorCalculator.hour_Return(self)
        hourStd=IndicatorCalculator.hour_Std(self)
        sharpRatio=hourReturn/hourStd
        return sharpRatio