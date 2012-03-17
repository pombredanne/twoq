# -*- coding: utf-8 -*-
'''active twoq mixins'''

from threading import local
from collections import deque
from bisect import bisect_right

from stuf.utils import iterexcept

from twoq.mixins.queuing import QueueingMixin

from twoq.active.contexts import AutoContext, ManContext, SyncContext

__all__ = ('AutoQMixin', 'ManQMixin', 'SyncQMixin')


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
        super(BaseQMixin, self).__init__(incoming, deque())
        #######################################################################
        ## incoming things ####################################################
        #######################################################################
        # incoming things right append
        self._inappend = self.__inappend = self.incoming.append
        # incoming things left append
        self._inappendleft = self.__inappendleft = self.incoming.appendleft
        # incoming things clear
        self._inclear = self.__inclear = self.incoming.clear
        # incoming things right extend
        self._inextend = self.__inextend = self.incoming.extend
        # incoming things left extend
        self._inextendleft = self.__inextendleft = self.incoming.extendleft
        #######################################################################
        ## outgoing things ####################################################
        #######################################################################
        # outgoing things right append
        self._outappend = self.__outappend = self.outgoing.append
        # outgoing things right extend
        self._outextend = self.__outextend = self.outgoing.extend
        # outgoing things clear
        self._outclear = self.__outclear = self.outgoing.clear
        # outgoing things right pop
        self.pop = self.__pop = self.outgoing.pop
        # outgoing things left pop
        self.popleft = self.__popleft = self.outgoing.popleft

    ###########################################################################
    ## queue information ######################################################
    ###########################################################################

    def __contains__(self, thing):
        return thing in self.incoming

    _oicontains = __contains__

    def __len__(self):
        return len(self.incoming)

    count = _oicount = __len__

    def outcount(self):
        '''count of outgoing things'''
        return len(self.outgoing)

    _ooutcount = outcount

    @property
    def balanced(self):
        '''if queues are balanced'''
        return len(self.outgoing) == len(self.incoming)

    _obalanced = balanced

    def index(self, thing):
        '''
        insert thing into incoming things

        @param thing: some thing
        '''
        return bisect_right(self.incoming, thing) - 1

    _oindex = index

    ###########################################################################
    ## clear queues ###########################################################
    ###########################################################################

    def __delitem__(self, index):
        incoming = self.incoming
        incoming.rotate(-index)
        incoming.popleft()
        incoming.rotate(index)

    _oidelitem = __delitem__

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

    _oiremove = remove

    def clear(self):
        '''clear every thing'''
        self.detap()
        self.__outclear()
        self.__inclear()
        return self

    _oclear = clear

    def inclear(self):
        '''clear incoming things'''
        self.__inclear()
        return self

    _oiclear = inclear

    def outclear(self):
        '''clear outgoing things'''
        self.__outclear()
        return self

    _ooutclear = outclear

    ###########################################################################
    ## manipulate queues ######################################################
    ###########################################################################

    def append(self, thing):
        '''
        append thing to right side of incoming things

        @param thing: some thing
        '''
        self.__inappend(thing)
        return self

    _oappend = append

    def appendleft(self, thing):
        '''
        append `thing` to left side of incoming things

        @param thing: some thing
        '''
        self.__inappendleft(thing)
        return self

    _oappendleft = appendleft

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

    _oinsert = insert

    def outextend(self, things):
        '''
        extend right side of outgoing things with `things`

        @param thing: some things
        '''
        self.__outextend(things)
        return self

    def extend(self, things):
        '''
        extend right side of incoming things with `things`

        @param thing: some things
        '''
        self.__inextend(things)
        return self

    _oextend = extend

    def extendleft(self, things):
        '''
        extend left side of incoming things with `things`

        @param thing: some things
        '''
        self.__inextendleft(things)
        return self

    _oextendleft = extendleft

    ###########################################################################
    ## balance queues #########################################################
    ###########################################################################

    def reup(self):
        '''put incoming things in incoming things as one incoming thing'''
        with self._sync as _sync:
            _sync.append(list(self.incoming))
        return self

    _oreup = reup

    def shift(self):
        '''shift outgoing things to incoming things'''
        self.__inextend(self.outgoing)
        return self

    _oshift = shift

    def sync(self):
        '''
        shift outgoing things to incoming things, clearing incoming things
        '''
        # clear incoming things
        self.__inclear()
        # extend incoming things with outgoing things
        self.__inextend(self.outgoing)
        return self

    _osync = sync

    def outshift(self):
        '''shift incoming things to outgoing things'''
        # extend incoming things with outgoing things
        self.__outextend(self.incoming)
        return self

    _outshift = outshift

    def outsync(self):
        '''
        shift incoming things to outgoing things, clearing outgoing things
        '''
        # clear incoming things
        self.__outclear()
        # extend incoming things with outgoing things
        self.__outextend(self.incoming)
        return self

    _outsync = outsync


class ScratchQMixin(BaseQMixin):

    def __init__(self, *args):
        super(ScratchQMixin, self).__init__(*args)
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


class ResultQMixin(local):

    def end(self):
        '''return outgoing things and clear out all things'''
        results = self.pop() if len(
            self.outgoing
        ) == 1 else list(self.outgoing)
        self.clear()
        return results

    _oend = end

    def results(self):
        '''yield outgoing things and clear outgoing things'''
        for thing in iterexcept(self.popleft, IndexError):
            yield thing

    _oresults = results

    def value(self):
        '''return outgoing things and clear outgoing things'''
        results = self.pop() if len(
            self.outgoing
        ) == 1 else list(self.outgoing)
        self._outclear()
        return results

    _ovalue = value

    def first(self):
        '''first incoming thing'''
        with self._sync as sync:
            sync.append(sync.iterable.popleft())
        return self

    _ofirst = first

    def last(self):
        '''last incoming thing'''
        with self._sync as sync:
            sync.append(sync.iterable.pop())
        return self

    _olast = last


class AutoQMixin(ScratchQMixin):

    '''auto balancing manipulation queue mixin'''

    @property
    def _sync(self):
        return AutoContext(self)


class AutoResultMixin(AutoQMixin, BaseQMixin, ResultQMixin):

    '''auto balancing manipulation queue mixin'''


class ManQMixin(ScratchQMixin):

    '''manually balanced manipulation queue mixin'''

    @property
    def _sync(self):
        return ManContext(self)


class ManResultMixin(ManQMixin, BaseQMixin, ResultQMixin):

    '''manually balanced manipulation queue mixin'''


class SyncQMixin(BaseQMixin):

    '''synchronized manipulation queue'''

    @property
    def _sync(self):
        return SyncContext(self)


class SyncResultMixin(SyncQMixin, BaseQMixin, ResultQMixin):

    '''synchronized manipulation queue'''
