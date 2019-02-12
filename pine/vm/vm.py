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
        self.meta = {}
        self.inputs = {}
        self.securities = []
        self.strategies = []
        self.plots = []
        self.builtin_variable_cache = {}

    @property
    def title (self):
        return self.meta.get('title', 'No title')
    @property
    def overlay (self):
        return self.meta.get('overlay', False)

    def load_node (self, node):
        self.node = node

        meta, self.inputs, self.securties,\
        self.strategies, self.plots = AnnotationCollector().execute(node)

        if meta:
            meta.evaluate(self)

        # setup registers
        self.registers = {}
        self.scoped_registers = []
        # timestamps
        self.size = self.market.size()
        self.timestamps = bseries(self.market.timestamp(), 'timestamp')
        # reset VM's ip
        self.ip = 0

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
        self.ip += 1

    def is_last_step (self):
        return self.ip + 1 == self.size

    def run (self):
        while self.ip < self.size:
            self.step()

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


class RenderVM (BaseVM):

    def __init__ (self, market, inputs):
        super().__init__(market)
        self.inputs = inputs
        self.function_table['input'] = self.input
        self.function_table['plot'] = self.plot
        self.function_table['hline'] = self.hline
        self.function_table['fill'] = self.fill
        self.function_table['plotshape'] = self.plotshape
        self.plots = []
        self.input_idx = 0

    def input (self, vm, args, kwargs):
        defval, title, typ,\
        minval, maxval, confirm, step, options = builtin_function._parse_input_args(args, kwargs)

        self.input_idx += 1
        if not title:
            title = "input{}".format(self.input_idx)

        val = self.inputs[title]
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
            val = self.lookup_variable(val)

        return val

    def plot (self, vm, args, kwargs):
        series, title, color, linewidth, style,\
         trackprice, transp, histbase,\
         offset, join, editable, show_last = builtin_function._expand_args(args, kwargs, (
            ('series', Series, True),
            ('title', str, False),
            ('color', None, False),
            ('linewidth', int, False),
            ('style', int, False),
            ('trackprice', bool, False),
            ('transp', int, False),
            ('histbase', float, False),
            ('offset', int, False),
            ('join', bool, False),
            ('editable', bool, False),
            ('show_last', int, False),
        ))

        plot = {'title': title, 'series': series}

        if style:
            if style == builtin_variable.STYLE_LINE:
                typ = 'line'
            elif style == builtin_variable.STYLE_STEPLINE:
                typ = 'line' 
            elif style == builtin_variable.STYLE_HISTOGRAM:
                typ = 'bar' 
            elif style == builtin_variable.STYLE_CROSS:
                typ = 'marker'
                plot['mark'] = '+'
            elif style == builtin_variable.STYLE_AREA:
                typ = 'band'
            elif style == builtin_variable.STYLE_COLUMNS:
                typ = 'bar'
            elif style == builtin_variable.STYLE_CIRCLES:
                typ = 'marker'
                plot['mark'] = 'o'
            else:
                typ = 'line'
            plot['type'] = typ

        if color is not None:
            if isinstance(color, Series):
                color = color[-1]
            plot['color'] = color
        if linewidth:
            plot['width'] = linewidth
        if transp:
            plot['alpha'] = transp * 0.01

        self.plots.append(plot)
        return plot

    def hline (self, vm, args, kwargs):
        price, title,\
         color, linestyle, linewidth, editable = builtin_function._expand_args(args, kwargs, (
            ('price', float, True),
            ('title', str, False),
            ('color', str, False),
            ('linestyle', int, False),
            ('linewidth', int, False),
            ('editable', bool, False),
        ))

        plot = {'title': title, 'series': price, 'type': 'hline'}
        if color:
            plot['color'] = color
        if linewidth:
            plot['width'] = linewidth
            
        self.plots.append(plot)
        return plot

    def fill (self, vm, args, kwargs):
        s1, s2,\
         color, transp, title, editable, _ = builtin_function._expand_args(args, kwargs, (
            ('series1', dict, True),
            ('series2', dict, True),
            ('color', str, False),
            ('transp', int, False),
            ('title', str, False),
            ('editable', bool, False),
            ('show_last', bool, False),
        ))

        plot = {'title': title, 'series': s1['series'], 'series2': s2['series'], 'type': 'fill'}
        
        if color is not None:
            if isinstance(color, Series):
                color = color[-1]
            plot['color'] = color
        if transp:
            plot['alpha'] = transp * 0.01

        self.plots.append(plot)
        return plot

    def plotshape (self, vm, args, kwargs):
        series, title, style, location,\
         color, transp,\
         offset, text, textcolor,\
         editable, show_last, size = builtin_function._expand_args(args, kwargs, (
            ('series', Series, True),
            ('title', str, False),
            ('style', str, False),
            ('location', str, False),
            ('color', str, False),
            ('transp', int, False),
            ('offset', int, False),
            ('text', str, False),
            ('textcolor', str, False),
            ('join', bool, False),
            ('editable', bool, False),
            ('show_last', int, False),
            ('size', str, False),
        ))

        plot = {'title': title}

        if location is None:
            pass

        if color is not None:
            if isinstance(color, Series):
                color = color[-1]
            plot['color'] = color
        if size:
            plot['size'] = size
        if transp:
            plot['alpha'] = transp * 0.01

        self.plots.append(plot)
        return plot

