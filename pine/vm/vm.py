# coding=utf-8

from . import builtin_function
from . import builtin_variable
from ..base import PineError

from .helper import Series, BuiltinSeries, bseries, NaN


class AnnotationCollector (object):

    def __init__ (self):
        self.meta = None
        self.inputs = []
        self.securities = []
        self.strategies = []
        self.plots = []

    def register_meta (self, node):
        self.meta = node

    def register_input (self, node):
        if node not in self.inputs:
            self.inputs.append(node)

    def register_security (self, node):
        if node not in self.securities:
            self.securities.append(node)

    def register_strategy (self, node):
        if node not in self.strategies:
            self.strategies.append(node)

    def register_plot (self, node):
        if node not in self.plots:
            self.plots.append(node)

    def execute (self, node):
        node.collect_anotation(self)
        return (self.meta, self.inputs, self.securities, self.strategies, self.plots)


class BaseVM (object):

    def __init__ (self, market=None):
        self.market = market
        self.node = None
        self.ident = ''
        self.meta = {}
        self.inputs = {}
        self.securities = []
        self.strategies = []
        self.plots = []
        self.builtin_variable_cache = {}
        self.broker = None

    def reset_context (self):
        # setup registers
        self.registers = {}
        self.scoped_registers = []
        # timestamps
        self.timestamps = bseries(self.market.timestamp(), builtin_variable.time)
        # reset VM's ip
        self.ip = 0

    @property
    def title (self):
        return self.meta.get('title', 'No title')
    @property
    def overlay (self):
        return self.meta.get('overlay', False)

    def set_broker (self, broker):
        self.broker = broker
        return broker

    @property
    def size (self):
        return self.market.size()

    def load_node (self, node):
        self.node = node

        meta, self.inputs, self.securties,\
        self.strategies, self.plots = AnnotationCollector().execute(node)

        if meta:
            meta.evaluate(self)
            if self.broker:
                self.broker.setup(meta)

        self.reset_context()

    def push_register_scope (self):
        self.scoped_registers.append({})
    def pop_register_scope (self):
        registers = self.scoped_registers.pop(-1)
        for n in registers.keys():
            self.registers.pop(n)

    def get_register (self, node):
        return self.registers.get(node, None)

    def set_register (self, node, val):
        self.registers[node] = val
        if self.scoped_registers:
            self.scoped_registers[node] = val
        return val

    def alloc_register (self, node, v):
        if isinstance(v, Series):
            v = v.default_elem()
        if isinstance(v, float):
            v = [NaN]
        elif isinstance(v, int):
            v = [0]
        elif isinstance(v, bool):
            v = [False]
        else:
            raise PineError("invalid type for mutable variable: {0}: {1}".format(type(v), v))
        val = Series(v * self.size)
        val.valid_index = -1
        return self.set_register(node, val)

    def set_register_value (self, node, val):
        dest = self.registers[node]
        dest[self.ip] = val
        dest.valid_index = self.ip
        return dest

    def dump_registers (self):
        for n, v in self.registers.items():
            n.dump()
            if isinstance(v, Series):
                print("=====> {0}: {1}".format(v.valid_index, v))
            else:
                print("=====> {}".format(v))

    def step (self):
        self.node.evaluate(self)
        if self.broker:
            self.broker.step()
        self.ip += 1

    def is_last_step (self):
        return self.ip + 1 == self.size

    def run (self):
        #import time
        #t = time.time()
        while self.ip < self.size:
            self.step()
            #t_ = time.time()
            #print(t_ - t)
            #t = t_

    def get_default_input_title (self, node):
        idx = self.inputs.index(node)
        return 'input{}'.format(idx + 1)


class InputScanVM (BaseVM):

    def input (self, vm, args, kwargs, node):
        defval, title, typ,\
        minval, maxval, confirm, step, options = builtin_function._parse_input_args(args, kwargs)

        if not title and node:
            title = vm.get_default_input_title(node)
    
        defval_ = defval
        if typ is None:
            t = type(defval)
            if t == bool:
                typ = 'bool'
            elif t == int:
                typ = 'integer'
            elif t == float:
                typ = 'float'
            elif isinstance(defval, BuiltinSeries):
                typ = 'source'
                defval_ = defval.varname
                if not options:
                    options = tuple(builtin_variable.sources.keys())
            else:
                typ = 'string'
                # symbol, resolution, session

        return {
            'defval': defval_,
            'title': title,
            'type': typ,
            'minval': minval,
            'maxval': maxval,
            'options': options,
        }

    def run (self):
        return [n.evaluate(self) for n in self.inputs]


class VM (BaseVM):

    def __init__ (self, market=None):
        super().__init__(market)
        self.user_inputs = None

    def set_user_inputs (self, user_inputs):
        self.user_inputs = user_inputs

    def input (self, vm, args, kwargs, node):
        defval, title, typ,\
        minval, maxval, _, step, options = builtin_function._parse_input_args(args, kwargs)

        if not self.user_inputs:
            return defval

        if not title:
            title = vm.get_default_input_title(node)
        val = self.user_inputs.get(title, None)

        # bool, integer, float, string, symbol, resolution, session, source
        if not typ:
            t = type(defval)
            if t == bool:
                typ = 'bool'
            elif t == int:
                typ = 'integer'
            elif t == float:
                typ = 'float'
            elif isinstance(defval, BuiltinSeries):
                typ = 'source'

        if typ == 'bool':
            val = bool(val)
        elif typ == 'integer':
            val = int(val)
        elif typ == 'float':
            val = float(val)
        elif typ == 'source':
            func = builtin_variable.sources[val]
            val = func(self)

        return val
