# coding=utf-8

class Series (list):

    def __init__ (self, orig):
        super().__init__(orig)

class BuitinSeries (Series):
    pass

def bseries (vals, name):
    s = BuitinSeries(vals)
    s.varname = name
    return s

def series_np (np_array):
    return Series(np_array.tolist())
