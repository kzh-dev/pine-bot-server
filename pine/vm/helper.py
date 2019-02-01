# coding=utf-8

import numpy as np

class Series (np.ndarray):

    def __new__ (cls, vals):
        return np.asarray(vals).view(cls)

class BuiltinSeries (Series):
    pass

def bseries (vals, name):
    s = BuiltinSeries(vals)
    s.varname = name
    return s

def series_np (np_array):
    return Series(np_array)
