# coding=utf-8

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
                raise PineErrpr("Missing mandatory arguemnt: {}".fomrat(name))
        else:
            if not isinstance(a, typ):
                raise PineErrpr("Invalid argument type mandatory arguemnt: {}".fomrat(name))
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
    raise NotImplementedError

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
    raise NotImplementedError

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
    raise NotImplementedError

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
    raise NotImplementedError

def sqrt (vm, args, kwargs):
    raise NotImplementedError

def stdev (vm, args, kwargs):
    raise NotImplementedError

def stoch (vm, args, kwargs):
    raise NotImplementedError

def strategy (vm, args, kwargs):
    raise NotImplementedError

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
    raise NotImplementedError

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
