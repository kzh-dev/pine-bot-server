# coding=utf-8

import requests

from .base import MarketBase, MarketError, empty_udf, utcunixtime, register_market

URL_TMPL = "https://www.bitmex.com/api/udf/history?symbol=XBTUSD&" + \
            "resolution={resolution}&from={f}&to={t}"

MARKET = 'BITMEX'
SYMBOL = 'XBTUSD'
TICKERID = 'BITMEX:XBTUSD'

class BitMexMarketBase (MarketBase):

    SYMBOLS = (SYMBOL,)

    def __init__ (self, symbol=SYMBOL, resolution=60):
        super().__init__(MARKET, symbol, resolution)

    def mintick (self):
        return 0.5


class BitMexMarketDirect (BitMexMarketBase):

    def __init__ (self, symbol='XBTUSD', resolution=60):
        super().__init__(symbol, resolution)

        unixtime = utcunixtime()
        since = unixtime - resolution * 60 * 256
        if resolution >= 1440:
            resolution = "{}D".format(resolution / 1440)

        url = URL_TMPL.format(resolution=resolution, f=since, t=unixtime)
        self.data = requests.get(url).json()


from .base import PROXY_PORT
# CandleProxyClient
from mprpc import RPCClient
class BitMexMarket (BitMexMarketBase):

    def __init__ (self, symbol=SYMBOL, resolution=60, port=PROXY_PORT):
        super().__init__(symbol, resolution)

        self.client = RPCClient('127.0.0.1', port)
        self.data = self.client.call('ohlcv', TICKERID, self.resolution, 256)

register_market(MARKET, BitMexMarket)

# CandleProxyServer
from .base import MarketOhlcvAdapter
class BitMexOhlcAdaptor (MarketOhlcvAdapter):

    def __init__ (self):
        super().__init__(TICKERID)

    def fetch_candles (self, resolution, from_, to):
        if resolution >= 60 * 24:
            resolution = "{}D".format(int(resolution / 60 / 24))
        url = URL_TMPL.format(resolution=resolution, f=from_, t=to)
        intvl = 1.0
        while True:
            try:
                j = requests.get(url).json()
                if j['s'] != 'ok':
                    raise MarketError("UDF refused: {}".format(j))
                return j
            except Exception as e:
                print(e)

if __name__ == '__main__':
    import os
    from gevent.server import StreamServer
    port = int(os.environ.get('PORT', PROXY_PORT))
    cli = BitMexMarket(port=port)
    print(cli.data)
