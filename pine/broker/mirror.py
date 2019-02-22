# coding=utf-8

from .base import BaseBroker

class MirrorBroker (BaseBroker):

    def __init__ (self):
        super().__init__()
        self._position_size = 0

    def position_size (self):
        return self._position_size

    def update (self, **kws):
        self._position_size = kws['position_size']

    def step (self):
        self.next_actions = self.actions
        self.clear_actions()
