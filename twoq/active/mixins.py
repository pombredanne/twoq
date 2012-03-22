# -*- coding: utf-8 -*-
'''active twoq mixins'''

from collections import deque

from stuf.utils import iterexcept, lazy

from twoq.mixins.queuing import QueueingMixin, ResultMixin

from twoq.active.contexts import (
    AutoContext, FourArmedContext, OneArmedContext, TwoArmedContext,
    ThreeArmedContext)

__all__ = ('AutoQMixin', 'ManQMixin')


class BaseQMixin(QueueingMixin):

    '''base active queue'''

    def __init__(self, *args):
        '''
        init

        @param incoming: incoming queue
        @param outgoing: outgoing queue
        '''
        # extend if just one argument
        incoming = deque()
        if len(args) == 1:
            incoming.append(args[0])
        else:
            incoming.extend(args)
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

    ###########################################################################
    ## clear queues ###########################################################
    ###########################################################################

    def inclear(self):
        '''clear incoming things'''
        self.incoming.clear()
        return self

    def outclear(self):
        '''clear outgoing things'''
        self.outgoing.clear()
        return self

    def _uclear(self):
        '''clear utility queue'''
        self._util.clear()
        return self

    def _wclear(self):
        '''clear work queue'''
        self._work.clear()
        return self

    ###########################################################################
    ## queue rotation #########################################################
    ###########################################################################

    def shift(self):
        '''shift outgoing things to incoming things'''
        self.incoming.extend(self.outgoing)
        return self

    def sync(self):
        '''
        shift outgoing things to incoming things, clearing incoming things
        '''
        # clear incoming things
        self.incoming.clear()
        # extend incoming things with outgoing things
        self.incoming.extend(self.outgoing)
        return self

    def outshift(self):
        '''shift incoming things to outgoing things'''
        self.outgoing.extend(self.incoming)
        return self

    def outsync(self):
        '''
        shift incoming things to outgoing things, clearing outgoing things
        '''
        # clear incoming things
        self.outgoing.clear()
        # extend incoming things with outgoing things
        self.outgoing.extend(self.incoming)
        return self


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
