# -*- coding: utf-8 -*-
'''twoq queuing mixins'''

from threading import local
from itertools import islice
from collections import deque

__all__ = ['QueueingMixin']


class QueueingMixin(local):

    '''queuing mixin'''

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

    def __iter__(self):
        '''outgoing things iterator'''
        return iter(self.outgoing)

    ###########################################################################
    ## queue management #######################################################
    ###########################################################################

    def args(self, *args, **kw):
        '''arguments for current callable'''
        # set positional arguments
        self._args = args
        # set keyword arguemnts
        self._kw = kw
        return self

    _oargs = args

    def tap(self, call):
        '''
        add call

        @param call: a call
        '''
        # reset postitional arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # add the callable
        self._call = call
        return self

    _otap = tap

    def detap(self):
        '''clear call'''
        # reset postitional arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # reset callable
        self._call = None
        return self

    _odetap = detap

    def wrap(self, call):
        '''build factory callable and make call'''
        def factory(*args, **kw):
            return call(*args, **kw)
        self._call = factory
        return self

    _owrap = wrap

    # aliases
    unwrap = detap

    def ahead(self, n=None):
        '''
        move iterator n-steps ahead or, if n is `None`, consume entirely

        @param n: number of steps to advance (default: None)
        '''
        # Use functions that consume iterators at C speed.
        if n is None:
            # feed the entire iterator into a zero-length deque
            self.incoming = deque(self.incoming, maxlen=0)
        else:
            # advance to the empty slice starting at position n
            next(islice(self.incoming, n, n), None)
        return self

    _oahead = ahead
