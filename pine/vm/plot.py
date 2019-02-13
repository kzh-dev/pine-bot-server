# coding=utf-8

import numpy

from . import builtin_function
from .vm import VM
from .helper import Series

class PlotVM (VM):

    def __init__ (self, market=None):
        super().__init__(market)
        self.outputs = []

    def load_node (self, node):
        super().load_node(node)

        # TODO good to save plot and strategy inputs if volatile
        # insert proxy node

    def plot (self, vm, args, kwargs):
        if not vm.is_last_step():
            return None

        series, title, color, linewidth, style,\
         trackprice, transp, histbase,\
         offset, join, editable, show_last = builtin_function._expand_args(args, kwargs, (
            ('series', None, True),
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

        if not isinstance(series, Series):
            series = Series([series] * vm.size)

        plot = {'title': title}

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
            if isinstance(color, Series):   # FIXME
                color = color[-1]
            plot['color'] = color
        if linewidth:
            plot['width'] = linewidth
        if transp:
            plot['alpha'] = transp * 0.01
        if offset:
            series = series.shift(offset)

        plot['series'] = series
        self.outputs.append(plot)
        return plot

    def plotshape (self, vm, args, kwargs):
        if not vm.is_last_step():
            return None

        series, title, style, location,\
         color, transp,\
         offset, text, textcolor,\
         editable, show_last, size = builtin_function._expand_args(args, kwargs, (
            ('series', None, True),
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

        if not isinstance(series, Series):
            series = Series([series] * vm.size)

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
        if offset:
            series = series.shift(offset)

        plot['series'] = series
        self.outputs.append(plot)
        return None

    def hline (self, vm, args, kwargs):
        if not vm.is_last_step():
            return None

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
            
        self.outputs.append(plot)
        return plot

    def fill (self, vm, args, kwargs):
        if not vm.is_last_step():
            return None

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
