# -*- coding: utf-8 -*-
'''lazy twoq mixins'''

from itertools import tee
from collections import deque

from twoq.mixins.queuing import QueueingMixin

from twoq.lazy.contexts import AutoContext, ManContext

__all__ = ['AutoQMixin', 'ManQMixin']


class BaseQMixin(QueueingMixin):

    '''base lazy queue'''

    def __init__(self, *args):
        # "extend" if just one argument
        incoming = iter([args[0]]) if len(args) == 1 else iter(args)
        self._scratch = None
        self._read = None
        super(BaseQMixin, self).__init__(incoming, iter([]))

    ###########################################################################
    ## queue information ######################################################
    ###########################################################################

    def __contains__(self, value):
        self.incoming, incoming = tee(self.incoming)
        return value in list(incoming)

    _o_contains = __contains__

    def __len__(self):
        self.incoming, incoming = tee(self.incoming)
        return len(list(incoming))

    count = _o_count = __len__

    def outcount(self):
        '''count of outgoing things'''
        self.outgoing, outgoing = tee(self.outgoing)
        return len(list(outgoing))

    _ooutcount = outcount

    @property
    def balanced(self):
        '''if queues are balanced'''
        self.incoming, incoming = tee(self.incoming)
        self.outgoing, outgoing = tee(self.outgoing)
        return len(list(outgoing)) == len(list(incoming))

    _obalanced = balanced

    def index(self, thing):
        '''
        index of thing in incoming things

        @param thing: some thing
        '''
        self.incoming, incoming = tee(self.incoming)
        return list(incoming).index(thing)

    _oindex = index

    ###########################################################################
    ## clear queues ###########################################################
    ###########################################################################

    def __delitem__(self, index):
        self.incoming = list(self.incoming)
        del self.incoming[index]
        self.incoming = iter(self.incoming)

    _o_delitem = __delitem__

    def remove(self, thing):
        '''
        remove thing from incoming things

        @param thing: some thing
        '''
        self.incoming = list(self.incoming)
        self.incoming.remove(thing)
        self.incoming = iter(self.incoming)
        return self

    _oiremove = remove

    def clear(self):
        '''clear every thing'''
        self.detap()
        self.outclear()
        self.inclear()
        return self

    _oclear = clear

    def inclear(self):
        '''clear incoming things'''
        self.incoming = iter([])
        return self

    _oiclear = inclear

    def outclear(self):
        '''clear outgoing things'''
        self.outgoing = iter([])
        return self

    _ooutclear = outclear

    def _sclear(self):
        '''clear scratch queue'''
        self._scratch = None
        return self

    _o_sclear = _sclear

    def _readclear(self):
        '''clear read-only queue'''
        self._read = None
        self._read, self._incoming = tee(self.incoming)
        return self

    _o_readclear = _readclear

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

    _oappend = append

    def appendleft(self, thing):
        '''
        append `thing` to left side of incoming things

        @param thing: some thing
        '''
        self.incoming = deque(self.incoming)
        self.incoming.appendleft(thing)
        self.incoming = iter(self.incoming)
        return self

    _oappendleft = appendleft

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

    _oinsert = insert

    def extend(self, things):
        '''
        extend right side of incoming things with `things`

        @param thing: some things
        '''
        self.incoming = deque(self.incoming)
        self.incoming.extend(things)
        self.incoming = iter(self.incoming)
        return self

    _oextend = extend

    def outextend(self, things):
        '''
        extend right side of outgoing things with `things`

        @param thing: some things
        '''
        outgoing = deque(self.outgoing)
        outgoing.extend(things)
        self.outgoing = iter(outgoing)
        return self

    _ooutextend = outextend

    def _sxtend(self, things):
        '''
        extend left side of scratch queue with `things`

        @param thing: some things
        '''
        self._scratch = deque(things)
        return self

    _o_sxtend = _sxtend

    def extendleft(self, things):
        '''
        extend left side of incoming things with `things`

        @param thing: some things
        '''
        self.incoming = deque(self.incoming)
        self.incoming.extendleft(things)
        self.incoming = iter(self.incoming)
        return self

    _oextendleft = extendleft

    ###########################################################################
    ## balance queues #########################################################
    ###########################################################################

    def shift(self):
        '''shift outgoing things to incoming things'''
        self.outgoing, self.incoming = tee(self.outgoing)
        return self

    _oshift = _osync = sync = shift

    def outshift(self):
        '''shift incoming things to outgoing things'''
        self.outgoing, self.incoming = tee(self.incoming)
        return self

    _outshift = _outsync = outsync = outshift


class ResultQMixin(BaseQMixin):

    def end(self):
        '''return outgoing things and clear out all things'''
        results = list(self.outgoing)
        results = results.pop() if len(results) == 1 else list(results)
        self.clear()
        return results

    _ofinal = end

    def results(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        return self.outgoing

    _oresults = results

    def value(self):
        '''return outgoing things and clear outgoing things'''
        results = list(self.outgoing)
        results = results.pop() if len(results) == 1 else list(results)
        self.outclear()
        return results

    _ovalue = value

    def first(self):
        '''first incoming thing'''
        with self._sync() as sync:
            sync.append(next(sync.iterable))
        return self

    _ofirst = first

    def last(self):
        '''last incoming thing'''
        with self._sync() as sync:
            i1, _ = tee(sync.iterable)
            sync.append(deque(i1, maxlen=1).pop())
        return self

    _olast = last

    def peek(self):
        '''see results of read-only mode'''
        measure, results = tee(self._read)
        return list(results)[0] if len(measure) == 1 else list(results)

    _opeek = peek


class AutoQMixin(BaseQMixin):

    '''auto-balancing queue mixin'''

    _default_context = _context = AutoContext
    _alt_context = ManContext

    def ro(self):
        '''enter read-only mode'''
        # swap context
        _context = self._alt_context
        return self._oro()

    _aread_only = ro

    def rw(self):
        '''enter read/write mode'''
        # swap context
        _context = self._default_context
        return self._orw()

    _aread_write = rw

    def reup(self):
        '''put incoming things in incoming things as one incoming thing'''
        with self._sync() as _sync:
            _sync.append(list(self.incoming))
        return self

    _oreup = reup


class AutoResultMixin(ResultQMixin, AutoQMixin):

    '''auto-balancing queue (with results extraction) mixin'''


class ManQMixin(BaseQMixin):

    '''manually balanced queue mixin'''

    _context = ManContext

    def reup(self):
        '''put incoming things in incoming things as one incoming thing'''
        return self

    _oreup = reup


class ManResultMixin(ResultQMixin, ManQMixin):

    '''manually balanced queue (with results extraction) mixin'''
