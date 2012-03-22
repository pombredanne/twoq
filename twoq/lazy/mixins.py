# -*- coding: utf-8 -*-
'''lazy twoq mixins'''

from itertools import tee

from twoq.mixins.queuing import QueueingMixin, ResultMixin

from twoq.lazy.contexts import (
    AutoContext, OneArmContext, FourArmContext, TwoArmContext, ThreeArmContext)

__all__ = ['AutoQMixin', 'ManQMixin']


class BaseQMixin(QueueingMixin):

    '''base lazy queue'''

    def __init__(self, *args):
        incoming = iter([args[0]]) if len(args) == 1 else iter(args)
        self._work = iter([])
        self._util = iter([])
        self._1arm = OneArmContext
        self._2arm = TwoArmContext
        self._3arm = ThreeArmContext
        self._4arm = FourArmContext
        self._auto = AutoContext
        super(BaseQMixin, self).__init__(incoming, iter([]))

    def __len__(self):
        self.incoming, incoming = tee(self.incoming)
        return len(list(incoming))

    def outcount(self):
        '''count of outgoing things'''
        self.outgoing, outgoing = tee(self.outgoing)
        return len(list(outgoing))

    @property
    def balanced(self):
        '''if queues are balanced'''
        self.incoming, incoming = tee(self.incoming)
        self.outgoing, outgoing = tee(self.outgoing)
        return len(list(outgoing)) == len(list(incoming))


class AutoQMixin(BaseQMixin):

    '''auto-balancing queue mixin'''

    _default_context = AutoContext


class ManQMixin(BaseQMixin):

    '''manually balanced queue mixin'''

    _default_context = FourArmContext


class AutoResultMixin(ResultMixin, AutoQMixin):

    '''auto-balancing queue (with results extraction) mixin'''


class ManResultMixin(ResultMixin, ManQMixin):

    '''manually balanced queue (with results extraction) mixin'''
