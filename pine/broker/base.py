# coding=utf-8

from ..vm.helper import NaN
from ..base import PineError

class Broker (object):

    def __init__ (self):
        self.setup({})
        self.clear_positions()
        self.actions = []
        # TODO self.active_entry_orders[id], self.active_exit_orders[id]
        self.order_history = []

    def clear_positions (self):
        self.positions = {}

    def position_size (self):
        s = 0.0
        for p in self.positions.values():
            s += p['qty']
        return s

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

    def entry (self, kws):
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
        kws['action'] = 'close'
        self.add_action(kws)

    def close_all (self, kws):
        kws['action'] = 'close_all'
        self.add_action(kws)

    def add_action (self, action):
        self.actions.append(action)
    def clear_actions (self):
        self.actions = []

    def step (self):
        # TODO need to separate order and execution for limit order.
        # We should have no pending orders here.
        # Don't touch self.positions during order making.
        orders = []
        for a in self.actions:
            if a['action'] == 'entry':
                if a['qty'] is None:
                    a['qty'] = self.default_qty_value
                qty = a['qty']
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
