# -*- coding: utf-8 -*-
'''lazy twoq mixins'''

from itertools import tee

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
        super(baseq, self).__init__(incoming, None)

    ###########################################################################
    ## queue information ######################################################
    ###########################################################################

    def __contains__(self, value):
        return value in tee(self.outgoing, 1)

    _oicontains = __contains__

    def __len__(self):
        return len(tee(self.outgoing, 1))

    count = _oicount = __len__

    def outcount(self):
        '''count of outgoing items'''
        return len(tee(self.outgoing, 1))

    _ooutcount = outcount

    @property
    def balanced(self):
        '''if queues are balanced'''
        return len(tee(self.outgoing, 1)) == len(tee(self.incoming, 1))

    _obalanced = balanced

    def index(self, thing):
        '''
        insert thing into incoming things

        @param thing: some thing
        '''

    _oindex = index

    def end(self, _l=list, _ln=len):
        '''return outgoing things and clear'''
        results = self.pop() if _ln(self.outgoing) == 1 else _l(self.outgoing)
        self.clear()
        return results

    _ofinal = end

    def results(self, _iterexcept=exhaust):
        '''iterate over reversed outgoing things, clearing as it goes'''
        return self.outgoing

    _oresults = results

    def value(self, _l=list, _ln=len):
        '''return outgoing things and clear'''
        results = self.outgoing
        while not hasattr(results, 'pop'):
            try:
                results = results.next()
            except AttributeError:
                break
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
            sync.append(next(reversed(sync.iterable)))
        return self

    _olast = last

    ###########################################################################
    ## clear queues ###########################################################
    ###########################################################################

#    def __delitem__(self, index):
#        incoming = self.incoming
#        incoming.rotate(-index)
#        incoming.popleft()
#        incoming.rotate(index)
#
#    _oidelitem = __delitem__
#
#    def remove(self, thing):
#        '''
#        remove thing from incoming things
#
#        @param thing: some thing
#        '''
#        return self
#
#    _oiremove = remove

    def clear(self):
        '''clear all queues'''
        self._call = None
        self.outclear()
        self.inclear()
        return self

    _oclear = clear

    def inclear(self):
        '''incoming things clear'''
        self.incoming = None
        return self

    _oiclear = inclear

    def outclear(self):
        '''incoming things clear'''
        self.outgoing = None
        return self

    _ooutclear = outclear

    ###########################################################################
    ## manipulate queues ######################################################
    ###########################################################################

#    def append(self, thing):
#        '''incoming things right append'''
#        self._inappend(thing)
#        return self
#
#    _oappend = append
#
#    def appendleft(self, thing):
#        '''incoming things left append'''
#        self._inappendleft(thing)
#        return self
#
#    _oappendleft = appendleft
#
#    def insert(self, index, value):
#        '''
#        insert thing into incoming things
#
#        @param index: index position
#        @param thing: some thing
#        '''
#        incoming = self.incoming
#        incoming.rotate(-index)
#        incoming.popleft()
#        incoming.appendleft(value)
#        incoming.rotate(index)
#        return self
#
#    _oinsert = insert
#
#    def extend(self, things):
#        '''incoming things right extend'''
#        self._inextend(things)
#        return self
#
#    _oextend = extend
#
#    def extendleft(self, things):
#        '''incoming things left extend'''
#        self.incoming
#        return self
#
#    _oextendleft = extendleft

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
        self.outgoing, self.incoming = tee(self.outgoing)
        return self

    _oshift = shift

    def sync(self):
        '''
        shift incoming things to outgoing things, clearing incoming things
        '''
        # clear incoming items
        self.incoming = None
        # extend incoming items with outgoing items
        self.outgoing, self.incoming = tee(self.outgoing)
        return self

    _osync = sync

    def outshift(self):
        '''shift incoming things to outgoing things'''
        # extend incoming items with outgoing items
        self.outgoing, self.incoming = tee(self.incoming)
        return self

    _outshift = outshift

    def outsync(self):
        '''
        shift outgoing things to incoming things, clearing outgoing things
        '''
        # clear incoming items
        self.outgoing = None
        # extend incoming items with outgoing items
        self.outgoing, self.incoming = tee(self.incoming)
        return self

    _outsync = outsync


class AutoQMixin(baseq):

    '''auto balancing manipulation queue mixin'''

    @property
    def _sync(self):
        return AutoContext(self)


class ManQMixin(baseq):

    '''manually balanced manipulation queue mixin'''

    @property
    def _sync(self):
        return ManContext(self)
