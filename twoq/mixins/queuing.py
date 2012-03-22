# -*- coding: utf-8 -*-
'''twoq queuing mixins'''

from threading import local
from itertools import islice
from collections import deque

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

    ###########################################################################
    ## queue rotation #########################################################
    ###########################################################################

    def two(self):
        '''switch to two-armed context manager'''
        self._context = self._2arm
        return self

    def three(self):
        '''switch to three-armed context manager'''
        self._context = self._3arm
        return self

    def four(self):
        '''switch to four-armed context manager'''
        self._context = self._4arm
        return self

    def auto(self):
        '''switch to auto-synchrinizing context manager'''
        self._context = self._auto
        return self

    def swap(self, **kw):
        '''swap queues'''
        # incoming queue (default: 'incoming')
        self._inq = kw.get('inq', 'incoming')
        # outcoming queue (default: 'outcoming')
        self._outq = kw.get('outq', 'outgoing')
        # work queue (default: '_work')
        self._workq = kw.get('workq', '_work')
        # utility queue (default: '_util')
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
