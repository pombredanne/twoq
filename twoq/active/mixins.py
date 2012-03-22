# -*- coding: utf-8 -*-
'''active twoq mixins'''

from collections import deque

from stuf.utils import iterexcept, lazy

from twoq.mixins.queuing import QueueingMixin, ResultMixin

from twoq.active.contexts import (
    AutoContext, OneArmedContext, FourArmedContext, TwoArmedContext,
    ThreeArmedContext)

__all__ = ('AutoQMixin', 'ManQMixin')


class BaseQMixin(QueueingMixin):

    '''base active queue'''

    def __init__(self, *args):
        # extend if just one argument
        incoming = deque(args[0]) if len(args) == 1 else deque(args)
        self._1arm = OneArmedContext
        self._2arm = TwoArmedContext
        self._3arm = ThreeArmedContext
        self._4arm = FourArmedContext
        self._auto = AutoContext
        super(BaseQMixin, self).__init__(incoming, deque())

    @lazy
    def _util(self):
        '''utility queue'''
        return deque()

    @lazy
    def _work(self):
        ''''work queue'''
        return deque()

    ###########################################################################
    ## queue information ######################################################
    ###########################################################################

    def __len__(self):
        return len(self.incoming)

    count = __len__

    def outcount(self):
        '''count of outgoing things'''
        return len(self.outgoing)

    @property
    def balanced(self):
        '''if queues are balanced'''
        return len(self.outgoing) == len(self.incoming)


class ResultQMixin(ResultMixin):

    def results(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        for thing in iterexcept(self.outgoing.popleft, IndexError):
            yield thing


class AutoQMixin(BaseQMixin):

    '''auto-balancing queue mixin'''

    _default_context = AutoContext


class ManQMixin(BaseQMixin):

    '''manually balanced queue mixin'''

    _default_context = FourArmedContext


class AutoResultMixin(AutoQMixin, ResultQMixin):

    '''auto-balancing manipulation queue (with results extractor) mixin'''


class ManResultMixin(ManQMixin, ResultQMixin):

    '''manually balanced queue (with results extractor) mixin'''
