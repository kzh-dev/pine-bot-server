# coding=utf-8

from datetime import datetime
from collections import OrderedDict
import pandas as pd
import calendar
import requests

from .base import Market

class BitMexMarket (Market):

    def __init__ (self, symbol, resolution):
        super().__init__('BITMEX', symbol, resolution)
        count = 500

        now = datetime.utcnow()
        unixtime = calendar.timegm(now.utctimetuple())

        since = unixtime - resolution * 60 * 256
        if resolution >= 1440:
            resolution = "{}D".format(resolution / 1440)

        param = {"period": resolution, "from": since, "to": unixtime}
        url   = "https://www.bitmex.com/api/udf/history?symbol=XBTUSD&" + \
                "resolution={period}&from={from}&to={to}".format(**param)

        self.data = requests.get(url).json()

    def open (self):
        return self.data['o']
    def high (self):
        return self.data['h']
    def low (self):
        return self.data['l']
    def close (self):
        return self.data['c']
    def volume (self):
        return self.data['v']

    def ohlcv_df (self):
        data = self.data
        return pd.DataFrame(OrderedDict(
                        {"unixtime":data["t"], "open":data["o"], "high":data["h"],
                         "low":data["l"], "close":data["c"], "volume":data["v"]}))
