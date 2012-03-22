# -*- coding: utf-8 -*-
'''twoq queuing mixins'''

from threading import local
from collections import deque
from itertools import islice, tee

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
    ## queue iteration ########################################################
    ###########################################################################

    def __iter__(self):
        '''iterate over outgoing things'''
        return iter(self.outgoing)

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
        self._context = self._4arm
        return self

    def autoctx(self):
        '''switch to autoctx-synchronizing context manager'''
        self._context = self._auto
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

    ###########################################################################
    ## current callable management ############################################
    ###########################################################################

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


class ResultMixin(local):

    def end(self):
        '''return outgoing things and clear everything'''
        results = list(self.outgoing)
        results = results.pop() if len(results) == 1 else results
        self.clear()
        return results

    def value(self):
        '''return outgoing things and clear outgoing things'''
        results = list(self.outgoing)
        results = results.pop() if len(results) == 1 else results
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
