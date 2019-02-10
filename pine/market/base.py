# coding=utf-8

class Market (object):

    def __init__ (self, market='MARKET', symbol='SYMBOL', resolution=240):
        self.market = market
        self.symbol = symbol
        self.resolution = resolution

    def size (self):
        return 1
    def timestamp (self):
        return [0]
    def close (self):
        return [0.0]
    def open (self):
        return [0.0]
    def high (self):
        return [0.0]
    def low (self):
        return [0.0]

    def period (self):
        return 'DD'
    def tickerid (self):
        return ':'.join((self.market, self.symbol))

    # float(ms)
    def bartimestamp (self):
        import datetime
        import math
        unixtime = datetime.datetime.utcnow().timestamp()
        # round by 4h
        step = 60 * self.resolution
        ts = math.floor(unixtime / step) * step
        return ts * 1000.0
