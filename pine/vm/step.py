# coding=utf-8

import hashlib
import random
import time

from .vm import VM
from .helper import Series, BuiltinSeries

class StepVM (VM):

    def __init__ (self, market, pine_code):
        super().__init__(market)
        self.code = pine_code
        self.ident = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()

    @property
    def clock (self):
        return int(self.timestamps[-1])

    @property
    def next_clock (self):
        return int(self.timestamps[-1]) + self.market.resolution * 60

    def step_new (self):
        ## TODO SubVM

        # load a new candle
        max_trial = 15
        trial = 0
        next_clock = self.next_clock
        while trial < max_trial:
            trial += 1
            ts = self.market.step_ohlcv(next_clock)
            if ts:
                break
            time.sleep(1)
        # Fail to load?
        if next_clock > self.next_clock:
            return None
        
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
