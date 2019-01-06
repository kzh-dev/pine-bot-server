# coding=utf-8

class Market (object):

    def __init__ (self):
        pass

    def close (self):
        return [5000.0] * 200

    def open (self):
        return [4000.0] * 200

    def period (self):
        return 'DD'
    def tickerid (self):
        return 'MARKET:SYMBOL'
