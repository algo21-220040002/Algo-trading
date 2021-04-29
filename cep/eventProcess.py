# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:24:24 2021

@author: Administrator
"""
import pandas as pd
import time
class Indicator:
    def __init__(self):
        self.indicatorRecord = {'ema12':[],'ema26':[]}
        self.recordLength = 0
    
    def calculate(self, dataMessage:pd.DataFrame):
        if dataMessage.shape[0] < 26:
            return 'data not enough'
        
        ema12 = (dataMessage.iloc[-12:,:])['open'].mean()
        ema26 = (dataMessage.iloc[-26:,:])['open'].mean()
        self.indicatorRecord['ema12'].append(ema12)
        self.indicatorRecord['ema26'].append(ema26)
        self.recordLength += 1

class Strategy:
    def __init__(self,Indicator:Indicator):
        self.Indicator = Indicator
        self.orderRecord = []
    
    def orderMake(self):
        currentTime = time.asctime( time.localtime(time.time()))
        if self.Indicator.recordLength < 2:
            return {'time':currentTime}
        
        emaList12 = self.Indicator.indicatorRecord['ema12'][-2:]
        emaList26 = self.Indicator.indicatorRecord['ema26'][-2:]
        
        if emaList12[-1] > emaList26[-1] and emaList12[0] < emaList26[0]:
            return {'time':currentTime,'buy':1}
        elif emaList12[-1] < emaList26[-1] and emaList12[0] > emaList26[0]:
            return {'time':currentTime,'sell':1}
        else:
            return {'time':currentTime}

meanIndicator = Indicator()
dualMeanStrategy = Strategy(meanIndicator)