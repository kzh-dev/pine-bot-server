# coding=utf-8

import math
from ..vm.helper import NaN
from ..base import PineError

class Broker (object):

    def __init__ (self):
        self.setup({})
        self.long_positions = {}
        self.short_positions = {}
        self.actions = []

    def setup (self, kws):
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
        
        if self.calc_on_order_fills:
            raise PineError('calc_on_order_fills is not supported')

    def step (self):
        # process actions and generate orders
        self.actions = []

    def entry (self, kws):
        oid = kws['id']
        is_long = kws['long']
        qty = kws.get('qty', self.default_qty_value)
        limit = kws.get('limit', None)
        stop = kws.get('stop', None)
        oca_name = kws.get('oca_name', '')
        oca_type = kws.get('oca_type', 'none')
        comment = kws.get('comment', 'none')

        if limit is not None:
            raise PineError("limit order is not supported")
        if stop is not None:
            raise PineError("stop-limit order is not supported")
        if oca_name or oca_type:
            raise PineError("OCA order is not supported")
        print("entry: {}".format(kws))

    def close (self, kws):
        oid = kws['id']
        print("close: {}".format(kws))

    def close_all (self, kws):
        print("close_all: {}".format(kws))
