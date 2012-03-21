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
        # labels
        self._inq = 'incoming'
        self._outq = 'outgoing'
        self._tmpq = '_scratch'

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

    def swap(self, inq='incoming', outq='outgoing', tmpq='_scratch'):
        '''
        swap queues

        @param inq: incoming queue (default: 'incoming')
        @param outq: outcoming queue (default: 'outcoming')
        @param tmpq: temporary queue (default: '_scratch')
        '''
        self._inq = inq
        self._outq = outq
        self._tmpq = tmpq
        return self

    def unswap(self):
        '''rotate queues to default'''
        return self.swap()

    @property
    def _sync(self):
        '''synchronization context'''
        return self._context(self, self._inq, self._outq, self._tmpq)

    def ro(self):
        '''enter read-only mode'''
        self._o_readclear()
        return self.swap(inq='_read', outq='_read')

    def rw(self):
        '''enter read/write mode'''
        self._o_readclear()
        return self.swap()

    ###########################################################################
    ## current callable management ############################################
    ###########################################################################

    def args(self, *args, **kw):
        '''arguments for current callable'''
        # set positional arguments
        self._args = args
        # set keyword arguemnts
        self._kw = kw
        return self

    def tap(self, call):
        '''
        set current callable

        @param call: a call
        '''
        # reset postitional arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # add the callable
        self._call = call
        return self

    def detap(self):
        '''clear current callable'''
        # reset postitional arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # reset callable
        self._call = None
        return self

    def wrap(self, call):
        '''build current callable from factory'''
        def factory(*args, **kw):
            return call(*args, **kw)
        self._call = factory
        return self

    # aliases
    unwrap = detap
