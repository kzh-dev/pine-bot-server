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
from .helper import bseries, NaN, series_np, series_mutable

sources = {}

def accdist (vm=None):
    raise NotImplementedError

def adjustment__dividends (vm=None):
    raise NotImplementedError
def adjustment__none (vm=None):
    raise NotImplementedError
def adjustment__splits (vm=None):
    raise NotImplementedError

def aqua (vm=None):
    return '#00FFFF'

def area (vm=None):
    return STYLE_AREA
def areabr (vm=None):
    return 0

def barmerge__gaps_off (vm=None):
    return False
def barmerge__gaps_on (vm=None):
    return True
def barmerge__lookahead_off (vm=None):
    return False
def barmerge__lookahead_on (vm=None):
    return True

def barstate__isconfirmed (vm=None):
    raise NotImplementedError
def barstate__isfirst (vm=None):
    raise NotImplementedError
def barstate__ishistory (vm=None):
    raise NotImplementedError
def barstate__islast (vm=None):
    raise NotImplementedError
def barstate__isnew (vm=None):
    raise NotImplementedError
def barstate__isrealtime (vm=None):
    raise NotImplementedError

def black (vm=None):
    return '#000000'
def blue (vm=None):
    return '#0000FF'

def bool (vm=None):
    return 'bool'

def circles (vm=None):
    return STYLE_CIRCLES

def close (vm=None):
    if vm is None:
        return None
    return bseries(vm.market.close(), 'close')
sources['close'] = close

def columns (vm=None):
    return STYLE_COLUMNS
def cross (vm=None):
    return STYLE_CROSS

def currency__AUD (vm=None):
    return NotImplementedError
def currency__CAD (vm=None):
    return NotImplementedError
def currency__CHF (vm=None):
    return NotImplementedError
def currency__EUR (vm=None):
    return NotImplementedError
def currency__GBP (vm=None):
    return NotImplementedError
def currency__HKD (vm=None):
    return NotImplementedError
def currency__JPY (vm=None):
    return NotImplementedError
def currency__NOK (vm=None):
    return NotImplementedError
def currency__NONE (vm=None):
    return NotImplementedError
def currency__NZD (vm=None):
    return NotImplementedError
def currency__RUB (vm=None):
    return NotImplementedError
def currency__SKE (vm=None):
    return NotImplementedError
def currency__SGD (vm=None):
    return NotImplementedError
def currency__TRY (vm=None):
    return NotImplementedError
def currency__USD (vm=None):
    return 'USD'
def currency__ZAR (vm=None):
    return NotImplementedError

def dashed (vm=None):
    return 0

def dayofmonth (vm=None):
    raise NotImplementedError
def dayofweek (vm=None):
    raise NotImplementedError

def dotted (vm=None):
    return 0

def float (vm=None):
    return 'float'

def friday (vm=None):
    raise NotImplementedError

def fuchsia (vm=None):
    return '#FF00FF'

def gray (vm=None):
    return '#808080'

def green (vm=None):
    return '#008000'

def high (vm=None):
    if vm is None:
        return None
    return bseries(vm.market.high(), 'high')
sources['high'] = high

def histogram (vm=None):
    return STYLE_HISTOGRAM

def hl2 (vm=None):
    if vm is None:
        return None
    h = vm.market.high()
    l = vm.market.low()
    series = [sum(v2) / 2.0 for v2 in zip(h, l)]
    return bseries(series, 'hl2')
sources['hl2'] = hl2

def hlc3 (vm=None):
    if vm is None:
        return None
    h = vm.market.high()
    l = vm.market.low()
    c = vm.market.close()
    series = [sum(v3) / 3.0 for v3 in zip(h, l, c)]
    return bseries(series, 'hlc3')
sources['hlc3'] = hlc3

def hour (vm=None):
    if vm is None:
        return 0
    return vm.timestamps[vm.ip] % (3600 * 24) / 3600

def integer (vm=None):
    return 'integer'

def interval (vm=None):
    raise NotImplementedError

def isdaily (vm=None):
    raise NotImplementedError

def isdwm (vm=None):
    raise NotImplementedError

def isintraday (vm=None):
    raise NotImplementedError

def ismonthly (vm=None):
    raise NotImplementedError

def isweekly (vm=None):
    raise NotImplementedError

def lime (vm=None):
    return '#00ff00'

def line (vm=None):
    return STYLE_LINE

def linebr (vm=None):
    return 0

def location__abovebar (vm=None):
    return 'abovebar'
def location__absolute (vm=None):
    return 'absolute'
def location__belowbar (vm=None):
    return 'belowbar'
def location__bottom (vm=None):
    return 'bottom'
def location__top (vm=None):
    return 'top'

def low (vm=None):
    if vm is None:
        return None
    return bseries(vm.market.low(), 'low')
sources['low'] = low

def maroon (vm=None):
    return '#800000'

def minute (vm=None):
    if vm is None:
        return 0
    return vm.timestamps[vm.ip] % 3600 / 60

def monday (vm=None):
    raise NotImplementedError

def month (vm=None):
    raise NotImplementedError

def n (vm=None):
    raise NotImplementedError

def na (vm=None):
    return NaN

def navy (vm=None):
    return '#000080'

def ohlc4 (vm=None):
    if vm is None:
        return None
    o = vm.market.open()
    h = vm.market.high()
    l = vm.market.low()
    c = vm.market.close()
    series = [sum(v4) / 4.0 for v4 in zip(o, h, l, c)]
    return bseries(series, 'ohlc4')
sources['ohlc4'] = ohlc4

def olive (vm=None):
    return '#808000'

    raise NotImplementedError

def open (vm=None):
    if vm is None:
        return None
    return bseries(vm.market.open(), 'open')
sources['open'] = open

def orange (vm=None):
    return '#ff7f00'

def period (vm=None):
    if vm is None:
        return None
    return vm.market.period()

def purple (vm=None):
    return '#800080'

def red (vm=None):
    return '#ff0000'

def resolution (vm=None):
    return 'resolution'

def saturday (vm=None):
    raise NotImplementedError

def scale__left (vm=None):
    return 0
def scale__none (vm=None):
    return 0
def scale__right (vm=None):
    return 0

def second (vm=None):
    if vm is None:
        return 0
    return vm.timestamps[vm.ip] % 60

def session (vm=None):
    raise NotImplementedError
def session__extended (vm=None):
    raise NotImplementedError
def session__regular (vm=None):
    raise NotImplementedError

def shape__arrowdown (vm=None):
    return 'arrowdown'
def shape__arrowup (vm=None):
    return 'arrowup'
def shape__circle (vm=None):
    return 'circle'
def shape__cross (vm=None):
    return 'cross'
def shape__diamond (vm=None):
    return 'diamond'
def shape__flag (vm=None):
    return 'flag'
def shape__labeldown (vm=None):
    return 'labeldown'
def shape__labelup (vm=None):
    return 'labelup'
def shape__square (vm=None):
    return 'square'
def shape__triangledown (vm=None):
    return 'triangledown'
def shape__triangleup (vm=None):
    return 'triangleup'
def shape__xcross (vm=None):
    return 'xcross'

def silver (vm=None):
    return "#c0c0c0"

def size__auto (vm=None):
    return 'auto'
def size__huge (vm=None):
    return 'huge'
def size__large (vm=None):
    return 'large'
def size__normal (vm=None):
    return 'normal'
def size__small (vm=None):
    return 'small'
def size__tiny (vm=None):
    return 'tiny'

def solid (vm=None):
    return 0

def source (vm=None):
    return 'source'

def stepline (vm=None):
    return STYLE_STEPLINE

def strategy__cash (vm=None):
    return 'cash'
def strategy__closedtrades (vm=None):
    raise NotImplementedError
def strategy__commission__cash_per_contract (vm=None):
    return 'cash_per_contract'
def strategy__commission__cash_per_order (vm=None):
    return 'cash_per_order'
def strategy__commission__percent (vm=None):
    return 'percent'
def strategy__direction_all (vm=None):
    raise NotImplementedError
def strategy__direction_long (vm=None):
    raise NotImplementedError
def strategy__direction_short (vm=None):
    raise NotImplementedError
def strategy__equity (vm=None):
    raise NotImplementedError
def strategy__eventrades (vm=None):
    raise NotImplementedError
def strategy__fixed (vm=None):
    return 'fixed'
def strategy__grossloss (vm=None):
    raise NotImplementedError
def strategy__grossprofit (vm=None):
    raise NotImplementedError
def strategy__initial_capital (vm=None):
    raise NotImplementedError
def strategy__long (vm=None):
    return True
def strategy__losstrades (vm=None):
    raise NotImplementedError
def strategy__max_contracts_held_all (vm=None):
    raise NotImplementedError
def strategy__max_contracts_held_long (vm=None):
    raise NotImplementedError
def strategy__max_drawdown (vm=None):
    raise NotImplementedError
def strategy__netprofit (vm=None):
    raise NotImplementedError
def strategy__oca__cancel (vm=None):
    raise NotImplementedError
def strategy__oca__none (vm=None):
    raise NotImplementedError
def strategy__oca__reduce (vm=None):
    raise NotImplementedError
def strategy__openprofit (vm=None):
    raise NotImplementedError
def strategy__opentrades (vm=None):
    raise NotImplementedError
def strategy__percent_of_equity (vm=None):
    return 'percent_of_equity'
def strategy__position_avg_price (vm=None):
    raise NotImplementedError
def strategy__position_entry_name (vm=None):
    raise NotImplementedError
def strategy__position_size (vm=None):
    if vm is None:
        return None
    if vm.broker is None:
        return 0.0
    sz = vm.broker.position_size()
    if vm.ip == 0:
        return series_mutable(sz, vm.size)
    return sz

def strategy__short (vm=None):
    return False
def strategy__wintrades (vm=None):
    raise NotImplementedError

def string (vm=None):
    return 'string'

def sunday (vm=None):
    raise NotImplementedError

def symbol (vm=None):
    return 'symbol'

def syminfo__mintick (vm=None):
    if vm is None:
        return 0.0
    return vm.market.mintick()
    raise NotImplementedError
def syminfo__pointvalue (vm=None):
    raise NotImplementedError
def syminfo__prefix (vm=None):
    raise NotImplementedError
def syminfo__root (vm=None):
    raise NotImplementedError
def syminfo__session (vm=None):
    raise NotImplementedError
def syminfo__timezone (vm=None):
    raise NotImplementedError

def teal (vm=None):
    return '#008080'

def thursday (vm=None):
    raise NotImplementedError

def ticker (vm=None):
    raise NotImplementedError
def tickerid (vm=None):
    if vm is None:
        return None
    return vm.market.tickerid()

def time (vm=None):
    if vm is None:
        return None
    return vm.timestamps
def timenow (vm=None):
    raise NotImplementedError

def tr (vm=None):
    if vm is None:
        return None
    high = np.array(vm.market.high(), dtype='f8')
    low  = np.array(vm.market.low(),  dtype='f8')
    close = np.array(vm.market.close(), dtype='f8')
    return series_np(ta.TRANGE(high, low, close))

def tuesday (vm=None):
    raise NotImplementedError

def volume (vm=None):
    raise NotImplementedError

def vwap (vm=None):
    raise NotImplementedError

def wednesday (vm=None):
    raise NotImplementedError

def weekofyear (vm=None):
    raise NotImplementedError

def white (vm=None):
    return '#000000'

def year (vm=None):
    raise NotImplementedError

def yellow (vm=None):
    return '#ffff00'
