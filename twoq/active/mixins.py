# -*- coding: utf-8 -*-
'''active twoq mixins'''

from collections import deque
from bisect import bisect_right

from twoq.support import iterexcept
from twoq.mixins.queuing import QueueingMixin

from twoq.active.contexts import AutoContext, ManContext, SyncContext

__all__ = ['AutoQMixin', 'ManQMixin', 'SyncContext']


class baseq(QueueingMixin):

    '''base active queue'''

    def __init__(self, incoming, outgoing):
        '''
        init

        @param incoming: incoming queue
        @param outgoing: outgoing queue
        '''
        super(baseq, self).__init__(incoming, outgoing)
        #######################################################################
        ## incoming things ####################################################
        #######################################################################
        # incoming things right append
        self._inappend = self.incoming.append
        # incoming things left append
        self._inappendleft = self.incoming.appendleft
        # incoming things clear
        self._inclear = self.incoming.clear
        # incoming things right extend
        self._inextend = self.incoming.extend
        # incoming things left extend
        self._inextendleft = self.incoming.extendleft
        #######################################################################
        ## outgoing things ####################################################
        #######################################################################
        # outgoing things right append
        self._outappend = self.outgoing.append
        # outgoing things right extend
        self._outextend = self.outgoing.extend
        # outgoing things clear
        self._outclear = self.outgoing.clear
        # outgoing things right pop
        self.pop = self.outgoing.pop
        # outgoing things left pop
        self.popleft = self.outgoing.popleft

    ###########################################################################
    ## queue information ######################################################
    ###########################################################################

    def __contains__(self, value):
        return value in self.incoming

    def __len__(self):
        return len(self.incoming)

    count = __len__

    def outcount(self):
        '''count of outgoing items'''
        return len(self.outgoing)

    @property
    def balanced(self):
        '''if queues are balanced'''
        return len(self.outgoing) == len(self.incoming)

    def index(self, thing, _bisect_right=bisect_right):
        '''
        insert thing into incoming things

        @param thing: some thing
        '''
        return _bisect_right(self.incoming, thing) - 1

    def final(self, _l=list, _ln=len):
        '''return outgoing things and clear'''
        results = self.pop() if _ln(self.outgoing) == 1 else _l(self.outgoing)
        self.clear()
        return results

    def results(self, _iterexcept=iterexcept):
        '''iterate over reversed outgoing things, clearing as it goes'''
        for thing in _iterexcept(self.outgoing.popleft, IndexError):
            yield thing

    def value(self, _l=list, _ln=len):
        '''return outgoing things and clear'''
        results = self.pop() if _ln(self.outgoing) == 1 else _l(self.outgoing)
        self._outclear()
        return results

    def first(self):
        '''first thing among incoming things'''
        with self._sync as sync:
            sync.append(sync.iterable.popleft())
        return self

    def last(self):
        '''last thing among incoming things'''
        with self._sync as sync:
            sync.append(sync.iterable.pop())
        return self

    ###########################################################################
    ## clear queues ###########################################################
    ###########################################################################

    def __delitem__(self, index):
        incoming = self.incoming
        incoming.rotate(-index)
        incoming.popleft()
        incoming.rotate(index)

    def remove(self, thing, _bisect_right=bisect_right):
        '''
        remove thing from incoming things

        @param thing: some thing
        '''
        incoming = self.incoming
        position = _bisect_right(incoming, thing) - 1
        incoming.rotate(-position)
        incoming.popleft()
        incoming.rotate(position)
        return self

    def clear(self):
        '''clear all queues'''
        self._call = None
        self._outclear()
        self._inclear()
        return self

    def inclear(self):
        '''incoming things clear'''
        self._inclear()
        return self

    def outclear(self):
        '''incoming things clear'''
        self._inclear()
        return self

    ###########################################################################
    ## manipulate queues ######################################################
    ###########################################################################

    def append(self, thing):
        '''incoming things right append'''
        self._inappend(thing)
        return self

    def appendleft(self, thing):
        '''incoming things left append'''
        self._inappendleft(thing)
        return self

    def insert(self, index, value):
        '''
        insert thing into incoming things

        @param index: index position
        @param thing: some thing
        '''
        incoming = self.incoming
        incoming.rotate(-index)
        incoming.popleft()
        incoming.appendleft(value)
        incoming.rotate(index)
        return self

    def extend(self, things):
        '''incoming things right extend'''
        self._inextend(things)
        return self

    def extendleft(self, things):
        '''incoming things left extend'''
        self._inextendleft(things)
        return self

    def reverse(self, _reversed=None):
        '''iterate over reversed incoming things, clearing as it goes'''
        self.outgoing.extendleft(self.incoming)
        self._inclear()
        self._inextend(self.outgoing)
        return self

    ###########################################################################
    ## balance queues #########################################################
    ###########################################################################

    def reup(self, _list=list):
        '''put incoming things in incoming things as one incoming thing'''
        with self._sync as _sync:
            _sync.append(_list(self.incoming))
        return self

    def shift(self):
        '''shift incoming things to outgoing things'''
        self._inextend(self.outgoing)
        return self

    def sync(self):
        '''
        shift incoming things to outgoing things, clearing incoming things
        '''
        # clear incoming items
        self._inclear()
        # extend incoming items with outgoing items
        self._inextend(self.outgoing)
        return self

    def outshift(self):
        '''shift outgoing things to incoming things'''
        # extend incoming items with outgoing items
        self._outextend(self.incoming)
        return self

    def outsync(self):
        '''
        shift outgoing things to incoming things, clearing outgoing things
        '''
        # clear incoming items
        self._outclear()
        # extend incoming items with outgoing items
        self._outextend(self.incoming)
        return self


class _dq(baseq):

    def __init__(self, *args):
        incoming = deque()
        # extend if just one argument
        if len(args) == 1:
            incoming.append(args[0])
        else:
            incoming.extend(args)
        super(_dq, self).__init__(incoming, deque())


class scratchq(_dq):

    def __init__(self, *args):
        super(scratchq, self).__init__(*args)
        #######################################################################
        ## scratch queue ######################################################
        #######################################################################
        self._scratch = deque()
        # outgoing things right append
        self._sappend = self._scratch.append
        # outgoing things right extend
        self._sxtend = self._scratch.extend
        # scratch clear
        self._sclear = self._scratch.clear
        # scratch pop left
        self._spopleft = self._scratch.popleft


class AutoQMixin(scratchq):

    '''auto balancing manipulation queue mixin'''

    @property
    def _sync(self):
        return AutoContext(self)


class ManQMixin(scratchq):

    '''manually balanced manipulation queue mixin'''

    @property
    def _sync(self):
        return ManContext(self)


class SyncQMixin(_dq):

    '''synchronized manipulation queue'''

    @property
    def _sync(self):
        return SyncContext(self)
