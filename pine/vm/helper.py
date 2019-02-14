# coding=utf-8

import numpy as np
from ..base import PineError

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

    def logical_not (self):
        return np.logical_not(self).set_valid_index(self)

    def sign (self):
        return np.sign(self).set_valid_index(self)

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
        elif self.dtype == 'object':
            return False
        else:
            raise PineError("No default value for series: {}".format(self.dtype))

    def to_bool_safe (self, idx=None):
        if idx is None:
            r = self
        else:
            r = self[idx]
        if self.dtype != 'float64':
            return r
        else:
            return np.nan_to_num(r)

    def shift (self, offset):
        if offset == 0:
            return self

        d = self.default_elem()
        if abs(offset) >= self.size:
            r = Series([d] * self.size)
        else:
            r = np.roll(self, offset)
            if offset > 0:
                rng = range(0, offset)
            else:
                rng = range(self.size+offset, self.size)
            for i in rng:
                r[i] = d
        return r.set_valid_index(self)

    def to_mutable_series (self):
        r = Series([self.default_elem()] * self.size)
        r[0] = self[0]
        r.valid_index = 0
        return r
    
    def append (self, v):
        self.valid_index += 1
        self[self.valid_index] = v 
        return v

class BuiltinSeries (Series):
    pass

def bseries (vals, name):
    s = BuiltinSeries(vals)
    s.varname = name
    return s

def series_np (np_array):
    return Series(np_array)

def series_mutable (v, size):
    if isinstance(v, float):
        d = NaN
    elif isinstance(v, int):
        d = 0
    elif isinstance(v, bool):
        d = False
    else:
        d = None
    s = Series([d] * size)
    s[0] = v
    s.valid_index = 0
    return s

def series_immutable (v, size):
    return Series([v] * size)
