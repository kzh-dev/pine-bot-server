# coding=utf-8

import requests

from .base import MarketBase, MarketError, empty_udf, utcunixtime, register_market, rows_to_udf

URL_TMPL = "https://api.cryptowat.ch/markets/bitflyer/btcfxjpy/ohlc?" + \
            "periods={resolution}&after={f}&before={t}"

MARKET = 'BITFLYER'
SYMBOL = 'FXBTCJPY'
TICKERID = ':'.join((MARKET, SYMBOL))

class BitFlyerMarketBase (MarketBase):

    SYMBOLS = (SYMBOL,)

    def __init__ (self, symbol=SYMBOL, resolution=60):
        super().__init__(MARKET, symbol, resolution)

    def mintick (self):
        return 1


class BitFlyerMarketDirect (BitFlyerMarketBase):

    def __init__ (self, symbol=SYMBOL, resolution=60):
        super().__init__(symbol, resolution)

        resolution *= 60
        unixtime = utcunixtime()
        since = unixtime - resolution * 256

        url   = URL_TMPL.format(resolution=resolution, f=since-1, t=unixtime+1)
        res = requests.get(url).json().get('result', None)
        if res:
            rows = res.get(str(resolution), None)
            if rows:
                self.data = rows_to_udf(rows)
            
# CandleProxyClient
from .base import PROXY_PORT
from mprpc import RPCClient
class BitFlyerMarket (BitFlyerMarketBase):

    def __init__ (self, symbol=SYMBOL, resolution=60, port=PROXY_PORT):
        super().__init__(symbol, resolution)

        self.client = RPCClient('127.0.0.1', port)
        self.data = self.client.call('ohlcv', TICKERID, self.resolution, 256)

register_market(MARKET, BitFlyerMarket)
#register_market(MARKET, BitFlyerMarketDirect)

# CandleProxyServer
from .base import MarketOhlcvAdapter
class BitFlyerOhlcAdaptor (MarketOhlcvAdapter):

    def __init__ (self):
        super().__init__(TICKERID)

    def fetch_candles (self, resolution, from_, to):
        resolution *= 60
        url = URL_TMPL.format(resolution=resolution, f=from_, t=to)
        intvl = 1.0
        while True:
            try:
                j = requests.get(url).json()
                res = j.get('result', None)
                if res is None:
                    raise MarketError('missing result: {}'.format(j))
                rows = res.get(str(resolution), None)
                if rows is None:
                    raise MarketError('invalid result: {}'.format(res))
                return rows_to_udf(rows)
            except Exception as e:
                print(e)

#if __name__ == '__main__':
#    BitFlyerMarketDirect()

if __name__ == '__main__':
    import os
    from gevent.server import StreamServer
    port = int(os.environ.get('PORT', PROXY_PORT))
    cli = BitFlyerMarket(port=port)
    print(cli.data)
