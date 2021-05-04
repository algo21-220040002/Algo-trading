
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
import time
import requests
import json

class CrawData:
    """CrawData
    It's used to craw trading data of Bitcoin from the website of bittrex.
    """
    def __init__(self,
                 bar_time: str = "30s",
                 url:str='https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=usdt-btc',
                 timeout:float=3):
        """
        parameters
        param bar_time:The bar time of ohlc you want.
        param url:The url of the website.
        param timeout:The timeout of the request function.
        """
        self.url=url
        self.bar_time=bar_time
        self.timeout=timeout

    def craw(self)->dict:
        """
        This function is used to craw the text from the website.
        """
        label = True
        while label:
            try:
                result = json.loads(requests.get(self.url,timeout = self.timeout).text)
                label = False
                return result
            except:
                label = True
                time.sleep(0.5)

    def get_datetime(x:str)->pd.Timestamp:
        """
        This function is used to transform the string into timestamp.
        parameters
        param x:The string of the time.
        return: The timestamp of the time.
        """
        x=x.replace("T"," ")
        try:
            return datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S.%f" )
        except:
            try:
                return datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S" )
            except:
                try:
                    return datetime.datetime.strptime(x,"%Y-%m-%d %H:%M" )
                except:
                    print('出现问题')

    def integrate_data(self)->pd.DataFrame:
        """
        This function is used to get the ohlc data.
        return: A dataframe whose index is the timestamp and columns are ['open','high','low','close','volume'].
        """
        result=CrawData.craw(self)
        orderflow=result['result']
        data=pd.DataFrame()
        for order in orderflow:
            data.loc[order['TimeStamp'],'price']=order['Price']
            data.loc[order['TimeStamp'],'quantity']=order['Quantity']
        data['datetime']=data.index
        data['datetime']=data['datetime'].apply(lambda x:CrawData.get_datetime(x))
        data=data.set_index('datetime')
        df=data['price'].resample(self.bar_time).ohlc()
        df = df.fillna(method='ffill')
        df['volume'] = data['quantity'].resample(self.bar_time).sum()
        df = df.fillna(value=0)
        df=df.loc[df.index[1]:df.index[-2], :]
        return df

def main():
    url='https://api.bittrex.com/api/v1.1/public/getmarkethistory?market=usdt-btc'
    craw=CrawData("10s",url,3)
    df=craw.integrate_data()
    print(df)

if __name__=="__main__":
    main()



