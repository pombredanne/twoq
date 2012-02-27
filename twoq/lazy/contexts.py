# -*- coding: utf-8 -*-
'''twoq lazy contexts'''

from itertools import tee

__all__ = ('AutoContext', 'ManContext')


class Context(object):

    '''base context manager'''

    def __init__(self, queue):
        '''
        init

        @param queue: queue
        '''
        super(Context, self).__init__()
        self._queue = queue

    def __call__(self, args):
        self._queue.outgoing = args

    def iter(self, args):
        self._queue.outgoing = iter(args)

    def append(self, args):
        self._queue.outgoing = iter([args])


class ManContext(Context):

    '''manual sync context manager'''

    def __enter__(self):
        # clear outgoing _queue
        self._queue.outgoing = None
        # extend scratch _queue with incoming things
        self._queue._scratch, self._queue.incoming = tee(self._queue.incoming)
        return self

    def __exit__(self, t, v, e):
        # clear scratch _queue
        self._queue._scratch = None

    @property
    def iterable(self):
        return self._queue._scratch


class AutoContext(ManContext):

    '''auto sync context manager'''

    def __exit__(self, t, v, e):
        # clear scratch _queue
        self._queue._scratch = None
        # extend incoming items with outgoing items
        self._queue.incoming, self._queue.outgoing = tee(self._queue.outgoing)
