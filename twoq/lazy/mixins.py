# -*- coding: utf-8 -*-
'''lazy twoq mixins'''

from itertools import tee

from twoq.mixins.queuing import QueueingMixin, ResultMixin

from twoq.lazy.contexts import (
    AutoContext, OneArmedContext, FourArmedContext, TwoArmedContext,
    ThreeArmedContext)

__all__ = ['AutoQMixin', 'ManQMixin']


class BaseQMixin(QueueingMixin):

    '''base lazy queue'''

    def __init__(self, *args):
        # "extend" if just one argument
        incoming = iter([args[0]]) if len(args) == 1 else iter(args)
        self._work = iter([])
        self._util = iter([])
        self._1arm = OneArmedContext
        self._2arm = TwoArmedContext
        self._3arm = ThreeArmedContext
        self._4arm = FourArmedContext
        self._auto = AutoContext
        super(BaseQMixin, self).__init__(incoming, iter([]))

    ###########################################################################
    ## queue information ######################################################
    ###########################################################################

    def __len__(self):
        self.incoming, incoming = tee(self.incoming)
        return len(list(incoming))

    count = __len__

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


class ResultQMixin(ResultMixin):

    def results(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        return self.outgoing


class AutoQMixin(BaseQMixin):

    '''auto-balancing queue mixin'''

    _default_context = AutoContext


class AutoResultMixin(ResultQMixin, AutoQMixin):

    '''auto-balancing queue (with results extraction) mixin'''


class ManQMixin(BaseQMixin):

    '''manually balanced queue mixin'''

    _default_context = FourArmedContext


class ManResultMixin(ResultQMixin, ManQMixin):

    '''manually balanced queue (with results extraction) mixin'''
