# coding=utf-8

import numpy as np
import talib as ta

STYLE_LINE = 0
STYLE_STEPLINE = 1
STYLE_HISTOGRAM = 2
STYLE_CROSS = 3
STYLE_AREA = 4
STYLE_COLUMNS = 5
STYLE_CIRCLES = 6

from ..base import PineError
from .helper import bseries


def accdist (vm):
    raise NotImplementedError

def adjustment__dividends (vm):
    raise NotImplementedError
def adjustment__none (vm):
    raise NotImplementedError
def adjustment__splits (vm):
    raise NotImplementedError

def aqua (vm):
    return '#00FFFF'

def area (vm):
    return STYLE_AREA
def areabr (vm):
    return 0

def barmerge__gaps_off (vm):
    return False
def barmerge__gaps_on (vm):
    return True
def barmerge__lookahead_off (vm):
    return False
def barmerge__lookahead_on (vm):
    return True

def barstate__isconfirmed (vm):
    raise NotImplementedError
def barstate__isfirst (vm):
    raise NotImplementedError
def barstate__ishistory (vm):
    raise NotImplementedError
def barstate__islast (vm):
    raise NotImplementedError
def barstate__isnew (vm):
    raise NotImplementedError
def barstate__isrealtime (vm):
    raise NotImplementedError

def black (vm):
    return '#000000'
def blue (vm):
    return '#0000FF'

def bool (vm):
    return 'bool'

def circles (vm):
    return STYLE_CIRCLES

def close (vm):
    return bseries(vm.market.close(), 'close')

def columns (vm):
    return STYLE_COLUMNS
def cross (vm):
    return STYLE_CROSS

def currency__AUD (vm):
    return NotImplementedError
def currency__CAD (vm):
    return NotImplementedError
def currency__CHF (vm):
    return NotImplementedError
def currency__EUR (vm):
    return NotImplementedError
def currency__GBP (vm):
    return NotImplementedError
def currency__HKD (vm):
    return NotImplementedError
def currency__JPY (vm):
    return NotImplementedError
def currency__NOK (vm):
    return NotImplementedError
def currency__NONE (vm):
    return NotImplementedError
def currency__NZD (vm):
    return NotImplementedError
def currency__RUB (vm):
    return NotImplementedError
def currency__SKE (vm):
    return NotImplementedError
def currency__SGD (vm):
    return NotImplementedError
def currency__TRY (vm):
    return NotImplementedError
def currency__USD (vm):
    return 'USD'
def currency__ZAR (vm):
    return NotImplementedError

def dashed (vm):
    return 0

def dayofmonth (vm):
    raise NotImplementedError
def dayofweek (vm):
    raise NotImplementedError

def dotted (vm):
    return 0

def float (vm):
    return 'float'

def friday (vm):
    raise NotImplementedError

def fuchsia (vm):
    return '#FF00FF'

def gray (vm):
    return '#808080'

def green (vm):
    return '#008000'

def high (vm):
    return bseries(vm.market.high(), 'high')

def histogram (vm):
    return STYLE_HISTOGRAM

def hl2 (vm):
    raise NotImplementedError

def hlc3 (vm):
    raise NotImplementedError

def integer (vm):
    return 'integer'

def interval (vm):
    raise NotImplementedError

def isdaily (vm):
    raise NotImplementedError

def isdwm (vm):
    raise NotImplementedError

def isintraday (vm):
    raise NotImplementedError

def ismonthly (vm):
    raise NotImplementedError

def isweekly (vm):
    raise NotImplementedError

def lime (vm):
    return '#00ff00'

def line (vm):
    return STYLE_LINE

def linebr (vm):
    return 0

def location__abovebar (vm):
    return 'abovebar'
def location__absolute (vm):
    return 'absolute'
def location__belowbar (vm):
    return 'belowbar'
def location__bottom (vm):
    return 'bottom'
def location__top (vm):
    return 'top'

def low (vm):
    return bseries(vm.market.low(), 'low')

def maroon (vm):
    return '#800000'

def minute (vm):
    raise NotImplementedError

def monday (vm):
    raise NotImplementedError

def month (vm):
    raise NotImplementedError

def n (vm):
    raise NotImplementedError

def na (vm):
    return float("nan")

def navy (vm):
    return '#000080'

def ohlc4 (vm):
    o = vm.market.open()
    h = vm.market.high()
    l = vm.market.low()
    c = vm.market.close()
    series = [sum(v4) / 4.0 for v4 in zip(o, h, l, c)]
    return bseries(series, 'ohlc4')

def olive (vm):
    return '#808000'

    raise NotImplementedError

def open (vm):
    return bseries(vm.market.open(), 'open')

def orange (vm):
    return '#ff7f00'

def period (vm):
    return vm.market.period()

def purple (vm):
    return '#800080'

def red (vm):
    return '#ff0000'

def resolution (vm):
    return 'resolution'

def saturday (vm):
    raise NotImplementedError

def scale__left (vm):
    return 0
def scale__none (vm):
    return 0
def scale__right (vm):
    return 0

def second (vm):
    raise NotImplementedError

def session (vm):
    raise NotImplementedError
def session__extended (vm):
    raise NotImplementedError
def session__regular (vm):
    raise NotImplementedError

def shape__arrowdown (vm):
    return 'arrowdown'
def shape__arrowup (vm):
    return 'arrowup'
def shape__circle (vm):
    return 'circle'
def shape__cross (vm):
    return 'cross'
def shape__diamond (vm):
    return 'diamond'
def shape__flag (vm):
    return 'flag'
def shape__labeldown (vm):
    return 'labeldown'
def shape__labelup (vm):
    return 'labelup'
def shape__square (vm):
    return 'square'
def shape__triangledown (vm):
    return 'triangledown'
def shape__triangleup (vm):
    return 'triangleup'
def shape__xcross (vm):
    return 'xcross'

def silver (vm):
    return "#c0c0c0"

def size__auto (vm):
    return 'auto'
def size__huge (vm):
    return 'huge'
def size__large (vm):
    return 'large'
def size__normal (vm):
    return 'normal'
def size__small (vm):
    return 'small'
def size__tiny (vm):
    return 'tiny'

def solid (vm):
    return 0

def source (vm):
    return 'source'

def stepline (vm):
    return STYLE_STEPLINE

def strategy__cash (vm):
    raise NotImplementedError
def strategy__closedtrades (vm):
    raise NotImplementedError
def strategy__commission__cash_per_contract (vm):
    return 'cash_per_contract'
def strategy__commission__cash_per_order (vm):
    return 'cash_per_order'
def strategy__commission__percent (vm):
    return 'percent'
def strategy__direction_all (vm):
    raise NotImplementedError
def strategy__direction_long (vm):
    raise NotImplementedError
def strategy__direction_short (vm):
    raise NotImplementedError
def strategy__equity (vm):
    raise NotImplementedError
def strategy__eventrades (vm):
    raise NotImplementedError
def strategy__fixed (vm):
    raise NotImplementedError
def strategy__grossloss (vm):
    raise NotImplementedError
def strategy__grossprofit (vm):
    raise NotImplementedError
def strategy__initial_capital (vm):
    raise NotImplementedError
def strategy__long (vm):
    raise NotImplementedError
def strategy__losstrades (vm):
    raise NotImplementedError
def strategy__max_contracts_held_all (vm):
    raise NotImplementedError
def strategy__max_contracts_held_long (vm):
    raise NotImplementedError
def strategy__max_drawdown (vm):
    raise NotImplementedError
def strategy__netprofit (vm):
    raise NotImplementedError
def strategy__oca__cancel (vm):
    raise NotImplementedError
def strategy__oca__none (vm):
    raise NotImplementedError
def strategy__oca__reduce (vm):
    raise NotImplementedError
def strategy__openprofit (vm):
    raise NotImplementedError
def strategy__opentrades (vm):
    raise NotImplementedError
def strategy__percent_of_equity (vm):
    return 'percent_of_equity'
def strategy__position_avg_price (vm):
    raise NotImplementedError
def strategy__position_entry_name (vm):
    raise NotImplementedError
def strategy__position_size (vm):
    raise NotImplementedError
def strategy__short (vm):
    raise NotImplementedError
def strategy__wintrades (vm):
    raise NotImplementedError

def string (vm):
    return 'string'

def sunday (vm):
    raise NotImplementedError

def symbol (vm):
    return 'symbol'

def syminfo__mintick (vm):
    raise NotImplementedError
def syminfo__pointvalue (vm):
    raise NotImplementedError
def syminfo__prefix (vm):
    raise NotImplementedError
def syminfo__root (vm):
    raise NotImplementedError
def syminfo__session (vm):
    raise NotImplementedError
def syminfo__timezone (vm):
    raise NotImplementedError

def teal (vm):
    return '#008080'

def thursday (vm):
    raise NotImplementedError

def ticker (vm):
    raise NotImplementedError
def tickerid (vm):
    return vm.market.tickerid()

def time (vm):
    return vm.market.bartimestamp()
def timenow (vm):
    raise NotImplementedError

def tr (vm):
    high = np.array(vm.market.high(), dtype='f8')
    low  = np.array(vm.market.low(),  dtype='f8')
    close = np.array(vm.market.close(), dtype='f8')
    return ta.TRANGE(high, low, close).tolist()

def tuesday (vm):
    raise NotImplementedError

def volume (vm):
    raise NotImplementedError

def vwap (vm):
    raise NotImplementedError

def wednesday (vm):
    raise NotImplementedError

def weekofyear (vm):
    raise NotImplementedError

def white (vm):
    return '#000000'

def year (vm):
    raise NotImplementedError

def yellow (vm):
    return '#ffff00'
