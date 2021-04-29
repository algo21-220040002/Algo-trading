# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:10:43 2021

@author: Administrator
"""
import pandas as pd
from eventProcess import meanIndicator,dualMeanStrategy

data = pd.read_csv('bitcoin.csv')

for i in range(data.shape[0]):
    currentGetData = data.iloc[:i,:]
    
    meanIndicator.calculate(currentGetData)
    order = dualMeanStrategy.orderMake()
    
    print(order)