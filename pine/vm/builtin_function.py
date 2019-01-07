# coding=utf-8

import math
import numpy as np
import talib as ta

from ..base import PineError

def _expand_args (args, kwargs, specs):
    args_dict = {}
    if args:
        la = len(args)
        ls = len(specs)
        if la > ls:
            raise PineError("Too many arguments: {0} for {1}".format(la , ls))
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
                raise PineError("Missing mandatory arguemnt: {}".format(name))
        else:
            if typ == float and type(a) == int:
                a = float(a)
            elif typ == int and type(a) == float and int(a) == a:
                a = int(a)
            elif typ is not None and not isinstance(a, typ):
                raise PineError("Invalid argument type mandatory arguemnt: {}".format(name))
        args_expanded.append(a)

    return args_expanded
    

def abs (vm, args, kwargs):
    raise NotImplementedError

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
    raise NotImplementedError

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
    raise NotImplementedError

def correlation (vm, args, kwargs):
    raise NotImplementedError

def cos (vm, args, kwargs):
    raise NotImplementedError

def corss (vm, args, kwargs):
    raise NotImplementedError

def corssover (vm, args, kwargs):
    raise NotImplementedError

def corssunder (vm, args, kwargs):
    raise NotImplementedError

def cum (vm, args, kwargs):
    raise NotImplementedError

def dayofmonth (vm, args, kwargs):
    raise NotImplementedError

def dayofweek (vm, args, kwargs):
    raise NotImplementedError

def dev (vm, args, kwargs):
    raise NotImplementedError

def ema (vm, args, kwargs):
    raise NotImplementedError

def exp (vm, args, kwargs):
    raise NotImplementedError

def falling (vm, args, kwargs):
    raise NotImplementedError

def fill (vm, args, kwargs):
    return None

def fixnan (vm, args, kwargs):
    raise NotImplementedError

def floor (vm, args, kwargs):
    raise NotImplementedError

def heikinashi (vm, args, kwargs):
    raise NotImplementedError

def highest (vm, args, kwargs):
    raise NotImplementedError

def highestbars (vm, args, kwargs):
    raise NotImplementedError

def hline (vm, args, kwargs):
    return None

def hour (vm, args, kwargs):
    raise NotImplementedError

def iff (vm, args, kwargs):
    raise NotImplementedError

def input (vm, args, kwargs):
    _args = _expand_args(args, kwargs,
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

    # TODO make dynamic, type check
    # return defval
    return _args[0]

def kagi (vm, args, kwargs):
    raise NotImplementedError

def linebreak (vm, args, kwargs):
    raise NotImplementedError

def linereg (vm, args, kwargs):
    raise NotImplementedError

def log (vm, args, kwargs):
    raise NotImplementedError

def log10 (vm, args, kwargs):
    raise NotImplementedError

def lowest (vm, args, kwargs):
    raise NotImplementedError

def lowestbars (vm, args, kwargs):
    raise NotImplementedError

def macd (vm, args, kwargs):
    raise NotImplementedError

def max (vm, args, kwargs):
    raise NotImplementedError

def min (vm, args, kwargs):
    raise NotImplementedError

def minute (vm, args, kwargs):
    raise NotImplementedError

def mom (vm, args, kwargs):
    raise NotImplementedError

def month (vm, args, kwargs):
    raise NotImplementedError

def na (vm, args, kwargs):
    x, = _expand_args(args, kwargs, (('x', None, True),))
    if isinstance(x, list):
        return [math.isnan(v) for v in x]
    else:
        return math.isnan(x)

def nz (vm, args, kwargs):
    raise NotImplementedError

def offset (vm, args, kwargs):
    raise NotImplementedError

def precentile_linear_interpolation (vm, args, kwargs):
    raise NotImplementedError

def precentile_nearest_rank (vm, args, kwargs):
    raise NotImplementedError

def percentrank (vm, args, kwargs):
    raise NotImplementedError

def pivothigh (vm, args, kwargs):
    raise NotImplementedError

def pivotlow (vm, args, kwargs):
    raise NotImplementedError

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

def pow (vm, args, kwargs):
    raise NotImplementedError

def renko (vm, args, kwargs):
    raise NotImplementedError

def rising (vm, args, kwargs):
    raise NotImplementedError

def rma (vm, args, kwargs):
    raise NotImplementedError

def roc (vm, args, kwargs):
    raise NotImplementedError

def round (vm, args, kwargs):
    raise NotImplementedError

def rsi (vm, args, kwargs):
    raise NotImplementedError

def sar (vm, args, kwargs):
    raise NotImplementedError

def second (vm, args, kwargs):
    raise NotImplementedError

def security (vm, args, kwargs):
    raise NotImplementedError

def sign (vm, args, kwargs):
    raise NotImplementedError

def sin (vm, args, kwargs):
    raise NotImplementedError

def sma (vm, args, kwargs):
    source, length = _expand_args(args, kwargs,
        (('source', list, True), ('length', int, True)))
    source = np.array(source, dtype='f8')
    return ta.SMA(source, length).tolist()

def sqrt (vm, args, kwargs):
    raise NotImplementedError

def stdev (vm, args, kwargs):
    raise NotImplementedError

def stoch (vm, args, kwargs):
    source, high, low, length = _expand_args(args, kwargs,
        (
            ('source', list, True),
            ('high', list, True),
            ('low', list, True),
            ('length', int, True),
        )
    )
    source = np.array(source, dtype='f8')
    high = np.array(high, dtype='f8')
    low = np.array(low, dtype='f8')
    fk, _ = ta.STOCHF(high, low, source, length)
    return fk.tolist()

def strategy (vm, args, kwargs):
    _ = _expand_args(args, kwargs,
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

def strategy__cancel (vm, args, kwargs):
    raise NotImplementedError

def strategy__cancel_all (vm, args, kwargs):
    raise NotImplementedError

def strategy__close (vm, args, kwargs):
    raise NotImplementedError

def strategy__close_all (vm, args, kwargs):
    raise NotImplementedError

def strategy__entry (vm, args, kwargs):
    raise NotImplementedError

def strategy__exit (vm, args, kwargs):
    raise NotImplementedError

def strategy__order (vm, args, kwargs):
    raise NotImplementedError

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

def study (vm, args, kwargs):
    title, stitle, _, _, _, _, _ = _expand_args(args, kwargs,
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
    return dt.timestamp() * 1000.0

def tostring (vm, args, kwargs):
    raise NotImplementedError

def tr (vm, args, kwargs):
    raise NotImplementedError

def tsi (vm, args, kwargs):
    raise NotImplementedError

def variance (vm, args, kwargs):
    raise NotImplementedError

def vwap (vm, args, kwargs):
    raise NotImplementedError

def vwma (vm, args, kwargs):
    raise NotImplementedError

def weekofyear (vm, args, kwargs):
    raise NotImplementedError

def wma (vm, args, kwargs):
    raise NotImplementedError

def year (vm, args, kwargs):
    raise NotImplementedError
