# coding=utf-8

from inspect import getmembers, isfunction

from . import builtin_function
from . import builtin_variable
from ..base import PineError

class VM (object):

    def __init__ (self, market):
        self.prepare_function_table()
        self.prepare_variable_tables()
        self.market = market

    def _load_builtins (self, mod, mod_sfx, dest):
        for name, func in getmembers(mod, isfunction):
            if not func.__module__.endswith(mod_sfx):
                continue
            if name.startswith('_'):
                continue
            name = name.replace('__', '.')
            dest[name] = func

    def prepare_function_table (self):
        self.function_table = {}
        self._load_builtins(builtin_function, '.builtin_function', self.function_table)

    def register_function (self, name, args, node):
        self.function_table[name] = (args, node)

    def prepare_variable_tables (self):
        self.variable_tables = []
        # global scope
        tbl = {}
        self.variable_tables.append(tbl)
        self._load_builtins(builtin_variable, '.builtin_variable', tbl)

    def define_variable (self, name, value):
        self.variable_tables[-1][name] = value

    def lookup_variable (self, name):
        for t in reversed(self.variable_tables):
            v = t.get(name, None)
            if v:
                if isfunction(v):
                    return v(self)
                return v
        raise PineError("variable not found: {}".format(name))

    def func_call (self, fname, args, kwargs):
        func = self.function_table.get(fname, None)
        if func is None:
            raise PineError('fuction is not found: {}'.format(fname))
        if isfunction(func):
            return func(self, args, kwargs)
        else:
            print("Trying to call: {}".format(func))
            raise NotImplementedError
        
