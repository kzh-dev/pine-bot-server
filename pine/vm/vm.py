# coding=utf-8

from inspect import getmembers, isfunction

from . import builtin_function
from ..base import PineError

class VM (object):

    def __init__ (self):
        self.prepare_function_table()

    def prepare_function_table (self):
        self.function_table = {}
        for name, func in getmembers(builtin_function, isfunction):
            if not func.__module__.endswith('.builtin_function'):
                continue
            if name.startswith('_'):
                continue
            self.function_table[name] = func

    def func_call (self, fname, args, kwargs):
        func = self.function_table.get(fname, None)
        if func is None:
            raise PineError('fuction is not found: {}'.format(fname))
        if isfunction(func):
            return func(self, args, kwargs)
        else:
            raise NotImplementedError
        
