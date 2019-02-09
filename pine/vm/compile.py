# coding=utf-8

from inspect import getmembers, isfunction, ismethod

from . import builtin_function
from . import builtin_variable
from ..base import PineError

def _load_builtins (mod, mod_sfx, dest):
    for name, func in getmembers(mod, isfunction):
        if not func.__module__.endswith(mod_sfx):
            continue
        if name.startswith('_'):
            continue
        name = name.replace('__', '.')
        dest[name] = func

builtin_variables = {}
_load_builtins(builtin_variable, '.builtin_variable', builtin_variables)

builtin_functions = {}
_load_builtins(builtin_function, '.builtin_function', builtin_functions)

class FuncExpander (object):

    def __init__ (self):
        self.funcs = {}

    def register_function (self, node):
        self.funcs[node.name] = node

    def lookup_function (self, name):
        f = self.funcs.get(name, None)
        if f:
            return f
        f = builtin_functions.get(name, None)
        if f:
            return f
        raise PineError('function is not found: {}'.format(fname))

    def execute (self, node):
        return node.expand_func(self)

class VarResolver (object):

    def __init__ (self):
        self.vars  = [{}]

    def push_scope (self):
        self.vars.insert(0, {})
    def pop_scope (self):
        self.vars.pop(0)

    def define_variable (self, node):
        self.vars[0][node.name] = node

    def lookup_variable (self, name):
        for t in self.vars:
            if name in t:
                return t[name]

        v = builtin_variables.get(name, None)
        if v is None:
            raise PineError("variable not found: {}".format(name))
        return v

    def execute (self, node):
        return node.resolve_var(self)

