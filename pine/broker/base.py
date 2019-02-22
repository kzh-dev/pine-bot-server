# coding=utf-8

import math

from ..vm.helper import NaN
from ..base import PineError

class BaseBroker (object):

    def __init__ (self):
        self.pyramiding = 0
        self.calc_on_order_fills = False
        self.calc_on_every_tick = True
        self.backtest_fill_limits_assumption = 0.0
        self.default_qty_type = 'fixed'
        self.default_qty_value = 1.0
        self.currency = 'NONE'
        self.slippage = 0
        self.commission_type = 'percent'
        self.commission_value = 'commission_value'

        self.actions = []

    def setup (self, kws):
        v = kws.get('pyramiding', None)
        if v is not None:
            self.pyramiding = v
        v = kws.get('calc_on_order_fills', None)
        if v is not None:
            self.calc_on_order_fills = v
        v = kws.get('calc_on_every_tick', None)
        if v is not None:
                self.calc_on_every_tick = v
        v = kws.get('backtest_fill_limits_assumption', None)
        if v is not None:
            self.backtest_fill_limits_assumption = v
        v = kws.get('default_qty_type', None)
        if v is not None:
            self.default_qty_type = v
        v = kws.get('default_qty_value', None)
        if v is not None:
            self.default_qty_value = v
        v = kws.get('currency', None)
        if v is not None:
            self.currency = v
        v = kws.get('slippage', None)
        if v is not None:
            self.commission_type = 0.0
        
        if self.calc_on_order_fills:
            raise PineError('calc_on_order_fills is not supported')

    def entry (self, kws):
        #print('entry', kws)
        #oid = kws['id']
        #is_long = kws['long']
        #qty = kws.get('qty', self.default_qty_value)
        limit = kws.get('limit', None)
        stop = kws.get('stop', None)
        oca_name = kws.get('oca_name', '')
        oca_type = kws.get('oca_type', 'none')
        #comment = kws.get('comment', None)

        if limit is not None:
            raise PineError("limit order is not supported")
        if stop is not None:
            raise PineError("stop-limit order is not supported")
        if oca_name or oca_type:
            raise PineError("OCA order is not supported")

        kws['action'] = 'entry'
        self.add_action(kws)

    def close (self, kws):
        #print('close', kws)
        kws['action'] = 'close'
        self.add_action(kws)

    def close_all (self, kws):
        #print('close_all', kws)
        kws['action'] = 'close_all'
        self.add_action(kws)

    def add_action (self, action):
        self.actions.append(action)
    def clear_actions (self):
        self.actions = []

    def position_size (self):
        raise NotImplementedError

    def step (self):
        raise NotImplementedError


class Broker (BaseBroker):

    def __init__ (self):
        super().__init__()
        self.clear_positions()
        # TODO self.active_entry_orders[id], self.active_exit_orders[id]
        self.order_history = []

    def clear_positions (self):
        self.positions = {}

    def position_size (self):
        s = 0.0
        for p in self.positions.values():
            s += p['qty']
        return s

    def step (self):
        # TODO need to separate order and execution for limit order.
        # We should have no pending orders here.
        # Don't touch self.positions during order making.
        orders = []
        for a in self.actions:
            if a['action'] == 'entry':
                qty = a['qty']
                if qty is None or math.isnan(qty):
                    a['qty'] = self.default_qty_value
                if a['long']:
                    orders += self.close_positions(False)
                    orders += self.open_position(a)
                else:
                    orders += self.close_positions(True)
                    orders += self.open_position(a)
            elif a['action'] == 'close':
                orders += self.close_position(a['id'])
            elif a['action'] == 'close_all':
                orders += self.close_positions()
            else:
                raise PineError("Invalid strategy action type:  {}".format(a))

        self.clear_actions()

        # Apply orders
        self.apply_orders(orders)

        self.order_history.append(orders)
        return orders

    def close_position (self, oid):
        p = self.positions.get(oid, None)
        if p is None:
            return []
        else:
            return [{'id': oid, 'qty': -p['qty']}]
                
    def close_positions (self, d=None):
        if d is None:
            ids = self.positions.keys()
        elif d:
            ids = [i for i,p in self.positions.items() if p['qty'] > 0]
        else:
            ids = [i for i,p in self.positions.items() if p['qty'] < 0]

        orders = []
        for i in ids:
            orders += self.close_position(i)
        return orders

    def open_position (self, a):
        if a['long']:
            long_qty = sum([p['qty'] for p in self.positions.values() if p['qty'] > 0])
            qty = a['qty'] - long_qty
            if qty <= 0:
                return []
        else:
            short_qty = sum([p['qty'] for p in self.positions.values() if p['qty'] < 0])
            qty = -a['qty'] - short_qty
            if qty >= 0:
                return []

        p = self.positions.get(a['id'], None)
        if p:
            oqty = qty - p['qty']
            if a['long'] and oqty <= 0:
                return []
            if (not a['long']) and oqty >= 0:
                return []
        else:
            oqty = qty
        return [{'id': a['id'], 'qty': oqty}]

    def apply_orders (self, orders):
        for o in orders:
            i = o['id']
            p = self.positions.get(i, None)
            if p:
                qty = p['qty'] + o['qty']
                if qty == 0:
                    del self.positions[i]
                else:
                    p['qty'] = qty
            else:
                self.positions[i] = o
