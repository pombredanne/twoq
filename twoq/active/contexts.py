# -*- coding: utf-8 -*-
'''twoq active contexts'''

from stuf.utils import breakcount

__all__ = ('AutoContext', 'ManContext')


class Context(object):

    def __enter__(self):
        return self

    def __call__(self, args):
        self._iterable.extend(args)

    def iter(self, args):
        self._iterable.extend(iter(args))

    def append(self, args):
        self._iterable.append(args)


class OneArmContext(Context):

    '''one arm context manager'''

    def __init__(self, queue, q='incoming'):
        '''
        init

        @param queue: queue
        '''
        super(OneArmContext, self).__init__()
        self._iterable = getattr(queue, q)

    @property
    def iterable(self):
        return breakcount(self._iterable.popleft, len(self._iterable))


class TwoArmContext(Context):

    '''two arm context manager'''

    def __init__(self, queue, q='incoming', tmpq='_scratch'):
        '''
        init

        @param queue: queue
        '''
        super(ManContext, self).__init__()
        self._queue = getattr(queue, q)
        self._iterable = getattr(queue, tmpq)

    def __enter__(self):
        # clear outgoing queue
        self._iterable.clear()
        return self

    def __exit__(self, t, v, e):
        # clear incoming items
        self._queue.clear()
        # extend incoming items with outgoing items
        self._queue.extend(self._iterable)
        self._iterable.clear()

    @property
    def iterable(self):
        return breakcount(self._queue.popleft, len(self._iterable))


class ManContext(object):

    '''manual synchronization context manager'''

    def __init__(self, q, inq='incoming', outq='outgoing', tmpq='_scratch'):
        '''
        init

        @param queue: queue
        '''
        super(ManContext, self).__init__()
        self._inq = getattr(q, inq)
        self._outq = getattr(q, outq)
        self._iterable = getattr(q, tmpq)

    def __enter__(self):
        # clear scratch queue
        self._iterable.clear()
        # clear outgoing queue
        self._outq.clear()
        # extend scratch queue with incoming things
        self._iterable.extend(self._inq)
        return self

    def __exit__(self, t, v, e):
        # clear scratch queue
        self._iterable.clear()

    def __call__(self, args):
        self._outq.extend(args)

    def iter(self, args):
        self._outq.extend(iter(args))

    def append(self, args):
        self._outq.append(args)

    @property
    def iterable(self):
        return self._iterable


class AutoContext(ManContext):

    '''auto-synchronization context manager'''

    def __exit__(self, t, v, e):
        # clear scratch queue
        self._iterable.clear()
        # clear incoming items
        self._inq.clear()
        # extend incoming items with outgoing items
        self._inq.extend(self._outq)
