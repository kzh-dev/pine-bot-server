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


PROXY_PORT = 7000

import threading
import fasteners
import queue
import time
class MarketOhlcvAdapter (object):

    MIN_COUNT = 500
    MAX_COUNT = 10000

    UDF_RESOLUTIONS = ( 1, 5, 60, 60*24 )

    def __init__ (self, tickerid='MARKET:SYMBOL'):
        super().__init__()
        self.tickerid = tickerid
        self.candles = {}
        self.lock = fasteners.ReaderWriterLock()
        self.queues = {}
        self.start_threads()

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
        resolutions = list(MarketBase.RESOLUTIONS)
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
        raise NotImplementedError

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
                print("{}: {}: {}: #={}: t={} c={} v={}".format(now, self.tickerid, res, len(udf['t']), int(udf['t'][-1] % 3600 / 60), udf['c'][-1], udf['v'][-1]))
