# coding=utf-8

from logging import getLogger
logger = getLogger(__name__)

from .base import MarketBase

class MirrorMarket (MarketBase):

    def __init__ (self, *args):
        super().__init__(*args)

    def set_ohlcv (self, ohlcv):
        for col, candles in ohlcv.items():
            self.data[col].clear()
            self.data[col] += candles

    def update_ohlcv2 (self, ohlcv2):
        for col, candles in ohlcv2.items():
            self.data[col].pop(0)
            self.data[col][-2] = candles[0]
            self.data[col][-1] = candles[1]
