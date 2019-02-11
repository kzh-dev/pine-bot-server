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

    def logical_or (self, ohther):
        s = self
        if isinstance(s[0], float):
            s = np.nan_to_num(s)
        o = other
        if isinstance(o, Series) and isinstance(o, float):
            o = np.nan_to_num(o)
        return np.logical_or(s, o).set_valid_index(self, other)

    def logical_and (self, other):
        s = self
        if isinstance(s[0], float):
            s = np.nan_to_num(s)
        o = other
        if isinstance(o, Series) and isinstance(o, float):
            o = np.nan_to_num(o)
        return np.logical_and(s, o).set_valid_index(self, other)

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

    def out_of_date (self, vm):
        return self.valid_index < vm.ip

    def filled (self): 
        return self.valid_index == (self.size - 1)

    def default_elem (self):
        if self.dtype == 'float64':
            return NaN
        elif self.dtype == 'int64':
            return 0
        elif self.dtype == 'bool':
            return False
        else:
            raise PineError("No default value for series: {}".format(self.dtype))

    def to_bool_safe (self):
        if self.dtype != 'float64':
            return self
        else:
            return np.nan_to_num(self)
    
class BuiltinSeries (Series):
    pass

def bseries (vals, name):
    s = BuiltinSeries(vals)
    s.varname = name
    return s

def series_np (np_array):
    return Series(np_array)
