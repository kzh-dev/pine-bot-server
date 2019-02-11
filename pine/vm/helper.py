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
        return np.logical_or(self, o).set_valid_index(self, o)

    def logical_and (self, o):
        return np.logical_and(self, o).set_valid_index(self, o)

    def set_valid_index (self, a, b=None):
        if isinstance(b, Series):
            if isinstance(a, Series):
                self.valid_index = min(a.valid_index, b.valid_index)
            else:
                self.valid_index = b.valid_index
        elif isinstance(a, Series):
            self.valid_index = a.valid_index
        else:
            raise "Trying to set valid index for non-Series values: {0}, {1}".format(a, b)
        return self

class BuiltinSeries (Series):
    pass

def bseries (vals, name):
    s = BuiltinSeries(vals)
    s.varname = name
    return s

def series_np (np_array):
    return Series(np_array)
