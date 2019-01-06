# coding=utf-8

from inspect import getmembers, isfunction

from . import builtin_function
from ..base import PineError

class VM (object):

    def __init__ (self):
        self.prepare_function_table()
        self.prepare_variable_table()

    def prepare_function_table (self):
        self.function_table = {}
        for name, func in getmembers(builtin_function, isfunction):
            if not func.__module__.endswith('.builtin_function'):
                continue
            if name.startswith('_'):
                continue
            self.function_table[name] = func

    def register_function (self, name, args, node):
        self.function_table[name] = (args, node)

    def prepare_variable_table (self):
        self.variable_table = []
        # global scope
        self.variable_table.append({})

    def define_variable (self, name, value):
        self.variable_table[-1][name] = value

    def func_call (self, fname, args, kwargs):
        func = self.function_table.get(fname, None)
        if func is None:
            raise PineError('fuction is not found: {}'.format(fname))
        if isfunction(func):
            return func(self, args, kwargs)
        else:
            print("Trying to call: {}".format(func))
            raise NotImplementedError
        
