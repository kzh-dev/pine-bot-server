# coding=utf-8

import numpy as np

NaN = float('nan')

class Series (np.ndarray):

    def __new__ (cls, vals):
        obj = np.asarray(vals).view(cls)
        obj.valid_index = len(vals) - 1
        return obj

    def __array_finalize__ (self, obj):
        if obj is None:
            return
        self.valid_index = getattr(obj, 'valid_index', None)
        #self.valid_index = len(self)

    def logical_or (self, o):
        np.logical_or(self, o)

    def logical_and (self, o):
        np.logical_and(self, o)

class BuiltinSeries (Series):
    pass

def bseries (vals, name):
    s = BuiltinSeries(vals)
    s.varname = name
    return s

def series_np (np_array):
    return Series(np_array)
