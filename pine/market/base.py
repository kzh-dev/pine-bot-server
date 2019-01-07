# coding=utf-8

class Market (object):

    def __init__ (self):
        pass

    def close (self):
        return [5000.0] * 200

    def open (self):
        return [4000.0] * 200

    def high (self):
        return [5500.0] * 200

    def low (self):
        return [4750.0] * 200

    def period (self):
        return 'DD'
    def tickerid (self):
        return 'MARKET:SYMBOL'

    # float(ms)
    def bartimestamp (self):
        import datetime
        import math
        unixtime = datetime.datetime.utcnow().timestamp()
        # round by 4h
        step = 60 * 240
        ts = math.floor(unixtime / step) * step
        return ts * 1000.0
