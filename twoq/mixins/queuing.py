# -*- coding: utf-8 -*-
'''twoq queuing mixins'''

from threading import local
from collections import deque
from itertools import islice, tee

__all__ = ['QueueingMixin']


class ManagementMixin(local):

    '''queue management mixin'''

    def __init__(self, incoming, outgoing):
        '''
        init

        @param incoming: incoming things
        @param outgoing: outgoing things
        '''
        super(ManagementMixin, self).__init__()
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

    ###########################################################################
    ## clear queues ###########################################################
    ###########################################################################

    def inclear(self):
        '''clear incoming things'''
        with self.ctx1()._sync as sync:
            sync.clear()
        return self.unswap()

    def outclear(self):
        '''clear outgoing things'''
        with self.ctx1('outgoing')._sync as sync:
            sync.clear()
        return self.unswap()

    def _wclear(self):
        '''clear work queue'''
        with self.ctx1('_work')._sync as sync:
            sync.clear()
        return self.unswap()

    def _uclear(self):
        '''clear utility queue'''
        with self.ctx1('_util')._sync as sync:
            sync.clear()
        return self.unswap()

    def clear(self):
        '''clear every thing'''
        self.detap()
        self.outclear()
        self.inclear()
        return self

    ###########################################################################
    ## queue rotation #########################################################
    ###########################################################################

    def ctx1(self, workq='incoming'):
        '''switch to ctx1-armed context manager'''
        self._workq = workq
        self._context = self._1arm
        return self

    def ctx2(self, workq='_work', outq='incoming'):
        '''switch to two-armed context manager'''
        self._workq = workq
        self._outq = outq
        self._context = self._2arm
        return self

    def ctx3(self, workq='_work', outq='outgoing', inq='incoming'):
        '''switch to three-armed context manager'''
        self._workq = workq
        self._outq = outq
        self._inq = inq
        self._context = self._3arm
        return self

    def ctx4(self, **kw):
        '''switch to four-armed context manager'''
        self._context = self._4arm
        self.swap(
            inq=kw.get('inq', 'incoming'),
            outq=kw.get('outq', 'outgoing'),
            workq=kw.get('workq', '_work'),
            utilq=kw.get('utilq', '_util'),
        )
        return self

    def autoctx(self, **kw):
        '''switch to auto-synchronizing context manager'''
        self._context = self._auto
        self.swap(
            inq=kw.get('inq', 'incoming'),
            outq=kw.get('outq', 'outgoing'),
            workq=kw.get('workq', '_work'),
            utilq=kw.get('utilq', '_util'),
        )
        return self

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
        self._context = self._default_context
        return self.swap()

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

    def reup(self):
        '''put incoming things in incoming things as one incoming thing'''
        with self.ctx1()._sync as sync:
            sync.append(list(sync.iterable))
        return self.unswap()

    def shift(self):
        '''shift outgoing things to incoming things'''
        with self.autoctx(inq='outgoing', outq='incoming')._sync as sync:
            sync(sync.iterable)
        return self.unswap()

    sync = shift

    def outshift(self):
        '''shift incoming things to outgoing things'''
        with self.autoctx()._sync as sync:
            sync(sync.iterable)
        return self.unswap()

    outsync = outshift


class CallableMixin(local):

    '''current callable management'''

    def args(self, *args, **kw):
        '''arguments for current callable'''
        # set positional arguments
        self._args = args
        # set keyword arguemnts
        self._kw.update(kw)
        return self

    def tap(self, call):
        '''
        set current callable

        @param call: a call
        '''
        self.detap()
        # set current callable
        self._call = call
        return self

    def detap(self):
        '''clear current callable'''
        # reset postitional arguments
        self._args = ()
        # reset keyword arguments
        self._kw.clear()
        # reset callable
        self._call = None
        return self

    def wrap(self, call):
        '''build current callable from factory'''
        def factory(*args, **kw):
            return call(*args, **kw)
        return self.tap(factory)

    # alias
    unwrap = detap


class FingerMixin(local):

    '''finger the queues'''

    def append(self, thing):
        '''
        append thing to right side of incoming things

        @param thing: some thing
        '''
        with self.ctx1()._sync as sync:
            sync.append(thing)
        return self.unswap()

    def appendleft(self, thing):
        '''
        append `thing` to left side of incoming things

        @param thing: some thing
        '''
        with self.ctx1()._sync as sync:
            sync.appendleft(thing)
        return self.unswap()

    def outextend(self, things):
        '''
        extend right side of outgoing things with `things`

        @param thing: some things
        '''
        with self.ctx1('outgoing')._sync as sync:
            sync(things)
        return self.unswap()

    def extend(self, things):
        '''
        extend right side of incoming things with `things`

        @param thing: some things
        '''
        with self.ctx1()._sync as sync:
            sync(things)
        return self.unswap()

    def extendleft(self, things):
        '''
        extend left side of incoming things with `things`

        @param thing: some things
        '''
        with self.ctx1()._sync as sync:
            sync.extendleft(things)
        return self.unswap()


class QueueingMixin(ManagementMixin, CallableMixin, FingerMixin):

    '''queuing mixin'''


class ResultMixin(local):

    '''result queue mixin'''

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

    def end(self):
        '''return outgoing things and clear everything'''
        results, measure = tee(self.outgoing)
        results = next(results) if len(list(measure)) == 1 else list(results)
        self.clear()
        return results

    def value(self):
        '''return outgoing things and clear outgoing things'''
        results, measure = tee(self.outgoing)
        results = next(results) if len(list(measure)) == 1 else list(results)
        self.outclear()
        return results

    def first(self):
        '''first incoming thing'''
        with self._sync as sync:
            sync.append(next(sync.iterable))
        return self

    def last(self):
        '''last incoming thing'''
        with self._sync as sync:
            i1, _ = tee(sync.iterable)
            sync.append(deque(i1, maxlen=1).pop())
        return self

    def peek(self):
        '''results in read-only mode'''
        results = list(self._util)
        return results[0] if len(results) == 1 else results

    def __iter__(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        with self._sync as sync:
            return sync.iterable

    results = __iter__
