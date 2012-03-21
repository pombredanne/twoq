# -*- coding: utf-8 -*-
'''active twoq mixins'''

from threading import local
from collections import deque
from bisect import bisect_right

from stuf.utils import iterexcept, lazy

from twoq.mixins.queuing import QueueingMixin

from twoq.active.contexts import (
    AutoContext, ManContext, OneArmContext, TwoArmContext)

__all__ = ('AutoQMixin', 'ManQMixin')


class BaseQMixin(QueueingMixin):

    '''base active queue'''

    _onearm = OneArmContext
    _twoarm = TwoArmContext
    _auto = AutoContext
    _man = ManContext

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
        super(BaseQMixin, self).__init__(incoming, deque())
        # work queue
        self._scratch = deque()

    @lazy
    def _read(self):
        '''read-only queue'''
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

    def clear(self):
        '''clear every thing'''
        self.detap()
        self.outgoing.clear()
        self.incoming.clear()
        return self

    def inclear(self):
        '''clear incoming things'''
        self.incoming.clear()
        return self

    def outclear(self):
        '''clear outgoing things'''
        self.outgoing.clear()
        return self

    def _readclear(self):
        '''clear read-only queue'''
        self._read.clear()
        self._read.extend(self._incoming)
        return self

    ###########################################################################
    ## manipulate queues ######################################################
    ###########################################################################

    def append(self, thing):
        '''
        append thing to right side of incoming things

        @param thing: some thing
        '''
        self.incoming.append(thing)
        return self

    def appendleft(self, thing):
        '''
        append `thing` to left side of incoming things

        @param thing: some thing
        '''
        self.incoming.appendleft(thing)
        return self

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
        self.outgoing.extend(things)
        return self

    def extend(self, things):
        '''
        extend right side of incoming things with `things`

        @param thing: some things
        '''
        self.incoming.extend(things)
        return self

    def extendleft(self, things):
        '''
        extend left side of incoming things with `things`

        @param thing: some things
        '''
        self.incoming.extendleft(things)
        return self

    ###########################################################################
    ## queue rotation #########################################################
    ###########################################################################

    def reup(self):
        '''put incoming things in incoming things as one incoming thing'''
        with self._sync as sync:
            sync.append(list(self.incoming))
        return self

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
        # extend incoming things with outgoing things
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


class ResultQMixin(local):

    def end(self):
        '''return outgoing things and clear everything'''
        outgoing = self.outgoing
        results = outgoing.pop() if len(outgoing) == 1 else list(outgoing)
        self.clear()
        return results

    def results(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        for thing in iterexcept(self.outgoing.popleft, IndexError):
            yield thing

    def value(self):
        '''return outgoing things and clear outgoing things'''
        outgoing = self.outgoing
        results = outgoing.pop() if len(outgoing) == 1 else list(outgoing)
        outgoing.clear()
        return results

    def first(self):
        '''first incoming thing'''
        with self._sync as sync:
            sync.append(sync.iterable.popleft())
        return self

    def last(self):
        '''last incoming thing'''
        with self._sync as sync:
            sync.append(sync.iterable.pop())
        return self

    def peek(self):
        '''results of read-only mode'''
        return self._read[0] if len(
            self._read
        ) == 1 else list(self._read)


class AutoQMixin(BaseQMixin):

    '''auto-balancing queue mixin'''

    _default_context = _context = AutoContext
    _alt_context = ManContext

    def ro(self):
        '''enter read-only mode'''
        # swap context
        _context = self._alt_context
        return self._oro()

    def rw(self):
        '''enter read/write mode'''
        # swap context
        _context = self._default_context
        return self._owriteable()


class AutoResultMixin(AutoQMixin, BaseQMixin, ResultQMixin):

    '''auto-balancing manipulation queue (with results extractor) mixin'''


class ManQMixin(BaseQMixin):

    '''manually balanced queue mixin'''

    _default_context = _context = ManContext


class ManResultMixin(ManQMixin, BaseQMixin, ResultQMixin):

    '''manually balanced queue (with results extractor) mixin'''
