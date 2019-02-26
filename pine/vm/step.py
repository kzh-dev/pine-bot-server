# coding=utf-8

import hashlib
import random
import time
import datetime

from .vm import VM
from .helper import Series, BuiltinSeries

class StepVM (VM):

    def __init__ (self, market, pine_code):
        super().__init__(market)
        self.code = pine_code
        self.ident = datetime.datetime.now().isoformat() + '@'\
                        hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()

    def scan_market (self):
        # TODO 
        for n in self.securties:
            n.evaluate(self)
        self.reset_context()
        return []

    def set_ohlcv (self, ohlcv):
        self.market.set_ohlcv(ohlcv)
        self.reset_context()

    @property
    def clock (self):
        return int(self.timestamps[-1])

    @property
    def next_clock (self):
        return int(self.timestamps[-1]) + self.market.resolution * 60

    def step_new (self):
        ## TODO SubVM

        # step registers
        for s in [v for v in self.registers.values() if isinstance(v, Series)]:
            if isinstance(s, BuiltinSeries):
                s.step(s.varfunc(self, 1))
            else:
                s.step()
        self.timestamps.step(self.timestamps.varfunc(self, 1))

        # set ip
        self.ip = self.size - 2

        # step and return actions
        self.step()
        return self.broker.next_actions
