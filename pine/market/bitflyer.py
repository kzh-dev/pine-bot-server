# coding=utf-8

import requests

from .base import MarketBase, MarketError, empty_udf, utcunixtime, register_market

class BitFlyerMarketBase (MarketBase):

    SYMBOLS = ('FXBTCJPY',)
    URL_TMPL = "https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc?" + \
                "periods={resolution}&after={f}&before={t}"

    def __init__ (self, symbol='FXBTCJPY', resolution=60):
        super().__init__('BITFLYER', symbol, resolution)

    def mintick (self):
        return 1


class BitFlyerMarketDirect (BitFlyerMarketBase):

    def __init__ (self, symbol='FXBTCJPY', resolution=60):
        super().__init__(symbol, resolution)

        resolution *= 60
        unixtime = utcunixtime()
        since = unixtime - resolution * 256

        url   = self.URL_TMPL.format(resolution=resolution, f=since-1, t=unixtime+1)
        res = requests.get(url).json().get('result', None)
        if res:
            rows = res.get(str(resolution), None)
            if rows:
                self.data = self.rows_to_udf(rows)
            
register_market('BITFLYER', BitFlyerMarketDirect)


if __name__ == '__main__':
    BitFlyerMarketDirect()
