# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:24:24 2021

@author: Administrator
"""
import pandas as pd
import time


class Indicator:
    def __init__(self):
        self.indicatorRecord = {'ema5': [], 'ema10': []}
        self.recordLength = 0

    def calculate(self, dataMessage: pd.DataFrame):
        if dataMessage.shape[0] < 10:
            return 'data not enough'

        ema5 = (dataMessage.iloc[-5:, :])['close'].mean()
        ema10 = (dataMessage.iloc[-10:, :])['close'].mean()
        self.indicatorRecord['ema5'].append(ema5)
        self.indicatorRecord['ema10'].append(ema10)
        self.recordLength += 1


class Strategy:
    def __init__(self, Indicator: Indicator):
        self.Indicator = Indicator
        self.orderRecord = []

    def orderMake(self):
        currentTime = time.asctime(time.localtime(time.time()))
        if self.Indicator.recordLength < 2:
            return {'type': 'hold'}

        emaList5 = self.Indicator.indicatorRecord['ema5'][-2:]
        emaList10 = self.Indicator.indicatorRecord['ema10'][-2:]

        if emaList5[-1] > emaList10[-1] and emaList5[0] < emaList10[0]:
            return {'type': 'buy', 'shares': 1}
        elif emaList5[-1] < emaList10[-1] and emaList5[0] > emaList10[0]:
            return {'type': 'sell', 'shares': 1}
        else:
            return {'type': 'hold'}

meanIndicator = Indicator()
dualMeanStrategy = Strategy(meanIndicator)

