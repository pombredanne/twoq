# -*- coding: utf-8 -*-
'''active twoq mixins'''

from collections import deque
from bisect import bisect_right

from stuf.utils import iterexcept

from twoq.mixins.queuing import QueueingMixin

from twoq.active.contexts import AutoContext, ManContext, SyncContext

__all__ = ('AutoQMixin', 'ManQMixin', 'SyncQMixin')


class baseq(QueueingMixin):

    '''base active queue'''

    def __init__(self, *args):
        '''
        init

        @param incoming: incoming queue
        @param outgoing: outgoing queue
        '''
        incoming = deque()
        # extend if just one argument
        if len(args) == 1:
            incoming.append(args[0])
        else:
            incoming.extend(args)
        super(baseq, self).__init__(incoming, deque())
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

    _oicontains = __contains__

    def __len__(self):
        return len(self.incoming)

    count = _oicount = __len__

    def outcount(self):
        '''count of outgoing items'''
        return len(self.outgoing)

    _ooutcount = outcount

    @property
    def balanced(self):
        '''if queues are balanced'''
        return len(self.outgoing) == len(self.incoming)

    _obalanced = balanced

    def index(self, thing, _bisect_right=bisect_right):
        '''
        insert thing into incoming things

        @param thing: some thing
        '''
        return _bisect_right(self.incoming, thing) - 1

    _oindex = index

    def end(self, _l=list, _ln=len):
        '''return outgoing things and clear'''
        results = self.pop() if _ln(self.outgoing) == 1 else _l(self.outgoing)
        self.clear()
        return results

    _ofinal = end

    def results(self, _iterexcept=iterexcept):
        '''iterate over reversed outgoing things, clearing as it goes'''
        for thing in _iterexcept(self.outgoing.popleft, IndexError):
            yield thing

    _oresults = results

    def value(self, _l=list, _ln=len):
        '''return outgoing things and clear'''
        results = self.pop() if _ln(self.outgoing) == 1 else _l(self.outgoing)
        self._outclear()
        return results

    _ovalue = value

    def first(self):
        '''first thing among incoming things'''
        with self._sync as sync:
            sync.append(sync.iterable.popleft())
        return self

    _ofirst = first

    def last(self):
        '''last thing among incoming things'''
        with self._sync as sync:
            sync.append(sync.iterable.pop())
        return self

    _olast = last

    ###########################################################################
    ## clear queues ###########################################################
    ###########################################################################

    def __delitem__(self, index):
        incoming = self.incoming
        incoming.rotate(-index)
        incoming.popleft()
        incoming.rotate(index)

    _oidelitem = __delitem__

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

    _oiremove = remove

    def clear(self):
        '''clear all queues'''
        self._call = None
        self._outclear()
        self._inclear()
        return self

    _oclear = clear

    def inclear(self):
        '''incoming things clear'''
        self._inclear()
        return self

    _oiclear = inclear

    def outclear(self):
        '''incoming things clear'''
        self._inclear()
        return self

    _ooutclear = outclear

    ###########################################################################
    ## manipulate queues ######################################################
    ###########################################################################

    def append(self, thing):
        '''incoming things right append'''
        self._inappend(thing)
        return self

    _oappend = append

    def appendleft(self, thing):
        '''incoming things left append'''
        self._inappendleft(thing)
        return self

    _oappendleft = appendleft

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

    _oinsert = insert

    def extend(self, things):
        '''incoming things right extend'''
        self._inextend(things)
        return self

    _oextend = extend

    def extendleft(self, things):
        '''incoming things left extend'''
        self._inextendleft(things)
        return self

    _oextendleft = extendleft

    ###########################################################################
    ## balance queues #########################################################
    ###########################################################################

    def reup(self, _list=list):
        '''put incoming things in incoming things as one incoming thing'''
        with self._sync as _sync:
            _sync.append(_list(self.incoming))
        return self

    _oreup = reup

    def shift(self):
        '''shift incoming things to outgoing things'''
        self._inextend(self.outgoing)
        return self

    _oshift = shift

    def sync(self):
        '''
        shift incoming things to outgoing things, clearing incoming things
        '''
        # clear incoming items
        self._inclear()
        # extend incoming items with outgoing items
        self._inextend(self.outgoing)
        return self

    _osync = sync

    def outshift(self):
        '''shift outgoing things to incoming things'''
        # extend incoming items with outgoing items
        self._outextend(self.incoming)
        return self

    _outshift = outshift

    def outsync(self):
        '''
        shift outgoing things to incoming things, clearing outgoing things
        '''
        # clear incoming items
        self._outclear()
        # extend incoming items with outgoing items
        self._outextend(self.incoming)
        return self

    _outsync = outsync


class scratchq(baseq):

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


class SyncQMixin(baseq):

    '''synchronized manipulation queue'''

    @property
    def _sync(self):
        return SyncContext(self)
