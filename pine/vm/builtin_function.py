# coding=utf-8

import math
import numpy as np
import talib as ta

from ..base import PineError
from .helper import Series, series_np, NaN, series_immutable, series_mutable

strategy_functions = {}
strategy_risk_functions = {}
plot_functions = {}


class PineArgumentError (PineError):
    def __init__ (self, msg):
        super().__init__(msg)

def _expand_args (args, kwargs, specs):
    args_dict = {}
    if args:
        la = len(args)
        ls = len(specs)
        if la > ls:
            raise PineArgumentError("Too many arguments: {0} for {1}".format(la , ls))
        for a, spec in zip(args, specs):
            n, _, _ = spec
            args_dict[n] = a
    if kwargs:
        args_dict.update(kwargs)

    args_expanded = []
    # TODO: wrong key check
    for name, typ, mand in specs:
        a = args_dict.get(name, None)
        if a is None:
            if mand:
                raise PineArgumentError("Missing mandatory arguemnt: {}".format(name))
        else:
            if typ == float and type(a) == int:
                a = float(a)
            elif typ == int and type(a) == float and int(a) == a:
                a = int(a)
            elif typ == bool and type(a) == str:
                if a == 'false':
                    a = False
            elif typ is not None and not isinstance(a, typ):
                raise PineArgumentError("Invalid argument type: {0}: {1} for {2}".format(
                    name, type(a).__name__, typ.__name__))
        args_expanded.append(a)

    return args_expanded

def _expand_args_as_dict (args, kwargs, specs):
    expanded = _expand_args(args, kwargs, specs)

    args_ = {}
    for v, spec in zip(expanded, specs):
        args_[spec[0]] = v
    return args_
    

def _ta_ma (args, kwargs, func):
    source, length = _expand_args(args, kwargs,
        (('source', Series, True), ('length', int, True)))
    try:
        return series_np(func(source, length), source)
    except Exception as e:
        if str(e) == 'inputs are all NaN':
            return source.dup()
        raise
            

pyabs = abs
def abs (vm, args, kwargs):
    source = _expand_args(args, kwargs, (('source', None, True),))[0]
    if isinstance(source, Series):
        return series_np(np.abs(source), source)
    else:
        return pyabs(source)

def acos (vm, args, kwargs):
    raise NotImplementedError

def alertcondition (vm, args, kwargs):
    raise NotImplementedError

def alma (vm, args, kwargs):
    raise NotImplementedError

def asin (vm, args, kwargs):
    raise NotImplementedError

def atan (vm, args, kwargs):
    raise NotImplementedError

def atr (vm, args, kwargs):
    raise NotImplementedError

def avg (vm, args, kwargs):
    raise NotImplementedError

def barcolor (vm, args, kwargs):
    raise NotImplementedError

def barssince (vm, args, kwargs):
    condition = _expand_args(args, kwargs, (
        ('condition', None, True),
    ))[0]
    if not isinstance(condition, Series):
        if bool(condition):
            return Series(list(range(1,vm.size+1)))
        return Series([0]*vm.size)

    # TODO speed!
    c = 0
    vidx = condition.valid_index
    dest = Series([0] * vm.size)
    for i in range(0, vidx+1):
        if condition.to_bool_safe(i):
            c = 0
        else:
            c += 1
        dest[i] = c
    return dest.set_valid_index(condition)

def bgcolor (vm, args, kwargs):
    return None

def cci (vm, args, kwargs):
    raise NotImplementedError

def ceil (vm, args, kwargs):
    raise NotImplementedError

def change (vm, args, kwargs):
    raise NotImplementedError

def cog (vm, args, kwargs):
    raise NotImplementedError

def color (vm, args, kwargs):
    col, transp = _expand_args(args, kwargs, (('color', str, True), ('transp', int, True)))
    return "{0}:{1}".format(col, transp)

def correlation (vm, args, kwargs):
    raise NotImplementedError

def cos (vm, args, kwargs):
    raise NotImplementedError

def cross (vm, args, kwargs):
    x, y = _expand_args(args, kwargs, (('x', Series, True), ('y', None, True)))
    if not isinstance(y, Series):
        y = series_immutable(y, vm.size)
    s = series_mutable(False, vm.size)
    imax = pymin([x.valid_index, y.valid_index])
    for i in range(1, imax+1):
        x1, y1 = x[i], y[i]
        x2, y2 = x[i-1], y[i-1]
        s.append((x1 - y1) * (x2 - y2) < 0)
    return s

def crossover (vm, args, kwargs):
    x, y = _expand_args(args, kwargs, (('x', Series, True), ('y', None, True)))
    if not isinstance(y, Series):
        y = series_immutable(y, vm.size)
    s = series_mutable(False, vm.size)
    imax = pymin([x.valid_index, y.valid_index])
    for i in range(1, imax+1):
        x1, y1 = x[i], y[i]
        x2, y2 = x[i-1], y[i-1]
        s.append(x1 > y1 and x2 < y2)
    return s

def crossunder (vm, args, kwargs):
    x, y = _expand_args(args, kwargs, (('x', Series, True), ('y', None, True)))
    if not isinstance(y, Series):
        y = series_immutable(y, vm.size)
    s = series_mutable(False, vm.size)
    imax = pymin([x.valid_index, y.valid_index])
    for i in range(1, imax+1):
        x1, y1 = x[i], y[i]
        x2, y2 = x[i-1], y[i-1]
        s.append(x1 < y1 and x2 > y2)
    return s

def cum (vm, args, kwargs):
    raise NotImplementedError

def dayofmonth (vm, args, kwargs):
    raise NotImplementedError

def dayofweek (vm, args, kwargs):
    raise NotImplementedError

def dev (vm, args, kwargs):
    raise NotImplementedError

def ema (vm, args, kwargs):
    return _ta_ma(args, kwargs, ta.EMA)

def exp (vm, args, kwargs):
    raise NotImplementedError

def falling (vm, args, kwargs):
    raise NotImplementedError

def fill (vm, args, kwargs):
    return None
plot_functions['fill'] = fill

def fixnan (vm, args, kwargs):
    raise NotImplementedError

def floor (vm, args, kwargs):
    raise NotImplementedError

def heikinashi (vm, args, kwargs):
    raise NotImplementedError

_xest_args1 = (
    ('length', int, True),
)
_xest_args2 = (
    ('source', Series, True),
) + _xest_args1

def _xest (vm, args, kwargs, sop, xop):
    try:
        source, length = _expand_args(args, kwargs, _xest_args2)
    except PineArgumentError:
        length = _expand_args(args, kwargs, _xest_args1)[0]
        source = sop(vm)
    return series_np(xop(source, length), source)

def highest (vm, args, kwargs):
    return _xest(vm, args, kwargs, high, ta.MAX)

def highestbars (vm, args, kwargs):
    raise NotImplementedError

def hline (vm, args, kwargs):
    return None
plot_functions['hline'] = hline

def hour (vm, args, kwargs):
    raise NotImplementedError

def iff (vm, args, kwargs):
    raise NotImplementedError

def _parse_input_args (args, kwargs):
    return _expand_args(args, kwargs,
        (
            ('defval', None, True),
            ('title', str, False),
            ('type', str, False),
            ('minval', None , False),
            ('maxval', None, False),
            ('confirm', bool, False),
            ('step', None, False),
            ('options', None, False),
        )
    )

def input (vm, args, kwargs, node=None):
    _args = _parse_input_args(args, kwargs)
    # TODO make dynamic, type check
    # return defval
    return _args[0]

def kagi (vm, args, kwargs):
    raise NotImplementedError

def linebreak (vm, args, kwargs):
    raise NotImplementedError

def linreg (vm, args, kwargs):
    source, length, _offset = _expand_args(args, kwargs,
        (('source', Series, True), ('length', int, True), ('offset', int, True)))
    try:
        return series_np(ta.LINEARREG(source, length) + _offset, source)
    except Exception as e:
        if str(e) == 'inputs are all NaN':
            return source.dup()
        raise

def log (vm, args, kwargs):
    raise NotImplementedError

def log10 (vm, args, kwargs):
    raise NotImplementedError

def lowest (vm, args, kwargs):
    return _xest(vm, args, kwargs, low, ta.MIN)

def lowestbars (vm, args, kwargs):
    raise NotImplementedError

def macd (vm, args, kwargs):
    raise NotImplementedError

def _mxx (args, kwargs, op, sop):
    x, y = _expand_args(args, kwargs, (('x', None, True), ('y', None, True)))
    if not isinstance(x, Series):
        if not isinstance(y, Series):
            # !x, !y
            if math.isna(x):
                return y
            elif math.isna(y):
                return x
            return op((x,y))
        else:
            # !x, y
            if math.isna(x):
                return y.dup()
            x = series_np([x] * y.size, y)
    elif not isinstance(y, Series):
        # x, !y
        if math.isna(y):
            return x.dup()
        y = series_np([y] * x.size, x)

    r = sop([x,y], axis=0)
    return Series(r).set_valid_index(x, y)

pymax = max
def max (vm, args, kwargs):
    return _mxx(args, kwargs, pymax, np.nanmax)

pymin = min
def min (vm, args, kwargs):
    return _mxx(args, kwargs, pymin, np.nanmin)

def minute (vm, args, kwargs):
    raise NotImplementedError

def mom (vm, args, kwargs):
    raise NotImplementedError

def month (vm, args, kwargs):
    raise NotImplementedError

def na (vm, args, kwargs):
    x, = _expand_args(args, kwargs, (('x', None, True),))
    if isinstance(x, Series):
        a = x[:x.valid_index+1]
        b = x[x.valid_index:]
        return Series([math.isnan(v) for v in a] + b).set_valid_index(x)
    else:
        return math.isnan(x)

def nz (vm, args, kwargs):
    x, y = _expand_args(args, kwargs, (('x', None, True),('y', None, False)))
    if y is None:
        y = 0.0
    if not isinstance(x, Series):
        if math.isnan(x):
            return y
        else:
            return x
    else:
        a = list(x)[:x.valid_index+1]
        b = list(x)[x.valid_index+1:]
        a_ = []
        for v in a:
            if math.isnan(v):
                v = y
            a_.append(v)
        return Series(a_ + b).set_valid_index(x)

def offset (vm, args, kwargs):
    source, _offset = _expand_args(args, kwargs,
        (('source', Series, True), ('offset', int, True)))
    return source.shift(_offset)

def precentile_linear_interpolation (vm, args, kwargs):
    raise NotImplementedError

def precentile_nearest_rank (vm, args, kwargs):
    raise NotImplementedError

def percentrank (vm, args, kwargs):
    raise NotImplementedError

_pivot_args2 = (
    ('leftbars', int, True),
    ('rightbars', int, True),
)
_pivot_args3 = (
    ('source', Series, True),
) + _pivot_args2

def _expand_pivot_args (args, kwargs):
    try:
        return _expand_args(args, kwargs, _pivot_args3)
    except PineArgumentError:
        l, r = _expand_args(args, kwargs, _pivot_args2)
        return (None, l,  r)

from .builtin_variable import high, low

# FIXME: follow TV's implementation
#def _pivot_inner (source, left, right, ismax):
#    slen = len(source)
#    if slen < left + right + 1:
#        return Series([NaN] * slen)
#
#    r = [NaN] * left
#    for i in range(left, slen - right):
#        v = source[i]
#        bars = source[i-left:i+right]
#        if ismax:
#            p = bars.max()
#        else:
#            p = bars.min()
#        if v == p:
#            r.append(v)
#        else:
#            r.append(NaN)
#    r += [NaN] * right
#    return Series(r)
def _pivot_inner (source, left, right, ismax):
    slen = len(source)
    if slen < left + right + 1:
        return Series([NaN] * slen)

    r = [NaN] * (left + right)
    for i in range(left, slen - right):
        v = source[i]
        bars = source[i-left:i+right]
        if ismax:
           p = bars.max()
        else:
            p = bars.min()
        if v == p:
            r.append(v)
        else:
            r.append(NaN)
    #r += [NaN] * right
    return Series(r)

def pivothigh (vm, args, kwargs):
    source, left, right = _expand_pivot_args(args, kwargs)
    if source is None:
        source = high(vm)
    return _pivot_inner(source, left, right, True)

def pivotlow (vm, args, kwargs):
    source, left, right = _expand_pivot_args(args, kwargs)
    if source is None:
        source = low(vm)
    return _pivot_inner(source, left, right, False)

def plot (vm, args, kwargs):
    return None
def plotarrow (vm, args, kwargs):
    return None
def plotbar (vm, args, kwargs):
    return None
def plotcandle (vm, args, kwargs):
    return None
def plotchar (vm, args, kwargs):
    return None
def plotshape (vm, args, kwargs):
    return None
def plotfigure (vm, args, kwargs):
    return None
plot_functions['plot'] = plot
plot_functions['plotarrow'] = plotarrow
plot_functions['plotbar'] = plotbar
plot_functions['plotcandle'] = plotcandle
plot_functions['plotchar'] = plotchar
plot_functions['plotshape'] = plotshape
plot_functions['plotfigure'] = plotfigure

def pow (vm, args, kwargs):
    raise NotImplementedError

def renko (vm, args, kwargs):
    raise NotImplementedError

def rising (vm, args, kwargs):
    raise NotImplementedError

def rma (vm, args, kwargs):
    source, length = _expand_args(args, kwargs,
        (('source', Series, True), ('length', int, True)))

    slen = len(source)
    if slen <= length:
        return source.dup()

    r = [NaN] * (length - 1)
    a = float(length - 1)
    for i in range(length - 1, slen):
        v = source[i]
        p = r[i-1]
        if math.isnan(v):
            r.append(NaN)
        else:
            if math.isnan(p):
                p = 0.0
            r.append((p * a + v) / length)
    return series_np(r, source)

def roc (vm, args, kwargs):
    raise NotImplementedError

def round (vm, args, kwargs):
    raise NotImplementedError

def rsi (vm, args, kwargs):
    x, y = _expand_args(args, kwargs,
        (('x', Series, True), ('y', int, True)))
    if math.isnan(x[-1]):
        return x.dup()
    return series_np(ta.RSI(x, y), x)

def sar (vm, args, kwargs):
    raise NotImplementedError

def second (vm, args, kwargs):
    raise NotImplementedError

def _parse_security_args (args, kwargs):
    return _expand_args(args, kwargs,
        (
            ('symbol', str, True),
            ('resolution', str, True),
            ('security', Series, True),
            ('gaps', bool , False),
            ('lookahead', bool, False),
        )
    )

def security (vm, args, kwargs):
    _parse_security_args(args, kwargs)
    raise NotImplementedError

def sign (vm, args, kwargs):
    raise NotImplementedError

def sin (vm, args, kwargs):
    raise NotImplementedError

def sma (vm, args, kwargs):
    return _ta_ma(args, kwargs, ta.SMA)

def sqrt (vm, args, kwargs):
    raise NotImplementedError

def stdev (vm, args, kwargs):
    source, length = _expand_args(args, kwargs,
        (
            ('source', Series, True),
            ('length', int, True),
        )
    )
    try:
        return series_np(ta.STDDEV(source, length), source)
    except Exception as e:
        if str(e) == 'inputs are all NaN':
            return source.dup()
        raise

def stoch (vm, args, kwargs):
    source, high, low, length = _expand_args(args, kwargs,
        (
            ('source', Series, True),
            ('high', Series, True),
            ('low', Series, True),
            ('length', int, True),
        )
    )
    try:
        fk, _ = ta.STOCHF(high, low, source, length)
        return series_np(fk, source)
    except Exception as e:
        if str(e) == 'inputs are all NaN':
            return source.dup()
        raise

def strategy (vm, args, kwargs):
    vm.meta = _expand_args_as_dict(args, kwargs,
        (
            ('title', str, True),
            ('shorttitle', str, False),
            ('overlay', bool, False),
            ('precision', int, False),
            ('scale', int, False),
            ('pyramiding', int, False),
            ('calc_on_order_fills', bool, False),
            ('calc_on_every_click', bool, False),
            ('max_bars_back', int, False),
            ('backtest_fill_limits_assumption', int, False),
            ('default_qty_type', str, False),
            ('default_qty_value', float, False),
            ('currency', str, False),
            ('linktoseries', bool, False),
            ('slippage', int, False),
            ('commision_type', str, False),
            ('commision_value', float, False),
        )
    )
    return None

def _evaluate_when (vm, val):
    if not isinstance(val, Series):
        return bool(val)
    return val[vm.ip]

def strategy__cancel (vm, args, kwargs):
    raise NotImplementedError

def strategy__cancel_all (vm, args, kwargs):
    raise NotImplementedError

def strategy__close (vm, args, kwargs):
    kws = _expand_args_as_dict(args, kwargs,
        (
            ('id', str, True),
            ('when', None, False),
        )
    )
    when = kws.get('when', None)
    if when is not None and not _evaluate_when(vm, when):
        return
    if vm.broker:
        return vm.broker.close(kws)
    return

def strategy__close_all (vm, args, kwargs):
    kws = _expand_args_as_dict(args, kwargs,
        (
            ('when', None, False),
        )
    )
    when = kws.get('when', None)
    if when is not None and not _evaluate_when(vm, when):
        return
    if vm.broker:
        return vm.broker.close_all(kws)
    return

def strategy__entry (vm, args, kwargs):
    if not vm.broker:
        return
    kws = _expand_args_as_dict(args, kwargs,
        (
            ('id', str, True),
            ('long', bool, True),
            ('qty', float, False),
            ('limit', float, False),
            ('stop', float, False),
            ('oca_name', str, False),
            ('oca_type', str, False),
            ('comment', str, False),
            ('when', None, False),
        )
    )
    when = kws.get('when', None)
    if when is not None and not _evaluate_when(vm, when):
        return
    if vm.broker:
        return vm.broker.entry(kws)
    return

def strategy__exit (vm, args, kwargs):
    raise NotImplementedError
    if not vm.broker:
        return None
    kws = _expand_args_as_dict(args, kwargs,
        (
            ('id', str, True),
            ('from_entry', str, False),
            ('qty', float, False),
            ('qty_percent', float, False),
            ('profit', float, False),
            ('oca_name', str, False),
            ('oca_type', str, False),
            ('comment', str, False),
            ('when', None, False),
        )
    )
    when = kws.get('when', None)
    if when is not None and not _evaluate_when(vm, when):
        return
    if vm.broker:
        return vm.broker.exit(kws)
    return

def strategy__order (vm, args, kwargs):
    raise NotImplementedError

strategy_functions['strategy.cancel'] = strategy__cancel
strategy_functions['strategy.cancel_all'] = strategy__cancel_all
strategy_functions['strategy.close'] = strategy__close
strategy_functions['strategy.close_all'] = strategy__close_all
strategy_functions['strategy.entry'] = strategy__entry
strategy_functions['strategy.exit'] = strategy__exit
strategy_functions['strategy.order'] = strategy__order


def strategy__risk__allow_entry_in (vm, args, kwargs):
    raise NotImplementedError

def strategy__risk__max_cons_loss_days (vm, args, kwargs):
    raise NotImplementedError

def strategy__risk__max_drawdown (vm, args, kwargs):
    raise NotImplementedError

def strategy__risk__max_intraday_filled_orders (vm, args, kwargs):
    raise NotImplementedError

def strategy__risk__max_intraday_loss (vm, args, kwargs):
    raise NotImplementedError

def strategy__risk__max_position_size (vm, args, kwargs):
    raise NotImplementedError

strategy_risk_functions['strategy.risk.allow_entry_in'] = strategy__risk__allow_entry_in
strategy_risk_functions['strategy.risk.max_cons_loss_days'] = strategy__risk__max_cons_loss_days
strategy_risk_functions['strategy.risk.max_drawdown'] = strategy__risk__max_drawdown
strategy_risk_functions['strategy.risk.max_intraday_filled_orders'] = strategy__risk__max_intraday_filled_orders
strategy_risk_functions['strategy.risk.max_intraday_loss'] = strategy__risk__max_intraday_loss
strategy_risk_functions['strategy.risk.max_position_size'] = strategy__risk__max_position_size


def study (vm, args, kwargs):
    vm.meta = _expand_args_as_dict(args, kwargs,
        (
            ('title', str, True),
            ('shorttitle', str, False),
            ('overlay', bool, False),
            ('precision', int, False),
            ('scale', int, False),
            ('max_bars_back', int, False),
            ('linktoseries', bool, False),
        )
    )
    return None

def sum (vm, args, kwargs):
    raise NotImplementedError

def swma (vm, args, kwargs):
    raise NotImplementedError

def tan (vm, args, kwargs):
    raise NotImplementedError

def tickerid (vm, args, kwargs):
    raise NotImplementedError

def time (vm, args, kwargs):
    raise NotImplementedError

def timestamp (vm, args, kwargs):
    import datetime
    import pytz
    spec1 = (
        ('year', int, True),
        ('month', int, True),
        ('day', int, True),
        ('hour', int, True),
        ('minute', int, True),
    )
    spec2 = (
        ('timezone', str, False),
    ) + spec1

    if args and isinstance(args[0], str):
        tz, year, month, day, hour, minute = _expand_args(args, kwargs, spec2)
        tzinfo = pytz.timezone(tz)
    else:
        year, month, day, hour, minute = _expand_args(args, kwargs, spec1)
        tzinfo = None

    dt = datetime.datetime(year, month, day, hour, minute, tzinfo=tzinfo)
    return int(dt.timestamp())

def tostring (vm, args, kwargs):
    raise NotImplementedError

def tr (vm, args, kwargs):
    raise NotImplementedError

def tsi (vm, args, kwargs):
    raise NotImplementedError

def valuewhen (vm, args, kwargs):
    condition, source, occurrence = _expand_args(args, kwargs, (
        ('condition', None, True),
        ('source', Series, True),
        ('occurrence', int, True),
    ))
    if not isinstance(condition, Series):
        if bool(condition):
            return source.offset(occurrence)
        return source.dup_none()

    # TODO speed!
    vidx = pymin([condition.valid_index, source.valid_index])
    tval = []
    dest = []
    dval = source.default_elem()
    for i in range(0, vidx+1):
        if condition.to_bool_safe(i):
            tval.append(source[i])
        if len(tval) > occurrence:
            dest.append(tval[-occurrence-1])
        else:
            dest.append(dval)
    for i in range(vidx+1, vm.size):
        dest.append(dval)
            
    return Series(dest).set_valid_index(condition, source)

def variance (vm, args, kwargs):
    raise NotImplementedError

def vwap (vm, args, kwargs):
    raise NotImplementedError

def vwma (vm, args, kwargs):
    raise NotImplementedError

def weekofyear (vm, args, kwargs):
    raise NotImplementedError

def wma (vm, args, kwargs):
    return _ta_ma(args, kwargs, ta.WMA)

def year (vm, args, kwargs):
    raise NotImplementedError
