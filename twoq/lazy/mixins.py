# -*- coding: utf-8 -*-
'''lazy twoq mixins'''

from itertools import tee
from collections import deque

from twoq.mixins.queuing import QueueingMixin, ResultMixin

from twoq.lazy.contexts import (
    AutoContext, OneArmedContext, FourArmedContext, TwoArmedContext)

__all__ = ['AutoQMixin', 'ManQMixin']


class BaseQMixin(QueueingMixin):

    '''base lazy queue'''

    def __init__(self, *args):
        # "extend" if just one argument
        incoming = iter([args[0]]) if len(args) == 1 else iter(args)
        self._work = None
        self._util = None
        self._1arm = OneArmedContext
        self._2arm = TwoArmedContext
        self._4arm = FourArmedContext
        self._auto = AutoContext
        super(BaseQMixin, self).__init__(incoming, iter([]))

    ###########################################################################
    ## queue information ######################################################
    ###########################################################################

    def __contains__(self, value):
        self.incoming, incoming = tee(self.incoming)
        return value in list(incoming)

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

    def index(self, thing):
        '''
        index of thing in incoming things

        @param thing: some thing
        '''
        self.incoming, incoming = tee(self.incoming)
        return list(incoming).index(thing)

    ###########################################################################
    ## clear queues ###########################################################
    ###########################################################################

    def __delitem__(self, index):
        self.incoming = list(self.incoming)
        del self.incoming[index]
        self.incoming = iter(self.incoming)

    def remove(self, thing):
        '''
        remove thing from incoming things

        @param thing: some thing
        '''
        self.incoming = list(self.incoming)
        self.incoming.remove(thing)
        self.incoming = iter(self.incoming)
        return self

    def inclear(self):
        '''clear incoming things'''
        self.incoming = iter([])
        return self

    def outclear(self):
        '''clear outgoing things'''
        self.outgoing = iter([])
        return self

    def _uclear(self):
        '''clear read-only queue'''
        self._util = None
        self._util, self._incoming = tee(self.incoming)
        return self

    ###########################################################################
    ## manipulate queues ######################################################
    ###########################################################################

    def append(self, thing):
        '''
        append thing to right side of incoming things

        @param thing: some thing
        '''
        self.incoming = deque(self.incoming)
        self.incoming.append(thing)
        self.incoming = iter(self.incoming)
        return self

    def appendleft(self, thing):
        '''
        append `thing` to left side of incoming things

        @param thing: some thing
        '''
        self.incoming = deque(self.incoming)
        self.incoming.appendleft(thing)
        self.incoming = iter(self.incoming)
        return self

    def insert(self, index, value):
        '''
        insert thing into incoming things

        @param index: index position
        @param thing: some thing
        '''
        self.incoming = list(self.incoming)
        self.incoming.insert(index, value)
        self.incoming = iter(self.incoming)
        return self

    def extend(self, things):
        '''
        extend right side of incoming things with `things`

        @param thing: some things
        '''
        self.incoming = deque(self.incoming)
        self.incoming.extend(things)
        self.incoming = iter(self.incoming)
        return self

    def outextend(self, things):
        '''
        extend right side of outgoing things with `things`

        @param thing: some things
        '''
        outgoing = deque(self.outgoing)
        outgoing.extend(things)
        self.outgoing = iter(outgoing)
        return self

    def extendleft(self, things):
        '''
        extend left side of incoming things with `things`

        @param thing: some things
        '''
        self.incoming = deque(self.incoming)
        self.incoming.extendleft(things)
        self.incoming = iter(self.incoming)
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

    def reup(self):
        '''put incoming things in incoming things as one incoming thing'''
        with self._sync as sync:
            sync.append(list(self.incoming))
        return self


class AutoResultMixin(ResultQMixin, AutoQMixin):

    '''auto-balancing queue (with results extraction) mixin'''


class ManQMixin(BaseQMixin):

    '''manually balanced queue mixin'''

    _default_context = FourArmedContext

    def reup(self):
        '''put incoming things in incoming things as one incoming thing'''
        return self


class ManResultMixin(ResultQMixin, ManQMixin):

    '''manually balanced queue (with results extraction) mixin'''
