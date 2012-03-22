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

    ###########################################################################
    ## clear queues ###########################################################
    ###########################################################################

    def inclear(self):
        '''clear incoming things'''
        self.incoming = iter([])
        return self

    def outclear(self):
        '''clear outgoing things'''
        self.outgoing = iter([])
        return self

    def _wclear(self):
        '''clear work queue'''
        self._work = iter([])
        return self

    def _uclear(self):
        '''clear utility queue'''
        self._util = iter([])
        return self

    ###########################################################################
    ## balance queues #########################################################
    ###########################################################################

    def shift(self):
        '''shift outgoing things to incoming things'''
        self.outgoing, self.incoming = tee(self.outgoing)
        return self

    sync = shift

    def outshift(self):
        '''shift incoming things to outgoing things'''
        self.outgoing, self.incoming = tee(self.incoming)
        return self

    outsync = outshift


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
