# -*- coding: utf-8 -*-
'''active twoq mixins'''

from collections import deque
from bisect import bisect_right

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

    def __contains__(self, thing):
        return thing in self.incoming

    def __len__(self):
        return len(self.incoming)

    def outcount(self):
        '''count of outgoing things'''
        return len(self.outgoing)

    @property
    def balanced(self):
        '''if queues are balanced'''
        return len(self.outgoing) == len(self.incoming)

    def index(self, thing):
        '''
        insert thing into incoming things

        @param thing: some thing
        '''
        return bisect_right(self.incoming, thing) - 1

    ###########################################################################
    ## clear queues ###########################################################
    ###########################################################################

    def __delitem__(self, index):
        incoming = self.incoming
        incoming.rotate(-index)
        incoming.popleft()
        incoming.rotate(index)

    def remove(self, thing):
        '''
        remove thing from incoming things

        @param thing: some thing
        '''
        incoming = self.incoming
        position = bisect_right(incoming, thing) - 1
        incoming.rotate(-position)
        incoming.popleft()
        incoming.rotate(position)
        return self

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
        self._util.extend(self.incoming)
        return self

    def _wclear(self):
        '''clear work queue'''
        self._work.clear()
        return self

    ###########################################################################
    ## manipulate queues ######################################################
    ###########################################################################

    def append(self, thing):
        '''
        append thing to right side of incoming things

        @param thing: some thing
        '''
        with self.ctx1()._sync as sync:
            sync.append(thing)
        return self.unswap()

    def appendleft(self, thing):
        '''
        append `thing` to left side of incoming things

        @param thing: some thing
        '''
        with self.ctx1()._sync as sync:
            sync.appendleft(thing)
        return self.unswap()

    def insert(self, index, thing):
        '''
        insert thing into incoming things

        @param index: index position
        @param thing: some thing
        '''
        incoming = self.incoming
        incoming.rotate(-index)
        incoming.appendleft(thing)
        incoming.rotate(index)
        return self

    def outextend(self, things):
        '''
        extend right side of outgoing things with `things`

        @param thing: some things
        '''
        with self.ctx1('outgoing')._sync as sync:
            sync(things)
        return self.unswap()

    def extend(self, things):
        '''
        extend right side of incoming things with `things`

        @param thing: some things
        '''
        with self.ctx1()._sync as sync:
            sync(things)
        return self.unswap()

    def extendleft(self, things):
        '''
        extend left side of incoming things with `things`

        @param thing: some things
        '''
        with self.ctx1()._sync as sync:
            sync.extendleft(things)
        return self.unswap()

    ###########################################################################
    ## queue rotation #########################################################
    ###########################################################################

    def reup(self):
        '''put incoming things in incoming things as one incoming thing'''
        with self.ctx1()._sync as sync:
            sync.append(list(sync.iterable))
        return self.unswap()

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


class AutoResultMixin(AutoQMixin, ResultQMixin):

    '''auto-balancing manipulation queue (with results extractor) mixin'''


class ManQMixin(BaseQMixin):

    '''manually balanced queue mixin'''

    _default_context = FourArmedContext


class ManResultMixin(ManQMixin, ResultQMixin):

    '''manually balanced queue (with results extractor) mixin'''
