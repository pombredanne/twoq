# -*- coding: utf-8 -*-
'''lazy twoq mixins'''

from itertools import tee
from collections import deque

from stuf.utils import exhaust

from twoq.mixins.queuing import QueueingMixin

from twoq.lazy.contexts import AutoContext, ManContext

__all__ = ['AutoQMixin', 'ManQMixin']


class baseq(QueueingMixin):

    '''base lazy queue'''

    def __init__(self, *args):
        # extend if just one argument
        if len(args) == 1:
            incoming = iter([args[0]])
        else:
            incoming = iter(args)
        self._scratch = None
        super(baseq, self).__init__(incoming, iter([]))

    ###########################################################################
    ## queue information ######################################################
    ###########################################################################

    def __contains__(self, value):
        self.incoming, incoming = tee(self.incoming)
        return value in list(incoming)

    _oicontains = __contains__

    def __len__(self):
        self.incoming, incoming = tee(self.incoming)
        return len(list(incoming))

    count = _oicount = __len__

    def outcount(self):
        '''count of outgoing items'''
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
        index of item in incoming things

        @param thing: some thing
        '''
        self.incoming, incoming = tee(self.incoming)
        return list(incoming).index(thing)

    _oindex = index

    def end(self, _l=list, _ln=len):
        '''return outgoing things and clear'''
        results = list(self.outgoing)
        results = self.pop() if _ln(results) == 1 else _l(results)
        self.clear()
        return results

    _ofinal = end

    def results(self, _iterexcept=exhaust):
        '''iterate over reversed outgoing things, clearing as it goes'''
        return self.outgoing

    _oresults = results

    def value(self, _l=list, _ln=len):
        '''return outgoing things and clear'''
        results = list(self.outgoing)
        results = results.pop() if _ln(results) == 1 else results
        self.outclear()
        return results

    _ovalue = value

    def first(self):
        '''first thing among incoming things'''
        with self._sync as sync:
            sync.append(next(sync.iterable))
        return self

    _ofirst = first

    def last(self):
        '''last thing among incoming things'''
        with self._sync as sync:
            i1, _ = tee(sync.iterable)
            sync.append(deque(i1, maxlen=1).pop())
        return self

    _olast = last

    ###########################################################################
    ## clear queues ###########################################################
    ###########################################################################

    def __delitem__(self, index):
        self.incoming = list(self.incoming)
        del self.incoming[index]
        self.incoming = iter(self.incoming)

    _oidelitem = __delitem__

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
        '''clear all queues'''
        self._call = None
        self.outclear()
        self.inclear()
        return self

    _oclear = clear

    def inclear(self):
        '''incoming things clear'''
        self.incoming = iter([])
        return self

    _oiclear = inclear

    def outclear(self):
        '''incoming things clear'''
        self.outgoing = iter([])
        return self

    _ooutclear = outclear

    ###########################################################################
    ## manipulate queues ######################################################
    ###########################################################################

    def append(self, thing):
        '''incoming things right append'''
        self.incoming = deque(self.incoming)
        self.incoming.append(thing)
        self.incoming = iter(self.incoming)
        return self

    _oappend = append

    def appendleft(self, thing):
        '''incoming things left append'''
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
        '''incoming things right extend'''
        self.incoming = deque(self.incoming)
        self.incoming.extend(things)
        self.incoming = iter(self.incoming)
        return self

    _oextend = extend

    def extendleft(self, things):
        '''incoming things left extend'''
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

    _osync = sync

    def outshift(self):
        '''shift incoming things to outgoing things'''
        self.outgoing, self.incoming = tee(self.incoming)
        return self

    _outshift = _outsync = outsync = outshift


class AutoQMixin(baseq):

    '''auto balancing manipulation queue mixin'''

    def reup(self, _list=list):
        '''put incoming things in incoming things as one incoming thing'''
        with self._sync as _sync:
            _sync.append(_list(self.incoming))
        return self

    _oreup = reup

    @property
    def _sync(self):
        return AutoContext(self)


class ManQMixin(baseq):

    '''manually balanced manipulation queue mixin'''

    @property
    def _sync(self):
        return ManContext(self)

    def reup(self, _list=list):
        '''put incoming things in incoming things as one incoming thing'''
        return self
