"""
@2021-04-18
"""
import pandas as pd
import numpy as np
import datetime
import pickle

def save_obj(path:str,obj:dict, name:str):
    """
    :parameter
    :parm path:The path the obj you want to save.
    :param obj:The dictionary.
    :param name:The name of the dictionary you want to store.
    """
    with open(path+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(path:str,name):
    """
    :parameter
    :param path:The path the pkl stores.
    :param name:The name of dictionary.
    :return: The dictionary.
    """
    with open(path+ name + '.pkl', 'rb') as f:
        return pickle.load(f)

class MarketAdapter:
    """MarketAdapter
    MarketAdapter is used to convert the format of the data into the format the system can understand.
    """

    def __init__(self,
                 open:float,
                 high:float,
                 low:float,
                 close:float,
                 current_time:pd.Timestamp,
                 if_init:bool=False):
        """
        parameter
        param open:The open price from the exchange.
        param high:The high price from the exchange.
        param low: The low price from the exchange.
        param close: The close price from the exchange.
        param current_time: The current time.
        """
        self.open=open
        self.high=high
        self.low=low
        self.close=close
        self.current_time=current_time
        self.if_init=if_init

        if self.if_init==True:
            path = r'../storage//'
            data=pd.DataFrame()
            save_obj(path, data, 'storage_ohlcv')


    def combine(self)->pd.DataFrame:
        """
        return: The index of the dataframe is the current time, the columns include "open,high,low,close".
        """
        data=pd.DataFrame(columns=['open','high','low','close'])
        data.loc[self.current_time,'open']=self.open
        data.loc[self.current_time,'high']=self.high
        data.loc[self.current_time,'low']=self.low
        data.loc[self.current_time,'close']=self.close
        return data

    def storage(self):
        """
        This function merge the ohlc data and then save it.
        """
        path=r'../storage//'
        data=MarketAdapter.combine(self)
        df=load_obj(path,'storage_ohlcv')
        data=pd.concat([df, data], axis=0)
        save_obj(path,data,'storage_ohlcv')
        return data

