# coding=utf-8

MARKETS = {}
def register_market (market, cls):
    MARKETS[market] = cls

class MarketError (Exception):
    pass

class L(list):

    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([None]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)

    def rindex (self, v):
        i = len(self) - 1
        while i >= 0:
            if self[i] == v:
                return i
            i -= 1
        return 0

def empty_udf ():
    return {'t':L(), 'o':L(), 'c':L(), 'h':L(), 'l':L(), 'v':L()}

import calendar
from datetime import datetime
def utcunixtime ():
    now = datetime.utcnow()
    return calendar.timegm(now.utctimetuple())

def resolution_to_str (resolution):
    if resolution < 60:
        return str(resolution)
    if resolution < 60*24:
        n, u = int(resolution / 60), 'H'
    else:
        n, u = int(resolution / 60 / 24), 'D'
    if n == 1:
        n = ''
    return str(n)+u
    
def str_to_resolution (string):
    try:
        return int(string)
    except:
        pass
    if string[-1] == 'H':
        n = string[0:-1]
        u = 60
    elif string[-1] == 'D':
        n = string[0:-1]
        u = 60 * 24
    else:
        raise PineError("invalid resolution: {}".format(string))

    if not bool(n):
        n = 1
    return n * u

class MarketBase (object):

    RESOLUTIONS = (
        1,
        3,
        5,
        15,
        30,
        60 * 1,
        60 * 2,
        60 * 4,
        60 * 6,
        60 * 12,
        60 * 24,
    )

    def __init__ (self, market='MARKET', symbol='SYMBOL', resolution=240):
        self.market = market
        self.symbol = symbol
        self.resolution = resolution
        self.data = empty_udf()

    def ohlcv_df (self):
        import pandas as pd
        from collections import OrderedDict
        data = self.data
        return pd.DataFrame(OrderedDict(
                        {"unixtime":data["t"], "open":data["o"], "high":data["h"],
                         "low":data["l"], "close":data["c"], "volume":data["v"]}))
    def rows_to_udf (self, rows):
        import numpy
        cols = numpy.array(rows).T
        udf = empty_udf()
        udf['t'] += [int(t) for t in cols[0]]
        udf['o'] += [t for t in cols[1]]
        udf['h'] += [t for t in cols[2]]
        udf['l'] += [t for t in cols[3]]
        udf['c'] += [t for t in cols[4]]
        udf['v'] += [t for t in cols[5]]
        return udf

    def size (self):
        return len(self.data['t'])
    def timestamp (self):
        return self.data['t']

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

    def mintick (self):
        raise NotImplementedError

    def period (self):
        return str_to_resolution(self.resolution)
    def tickerid (self):
        return ':'.join((self.market, self.symbol))
    def mintick (self):
        raise NotImplementedError

    # float(ms)
    def bartimestamp (self):
        import datetime
        import math
        unixtime = utcunixtime
        step = 60 * self.resolution
        ts = math.floor(unixtime / step) * step
        return ts * 1000.0


class Market (MarketBase):

    def __init__ (self, market='MARKET', symbol='SYMBOL', resolution=240):
        super().__init__(market, symbol, resolution)
        for k in self.data.keys():
            self.data[k].append(0)

    def mintick (self):
        return 0.0
