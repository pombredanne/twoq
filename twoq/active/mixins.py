# -*- coding: utf-8 -*-
'''active twoq mixins'''

from collections import deque

from stuf.utils import lazy

from twoq.mixins.queuing import QueueingMixin, ResultMixin

from twoq.active.contexts import (
    AutoContext, OneArmContext, FourArmContext, TwoArmContext, ThreeArmContext)

__all__ = ('AutoQMixin', 'ManQMixin')


class BaseQMixin(QueueingMixin):

    '''base active queue'''

    def __init__(self, *args):
        incoming = deque(args[0]) if len(args) == 1 else deque(args)
        super(BaseQMixin, self).__init__(incoming, deque())
        self._1arm = OneArmContext
        self._2arm = TwoArmContext
        self._3arm = ThreeArmContext
        self._4arm = FourArmContext
        self._auto = AutoContext

    @lazy
    def _util(self):
        '''utility queue'''
        return deque()

    @lazy
    def _work(self):
        ''''work queue'''
        return deque()

    def __len__(self):
        return len(self.incoming)

    def outcount(self):
        '''count of outgoing things'''
        return len(self.outgoing)

    @property
    def balanced(self):
        '''if queues are balanced'''
        return len(self.outgoing) == len(self.incoming)


class AutoQMixin(BaseQMixin):

    '''auto-balancing queue mixin'''

    _default_context = AutoContext


class ManQMixin(BaseQMixin):

    '''manually balanced queue mixin'''

    _default_context = FourArmContext


class AutoResultMixin(AutoQMixin, ResultMixin):

    '''auto-balancing manipulation queue (with results extractor) mixin'''


class ManResultMixin(ManQMixin, ResultMixin):

    '''manually balanced queue (with results extractor) mixin'''
