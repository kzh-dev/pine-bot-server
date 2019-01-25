# coding=utf-8

from inspect import getmembers, isfunction, ismethod

from . import builtin_function
from . import builtin_variable
from ..base import PineError

class VM (object):

    def __init__ (self, market):
        self.prepare_function_table()
        self.prepare_variable_tables()
        self.market = market
        self.title = 'No Title'

    def _load_builtins (self, mod, mod_sfx, dest):
        for name, func in getmembers(mod, isfunction):
            if not func.__module__.endswith(mod_sfx):
                continue
            if name.startswith('_'):
                continue
            name = name.replace('__', '.')
            dest[name] = func

    # TODO separate bultin table from user-defined one.
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

    def assign_variable (self, name, value):
        for t in reversed(self.variable_tables):
            if name in t:
                if type(t[name]) != type(value):
                    raise PineError('invalid type to assign: {0}: {1} for {2}'.format(name, value, t[name]))
                t[name] = value
                return value
        raise PineError('variable not found to assign: {}'.format(name))

    def lookup_variable (self, name):
        for t in reversed(self.variable_tables):
            if name in t:
                v = t[name]
                if isfunction(v):
                    try:
                        return v(self)
                    except NotImplementedError as e:
                        raise PineError('variable is not implemented: {}'.format(name)) from e
                return v
        raise PineError("variable not found: {}".format(name))

    def push_scope (self):
        self.variable_tables.append({})
        
    def pop_scope (self):
        self.variable_tables.pop(-1)

    def func_call (self, fname, args, kwargs):
        func = self.function_table.get(fname, None)
        if func is None:
            raise PineError('fuction is not found: {}'.format(fname))
        if isfunction(func) or ismethod(func):
            try:
                return func(self, args, kwargs)
            except NotImplementedError as e:
                raise PineError('function is not implemented: {}'.format(fname)) from e
        else:
            arg_ids, node = func
            try:
                self.push_scope()
                self._set_func_arguments(arg_ids, args, kwargs)
                return node.eval(self)
            finally:
                self.pop_scope()

    def _set_func_arguments (self, names, args, kwargs):
        if args:
            for n, a in zip(names, args):
                self.define_variable(n, a)
        if kwargs:
            for k, a in kwargs.items():
                self.define_variable(k, a)

        for n in names:
            if n not in self.variable_tables[-1]:
                raise PineError("missing argument: {}".format(n))

    def eval_node (self, node):
        self.push_scope()
        try:
            node.eval(self)
        finally:
            self.pop_scope()



class InputScanner (VM):

    def __init__ (self, market):
        super().__init__(market)
        self.input_func = self.function_table.get('input', None)
        self.function_table['input'] = self.input
        self.inputs = []

    def eval_node (self, node):
        super().eval_node(node)

    def input (self, vm, args, kwargs):
        defval, title, typ,\
        minval, maxval, confirm, step, options = builtin_function._parse_input_args(args, kwargs)
        self.inputs.append({
            'defval': defval,
            'title': title,
            'type': typ,
            'minval': minval,
            'maxval': maxval,
            'options': options,
        })
        return defval
