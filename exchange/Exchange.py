"""
@2021-04-18
"""
import pandas as pd
import numpy as np
import pickle
import os
from pathlib import *
import datetime

def save_obj(obj:dict, name:str):
    """
    :parameter
    :param obj:The dictionary.
    :param name:The name of the dictionary you want to store.
    """
    with open(r'./'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    """
    :parameter
    :param name:The name of dictionary.
    :return: The dictionary.
    """
    with open(r'./' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

class Exchange:
    """Exchange
    It's simulated exchange of bitcoin.
    """
    def __init__(self,
                 data:pd.DataFrame,
                 if_init_account_info:bool=True,
                 account_id: float='12345',
                 init_cash:float=80000,
                 commision: float = 0.00025,
                 slippage_rate: float = 0.00005):
        """
        :parameter
        :param data:The OHLC data of bitcoin.
        :param account_id: The account id.
        :param init_cash: The initial cash.
        :param commision: The commision of the trading.
        :param slippage_rate: The slippage rate.
        """
        self.data=data
        self.account_id=account_id
        self.init_cash=init_cash
        self.commision=commision
        self.slippage_rate=slippage_rate

        if os.path.exists(str(account_id)+'.pkl')==False:
            print('You do not have an account,we will help you open the account,the initial cash is '+str(self.init_cash))
            print('please notice that the account id is '+str(account_id))
            dic_account={}
            dic_account['Bitcoin_num']=0                                     # The number of bitcoin in the account.
            dic_account['Bitcoin_value']=0                                   # The market value of the bitcoin in the account.
            dic_account['cash'] =self.init_cash                              # The cash in the account.
            dic_account['Total_banlance']=self.init_cash
            save_obj(dic_account, str(account_id))
        elif if_init_account_info==True:
            print('We have initialized your account information in the exchange')
            dic_account = {}
            dic_account['Bitcoin_num'] = 0
            dic_account['Bitcoin_value'] = 0
            dic_account['cash']=self.init_cash
            dic_account['Total_banlance'] = self.init_cash
            save_obj(dic_account, str(account_id))

    def get_open_price(self,time:pd.Timestamp)->float:
        """
        :param time: The time.
        :return: The open price.
        """
        open_price=self.data.loc[time,'open']
        return open_price

    def get_high_price(self,time:pd.Timestamp):
        """
        :param time: The time.
        :return: The high price.
        """
        high_price=self.data.loc[time,'high']
        return high_price

    def get_low_price(self,time:pd.Timestamp):
        """
        :param time: The time.
        :return: The low price.
        """
        low_price=self.data.loc[time,'low']
        return low_price

    def get_close_price(self,time:pd.Timestamp):
        """
        :param time: The time.
        :return: The close price in the time.
        """
        close_price=self.data.loc[time,'close']
        return close_price

    def update_account_info(self,time:pd.Timestamp):
        """
        To update the account information each time.
        :param time: The time.
        """
        dic_account = load_obj(str(self.account_id))
        close_price=Exchange.get_close_price(self,time)
        dic_account['Bitcoin_value']=dic_account['Bitcoin_num']*close_price
        dic_account['Total_banlance']=dic_account['cash']+dic_account['Bitcoin_value']
        save_obj(dic_account, str(self.account_id))

    def trade_l(self,order:dict,time:pd.Timestamp):
        """
        只允许做多
        :param order: It's a dictionary that includes the type(buy or sell),num of shares.
        """
        dic_account = load_obj(str(self.account_id))
        if order['type']=='buy':
            close_price=Exchange.get_close_price(self,time)
            if dic_account['cash']>=order['shares']*close_price*(1+self.commision+self.slippage_rate):
                dic_account['Bitcoin_num']=dic_account['Bitcoin_num']+order['shares']
                dic_account['cash'] = dic_account['cash'] -order['shares']*close_price*(1+self.commision+self.slippage_rate)
                dic_account['Bitcoin_value']=dic_account['Bitcoin_num']*close_price
                dic_account['Total_banlance']=dic_account['cash']+dic_account['Bitcoin_value']
            else:
                print('You do not have enough cash to buy'+str(order['shares'])+'shares bitcoin')
            save_obj(dic_account, str(self.account_id))
        elif order['type']=='sell':
            close_price=Exchange.get_close_price(self,time)
            if dic_account['Bitcoin_num']>=order['shares']:
                dic_account['Bitcoin_num'] = dic_account['Bitcoin_num'] - order['shares']
                dic_account['cash']=dic_account['cash']+order['shares']*close_price*(1-self.commision-self.slippage_rate)
                dic_account['Bitcoin_value']=dic_account['Bitcoin_num']*close_price
                dic_account['Total_banlance']=dic_account['cash']+dic_account['Bitcoin_value']
            else:
                print('You do not have enough bitcoin to sell')
            save_obj(dic_account, str(self.account_id))
        elif order['type']=="hold":
            Exchange.update_account_info(self,time)

    def trade_ls(self,order:dict,time:pd.Timestamp):
        """
        允许做多和做空
        :param order: It's a dictionary that includes the type(buy or sell),num of shares.
        """
        dic_account = load_obj(str(self.account_id))
        if order['type']=='buy':
            close_price=Exchange.get_close_price(self,time)
            dic_account['Bitcoin_num']=dic_account['Bitcoin_num']+order['shares']
            dic_account['cash'] = dic_account['cash'] -order['shares']*close_price*(1+self.commision+self.slippage_rate)
            dic_account['Bitcoin_value']=dic_account['Bitcoin_num']*close_price
            dic_account['Total_banlance']=dic_account['cash']+dic_account['Bitcoin_value']
            save_obj(dic_account, str(self.account_id))
        elif order['type']=='sell':
            close_price=Exchange.get_close_price(self,time)
            dic_account['Bitcoin_num'] = dic_account['Bitcoin_num'] - order['shares']
            dic_account['cash']=dic_account['cash']+order['shares']*close_price*(1-self.commision-self.slippage_rate)
            dic_account['Bitcoin_value']=dic_account['Bitcoin_num']*close_price
            dic_account['Total_banlance']=dic_account['cash']+dic_account['Bitcoin_value']
            save_obj(dic_account, str(self.account_id))
        elif order['type']=="hold":
            Exchange.update_account_info(self,time)


    def get_account_info(self):
        """
        This funtion is used to get the account information.
        """
        dic_account = load_obj(str(self.account_id))
        return dic_account

