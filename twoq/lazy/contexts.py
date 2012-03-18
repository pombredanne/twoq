# -*- coding: utf-8 -*-
'''twoq lazy contexts'''

from itertools import tee

__all__ = ('AutoContext', 'ManContext')


class ManContext(object):

    '''manual sync context manager'''

    def __init__(self, queue, inq='incoming', outq='outgoing', tmp='_scratch'):
        '''
        init

        @param queue: queue
        '''
        super(ManContext, self).__init__()
        self._queue = queue
        self._inq = inq
        self._outq = outq
        self._iterable = tmp

    def __enter__(self):
        # clear outgoing queue
        setattr(self._queue, self._outq, None)
        # extend scratch queue with incoming queue
        tmp, inq = tee(getattr(self._queue, self._inq))
        setattr(self._queue, self._iterable, tmp)
        setattr(self._queue, self._inq, inq)
        return self

    def __exit__(self, t, v, e):
        # clear scratch queue
        self._queue._scratch = None

    @property
    def iterable(self):
        return getattr(self._queue, self._iterable)

    def __call__(self, args):
        setattr(self._queue, self._outq, args)

    def iter(self, args):
        setattr(self._queue, self._outq, iter(args))

    def append(self, args):
        setattr(self._queue, self._outq, iter([args]))


class AutoContext(ManContext):

    '''auto sync context manager'''

    def __exit__(self, t, v, e):
        # clear scratch queue
        setattr(self._queue, self._iterable, None)
        # extend incoming queue with outgoing queue
        outq, inq = tee(getattr(self._queue, self._outq))
        setattr(self._queue, self._outq, outq)
        setattr(self._queue, self._inq, inq)
