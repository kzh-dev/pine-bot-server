# coding=utf-8

class Broker (object):

    def __init__ (self, market='MARKET', symbol='SYMBOL'):
        self.market = market
        self.symbol = symbol

    def entry (self, oid, isLong, **kwargs):
        pass
