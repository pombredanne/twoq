# -*- coding: utf-8 -*-
'''twoq queuing mixins'''

from threading import local
from collections import deque
from itertools import islice, chain, tee, starmap

from stuf.utils import imap

__all__ = ['QueueingMixin']


class QueueingMixin(local):

    '''queue management mixin'''

    def __init__(self, incoming, outgoing):
        '''
        init

        @param incoming: incoming things
        @param outgoing: outgoing things
        '''
        super(QueueingMixin, self).__init__()
        # incoming queue
        self.incoming = incoming
        # outgoing queue
        self.outgoing = outgoing
        # set defaults
        self.detap().unswap()

    def __iter__(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        return self._iterator(self._outq)

    def _split(self, iterable, n=2):
        return tee(iterable, n)

    def _join(self, *iterables):
        return chain(*iterables)

    def _xmap(self, call, iterable=False):
        '''
        invoke call on each incoming thing

        @param call: a callable
        @param iterable: an iterable
        '''
        iterable = self._iterable if not iterable else iterable
        return self._pre()._extend(imap(call, self._iterable))

    def _xstarmap(self, call, iterable=False):
        '''
        invoke 'call' on each sequence of incoming things

        @param call: a callable
        @param iterable: an iterable
        '''
        iterable = self._iterable if not iterable else iterable
        return self._pre()._extend(starmap(call, self._iterable))

    @property
    def balanced(self):
        '''if queues are balanced'''
        return self.outcount() == self.__len__()

    @property
    def _iterable(self):
        '''iterable'''
        return self._iterator(self._workq)

    ###########################################################################
    ## queue clearance ########################################################
    ###########################################################################

    def _wclear(self):
        '''clear work queue'''
        return self.ctx1(workq='_work')._pre()._clear().unswap()

    def _uclear(self):
        '''clear utility queue'''
        return self.ctx1(workq='_util')._pre()._clear().unswap()

    def clear(self):
        '''clear every thing'''
        return self.detap().outclear().inclear()

    def inclear(self):
        '''clear incoming things'''
        return self.ctx1()._pre()._clear().unswap()

    def outclear(self):
        '''clear outgoing things'''
        return self.ctx1(workq='outgoing')._pre()._clear().unswap()

    ###########################################################################
    ## context management #####################################################
    ###########################################################################

    def ro(self):
        '''switch to read-only mode'''
        return self.ctx3(outq='_util')._pre()._extend(
            self._iterable
        ).ctx1(workq='_util')

    def ctx1(self, **kw):
        '''switch to ctx1-armed context manager'''
        self._workq = self._utilq = kw.pop('workq', 'incoming')
        # clear out outgoing things before extending them?
        self._clearout = kw.pop('clearout', True)
        self._pre = lambda: self
        self._post = lambda: self
        return self

    def ctx2(self, **kw):
        '''switch to two-armed context manager'''
        # clear out outgoing things before extending them?
        self._clearout = kw.pop('clearout', True)
        self._workq = kw.pop('workq', '_work')
        self._outq = kw.pop('outq', 'incoming')
        self._pre = self._oq2wq
        self._post = self._uq2oq
        return self

    def ctx4(self, **kw):
        '''switch to four-armed context manager'''
        self._pre = self._iq2wq
        self._post = self._uq2oq
        self._clearout = kw.pop('clearout', True)
        return self.swap(**kw)

    def autoctx(self, **kw):
        '''switch to auto-synchronizing context manager'''
        self._pre = self._iq2wq
        self._post = self._uq2iqoq
        return self.swap(**kw)

    def swap(self, **kw):
        '''swap queues'''
        # clear out outgoing things before extending them?
        self._clearout = kw.pop('clearout', True)
        # incoming queue
        self._inq = kw.get('inq', 'incoming')
        # outcoming queue
        self._outq = kw.get('outq', 'outgoing')
        # work queue
        self._workq = kw.get('workq', '_work')
        # utility queue
        self._utilq = kw.get('utilq', '_util')
        return self

    def unswap(self):
        '''rotate queues to default'''
        self._pre = getattr(self, '_iq2wq')
        self._post = getattr(self, self._default_post)
        return self.swap()

    rw = unswap

    ###########################################################################
    ## current callable management ############################################
    ###########################################################################

    def args(self, *args, **kw):
        '''arguments for active callable'''
        # set positional arguments
        self._args = args
        # set keyword arguemnts
        self._kw = kw
        return self

    def tap(self, call):
        '''
        set active callable

        @param call: a call
        '''
        self.detap()
        # set active callable
        self._call = call
        return self

    def detap(self):
        '''clear active callable'''
        # reset postitional arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # reset callable
        self._call = None
        return self

    def wrap(self, call):
        '''build active callable from factory'''
        def factory(*args, **kw):
            return call(*args, **kw)
        return self.tap(factory)

    # alias
    unwrap = detap

    ###########################################################################
    ## queue rotation #########################################################
    ###########################################################################

    def ahead(self, n=None):
        '''
        move iterator for incoming things `n`-steps ahead

        If `n` is `None`, consume entirely.

        @param n: number of steps to advance incoming things (default: None)
        '''
        # use functions that consume iterators at C speed.
        if n is None:
            # feed the entire iterator into a zero-length `deque`
            self.incoming = deque(self.incoming, maxlen=0)
        else:
            # advance to the empty slice starting at position `n`
            next(islice(self.incoming, n, n), None)
        return self

    def reup(self):
        '''put incoming things in incoming things as one incoming thing'''
        return self.ctx1()._pre()._append(list(self._iterable)).unswap()

    def shift(self):
        '''shift outgoing things to incoming things'''
        return self.autoctx(inq='outgoing', outq='incoming')._pre()._extend(
            self._iterable
        ).unswap()

    sync = shift

    def outshift(self):
        '''shift incoming things to outgoing things'''
        return self.autoctx()._pre()._extend(self._iterable).unswap()

    outsync = outshift

    ###########################################################################
    ## queue appending ########################################################
    ###########################################################################

    def append(self, thing):
        '''
        append thing to right side of incoming things

        @param thing: some thing
        '''
        return self.ctx1()._pre()._append(thing).unswap()

    def appendleft(self, thing):
        '''
        append `thing` to left side of incoming things

        @param thing: some thing
        '''
        return self.ctx2()._pre()._appendleft(thing).unswap()

    ###########################################################################
    ## queue extension ########################################################
    ###########################################################################

    def outextend(self, things):
        '''
        extend right side of outgoing things with `things`

        @param thing: some things
        '''
        return self.ctx1(workq='outgoing')._pre()._extend(things).unswap()

    def extend(self, things):
        '''
        extend right side of incoming things with `things`

        @param thing: some things
        '''
        return self.ctx1()._pre()._extend(things).unswap()

    def extendleft(self, things):
        '''
        extend left side of incoming things with `things`

        @param thing: some things
        '''
        return self.ctx1()._pre()._extendleft(things).unswap()


class ResultMixin(local):

    '''result queue mixin'''

    def end(self):
        '''return outgoing things and clear everything'''
        results, measure = self._split(self.outgoing)
        results = next(results) if len(list(measure)) == 1 else list(results)
        self.clear()
        return results

    def value(self):
        '''return outgoing things and clear outgoing things'''
        results, measure = self._split(self.outgoing)
        results = next(results) if len(list(measure)) == 1 else list(results)
        self.outclear()
        return results

    def first(self):
        '''first incoming thing'''
        return self._pre()._append(next(self._iterable))

    def last(self):
        '''last incoming thing'''
        self._pre()
        i1, _ = self._split(self._iterable)
        self._append(deque(i1, maxlen=1).pop())
        return self

    def peek(self):
        '''results in read-only mode'''
        results = list(self._util)
        return results[0] if len(results) == 1 else results

    def results(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        return self.__iter__()
