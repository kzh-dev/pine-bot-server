# coding=utf-8

import requests

from .base import MarketBase, MarketError, empty_udf, utcunixtime, register_market

class BitMexMarketBase (MarketBase):

    SYMBOLS = ('XBTUSD',)

    def __init__ (self, symbol='XBTUSD', resolution=60):
        super().__init__('BITMEX', symbol, resolution)

    def mintick (self):
        return 0.5


class BitMexMarketDirect (BitMexMarketBase):

    def __init__ (self, symbol='XBTUSD', resolution=60):
        super().__init__(symbol, resolution)

        unixtime = utcunixtime()
        since = unixtime - resolution * 60 * 256
        if resolution >= 1440:
            resolution = "{}D".format(resolution / 1440)

        param = {"period": resolution, "from": since, "to": unixtime}
        url   = "https://www.bitmex.com/api/udf/history?symbol=XBTUSD&" + \
                "resolution={period}&from={from}&to={to}".format(**param)

        self.data = requests.get(url).json()

    def resolutions (self):
        return (1, 5, 60, 60*24)


PROXY_PORT = 7000
# CandleProxyClient
from mprpc import RPCClient

class BitMexMarket (BitMexMarketBase):

    def __init__ (self, symbol='XBTUSD', resolution=60):
        super().__init__(symbol, resolution)

        self.client = RPCClient('127.0.0.1', PROXY_PORT)

        self._resolutions = tuple(self.client.call('resolutions'))
        self.data = self.client.call('ohlcv', self.resolution, 256)

    def resolutions (self):
        return self._resolutions



# CandleProxyServer
from mprpc import RPCServer
import threading
import fasteners
import queue
import time

class BitMexMarketProxyServer (RPCServer):

    UDF_RESOLUTIONS = ( 1, 5, 60, 60*24 )

    MIN_COUNT = 500
    MAX_COUNT = 10000

    URL_TMPL = "https://www.bitmex.com/api/udf/history?symbol=XBTUSD&" + \
                "resolution={resolution}&from={f}&to={t}"

    def __init__ (self):
        super().__init__()
        self.candles = {}
        self.lock = fasteners.ReaderWriterLock()
        self.queues = {}
        self.start_threads()

    def resolutions (self):
        return self.RESOLUTIONS

    def ohlcv (self, resolution, count):
        candles = self.candles[resolution]
        return dict(
            t=candles['t'][-count:],
            o=candles['o'][-count:],
            h=candles['h'][-count:],
            l=candles['l'][-count:],
            c=candles['c'][-count:],
            v=candles['v'][-count:],
        )

    def start_threads (self):
        resolutions = list(self.RESOLUTIONS)
        res_groups = []
        for udf_res in reversed(self.UDF_RESOLUTIONS):
            child_res = []
            while True:
                res = resolutions.pop(-1)
                if udf_res < res:
                    child_res.insert(0, res)
                else:
                    res_groups.append((udf_res, child_res))
                    break

        # maintainers
        for res, children in res_groups:
            self.queues[res] = queue.Queue()
            t = threading.Thread(target=self.candle_maintainer,
                                    args=(res, children), daemon=True)
            t.start()

        # loader
        t = threading.Thread(target=self.candle_loader, args=(res_groups,), daemon=True)
        t.start()

    def fetch_candles (self, resolution, from_, to):
        if resolution >= 60 * 24:
            resolution = "{}D".format(int(resolution / 60 / 24))
        url = self.URL_TMPL.format(resolution=resolution, f=from_, t=to)
        intvl = 1.0
        while True:
            try:
                j = requests.get(url).json()
                if j['s'] != 'ok':
                    raise MarketError("UDF refused: {}".format(j))
                return j
            except Exception as e:
                print(e)
                time.sleep(intvl)
                intvl *= min((intvl * 1.5, 60))

    def candle_loader (self, resolution_groups):
        next_timestamps = {}
        now = utcunixtime()
        for res, children in resolution_groups:
            maxres = res
            if children:
                maxres = children[-1]
            next_timestamps[res] = now - maxres * 60 * (self.MIN_COUNT - 1)

        while True:
            now = utcunixtime()
            # Fetch if necessary
            for res, next_ts in next_timestamps.items():
                if now < next_ts:
                    continue
                # try to get new candles
                candles = self.fetch_candles(res, next_ts - res * 60, now)
                ts = candles['t'][-1]
                if ts < next_ts:
                    continue
                # notify & schedule
                self.queues[res].put(candles)
                next_timestamps[res] = ts + res * 60
                #print(candles)

            # Schedule
            earlist = min(next_timestamps.values())
            interval = earlist - utcunixtime()
            if interval < 1:
                interval = 1
            interval = 3
            time.sleep(interval)

    def downsample_candle (self, source_res, target_res):
        source = self.candles[source_res]
        target = self.candles.get(target_res, None)
        slen = len(source['t'])
        tres = target_res * 60

        # Find last ts of target
        if target:
            ti = len(target['t']) - 1
            target_ts = target['t'][ti]
        else:
            ti = 0
            target_ts = 0
            target = empty_udf()
            self.candles[target_res] = target

        # Find corresponding source ts
        if target_ts:
            si = slen - 1
            while si:
                source_ts = source['t'][si]
                if source_ts <= target_ts and source_ts % tres == 0:
                    break
                si -= 1
        else:
            for i in range(0, slen):
                if source['t'][i] % tres == 0:
                    si = i
                    break

        # Down sample
        o = c = h = l = v = 0
        for i in range(si, slen):
            sts = source['t'][i]
            if sts % tres == 0:
                if o:
                    target['t'][ti] = sts - tres
                    target['o'][ti] = o
                    target['c'][ti] = c
                    target['h'][ti] = h
                    target['l'][ti] = l
                    target['v'][ti] = v
                    ti += 1
                o = source['o'][i]
                c = source['c'][i]
                h = source['h'][i]
                l = source['l'][i]
                v = source['v'][i]
            else:
                c = source['c'][i]
                h = max((h, source['h'][i]))
                l = min((l, source['l'][i]))
                v += source['v'][i]
        if o:
            target['t'][ti] = target['t'][ti-1] + tres
            target['o'][ti] = o
            target['c'][ti] = c
            target['h'][ti] = h
            target['l'][ti] = l
            target['v'][ti] = v

        if len(target) > self.MAX_COUNT:
            del target[0:self.MAX_COUNT/2]

    def update_candles (self, res, candles):
        target = self.candles.get(res, None)
        if target is None:
            target = empty_udf()
            self.candles[res] = target

        ti = target['t'].rindex(candles['t'][0])

        for i in range(0, len(candles['t'])):
            target['t'][ti+i] = candles['t'][i]
            target['o'][ti+i] = candles['o'][i]
            target['h'][ti+i] = candles['h'][i]
            target['l'][ti+i] = candles['l'][i]
            target['c'][ti+i] = candles['c'][i]
            target['v'][ti+i] = candles['v'][i]

        if len(target) > self.MAX_COUNT:
            del target[0:self.MAX_COUNT/2]

    def candle_maintainer (self, myres, children):
        maxres = myres
        if children:
            maxres = children[-1]

        while True:
            candles = self.queues[myres].get()

            with self.lock.write_lock():
                self.update_candles(myres, candles)

                # downsample
                for dres in children:
                    self.downsample_candle(myres, dres)

            # debug
            from datetime import datetime
            now = datetime.now()
            for res in [myres] + children:
                udf = self.candles[res]
                print("{}: {}: #={}: t={} c={} v={}".format(now, res, len(udf['t']), int(udf['t'][-1] % 3600 / 60), udf['c'][-1], udf['v'][-1]))

register_market('BITMEX', BitMexMarket)


if __name__ == '__main__':
    import os
    from gevent.server import StreamServer

    port = int(os.environ.get('PORT', PROXY_PORT))
    server = StreamServer(('127.0.0.1', port), BitMexMarketProxyServer())
    server.serve_forever()
