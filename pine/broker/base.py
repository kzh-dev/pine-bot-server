# coding=utf-8

from ..helper import NaN

class Broker (object):

    def __init__ (self):
        self.setup({})

    def setup (self, **kws):
        self.pyramiding = kws.get('pyramiding', 0)
        self.calc_on_order_fills = kws.get('calc_on_order_fills', False)
        self.calc_on_every_tick = kws.get('calc_on_every_tick', False)
        self.backtest_fill_limits_assumption = kws.get('backtest_fill_limits_assumption', 0)
        self.default_qty_type = kws.get('default_qty_type', 'fixed')
        self.default_qty_value = kws.get('default_qty_value', 1.0)
        self.currency = kws.get('currency', 'NONE')
        self.slippage = kws.get('slippage', 0)
        self.commission_type = kws.get('commission_type', 'percent')
        self.commission_value = kws.get('commission_value', 0.0)

    def entry (self, **kws):
        oid = kws['id']
        is_long = kws['long']
        qty = kws.get('qty', NaN)
        limit = kws.get('limit', NaN)
        stop = kws.get('stop', NaN)
        oca_name = kws.get('oca_name', '')
        oca_type = kws.get('oca_type', 'none')
        comment = kws.get('comment', 'none')

    def close (self, **kws):
        oid = kws['id']
        raise NotImplementedError

    def close_all (self, **kws):
        raise NotImplementedError
