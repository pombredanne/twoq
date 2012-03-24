# -*- coding: utf-8 -*-
'''twoq queuing mixins'''

from threading import local
from collections import deque
from itertools import islice, tee, chain

__all__ = ['QueueingMixin']


class QueueingMixin(local):

    '''queue management mixin'''

    _default_pre = '_iq2wq'

    def __init__(self, incoming, outgoing):
        '''
        init

        @param incoming: incoming things
        @param outgoing: outgoing things
        '''
        super(QueueingMixin, self).__init__()
        # callable stub
        self._call = None
        # callable postitional arguments stub
        self._args = ()
        # callable keyword arguments stub
        self._kw = {}
        # incoming queue
        self.incoming = incoming
        # outgoing queue
        self.outgoing = outgoing
        # queue pointers -> incoming queue label
        self._inq = 'incoming'
        # queue pointers -> outgoing queue label
        self._outq = 'outgoing'
        # queue pointers -> work queue label
        self._workq = '_work'
        # queue pointers -> utility queue label
        self._utilq = '_util'
        # context pointers -> default context manager
        self._context = self._default_context
        # clear out outgoing queue
        self._clearout = True

    def __iter__(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        return self._iterator(self, self._outq)

    @property
    def balanced(self):
        '''if queues are balanced'''
        return self.outcount() == self.__len__()

    @property
    def _iterable(self):
        '''iterable'''
        return self._iterator(self._workq)

    def _split(self, iterable, n=2):
        return tee(iterable, n)

    def _join(self, *iterables):
        return chain(*iterables)

    def _wclear(self):
        '''clear work queue'''
        return self.ctx1('_work').clear().unswap()

    def _uclear(self):
        '''clear utility queue'''
        return self.ctx1('_util').clear().unswap()

    def clear(self):
        '''clear every thing'''
        return self.detap().outclear().inclear()

    def inclear(self):
        '''clear incoming things'''
        return self.ctx1()._clear().unswap()

    def outclear(self):
        '''clear outgoing things'''
        return self.ctx1('outgoing').clear().unswap()

    def ro(self):
        '''switch to read-only mode'''
        return self.ctx3(outq='_util')._extend(
            self._iterable
        ).unswap().ctx1('_util')

    def ctx1(self, workq='incoming'):
        '''switch to ctx1-armed context manager'''
        self._workq = workq
        self._pre = lambda: self
        self._post = lambda: self
        return self

    def ctx2(self, workq='_work', outq='incoming'):
        '''switch to two-armed context manager'''
        self._workq = workq
        self._outq = outq
        self._pre = self._oq2wq
        self._post = self._uq2oq
        return self

    def ctx3(self, workq='_work', outq='outgoing', inq='incoming'):
        '''switch to three-armed context manager'''
        self._workq = workq
        self._outq = outq
        self._inq = inq
        self._pre = self._iq2wq
        self._post = self._uq2oq
        return self

    def ctx4(self, **kw):
        '''switch to four-armed context manager'''
        self._pre = self._iq2wq
        self._post = self._uq2oq
        return self.swap(**kw)

    def autoctx(self, **kw):
        '''switch to auto-synchronizing context manager'''
        self._pre = self._iq2wq
        self._post = self._uq2iqoq
        return self.swap(**kw)

    def swap(self, **kw):
        '''swap queues'''
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
        self._pre = getattr(self, '_default_pre')
        self._post = getattr(self, '_default_post')
        return self.swap()

    rw = unswap

    @property
    def _sync(self):
        '''synchronization context'''
        return self._context(
            self,
            inq=self._inq,
            outq=self._outq,
            workq=self._workq,
            utilq=self._utilq,
        )

    def args(self, *args, **kw):
        '''arguments for active callable'''
        # set positional arguments
        self._args = args
        # set keyword arguemnts
        self._kw.update(kw)
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
        self._kw.clear()
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
        self.ctx1()._append(list(self._iterable))
        return self.unswap()

    def shift(self):
        '''shift outgoing things to incoming things'''
        return self.autoctx(inq='outgoing', outq='incoming')._extend(
            self._iterable
        ).unswap()

    sync = shift

    def outshift(self):
        '''shift incoming things to outgoing things'''
        return self.autoctx()._extend(self._iterable).unswap()

    outsync = outshift

    def append(self, thing):
        '''
        append thing to right side of incoming things

        @param thing: some thing
        '''
        return self.ctx1()._append(thing).self.unswap()

    def appendleft(self, thing):
        '''
        append `thing` to left side of incoming things

        @param thing: some thing
        '''
        return self.ctx2()._appendleft(thing).unswap()

    def outextend(self, things):
        '''
        extend right side of outgoing things with `things`

        @param thing: some things
        '''
        return self.ctx1('outgoing')._extend(things).unswap()

    def extend(self, things):
        '''
        extend right side of incoming things with `things`

        @param thing: some things
        '''
        return self.ctx1()._extend(things).unswap()

    def extendleft(self, things):
        '''
        extend left side of incoming things with `things`

        @param thing: some things
        '''
        return self.ctx1()._extendleft(things).unswap()


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
        return self._append(next(self._iterable))

    def last(self):
        '''last incoming thing'''
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
