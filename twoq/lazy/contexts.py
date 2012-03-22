# -*- coding: utf-8 -*-
'''twoq lazy contexts'''

from itertools import tee

__all__ = (
    'AutoContext', 'FourArmedContext', 'TwoArmedContext', 'ThreeArmedContext',
)


class Context(object):

    @property
    def iterable(self):
        '''iterable object'''
        return getattr(self._queue, self._workq)

    def __call__(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        setattr(self._queue, self._utilq, args)

    def iter(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        setattr(self._queue, self._utilq, iter(args))

    def append(self, args):
        '''append `args` to work queue'''
        setattr(self._queue, self._utilq, iter([args]))


class TwoArmedContext(Context):

    '''two armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue
        '''
        super(TwoArmedContext, self).__init__()
        self._queue = queue
        # work/utility queue attribute name
        self._workq = self._utilq = kw.get('workq', 'incoming')

    def __enter__(self):
        return self


class ThreeArmedContext(Context):

    '''three armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue
        '''
        super(ThreeArmedContext, self).__init__()
        self._queue = queue
        # work/utility queue attribute name
        self._workq = self._utilq = kw.get('workq', '_work')
        # outgoing queue attribute name
        self._outq = kw.get('outq', 'incoming')

    def __enter__(self):
        # clear work queue
        setattr(self._queue, self._workq, None)
        # clear utility queue
        setattr(self._queue, self._utilq, None)
        # extend scratch queue with incoming queue
        workq, inq = tee(getattr(self._queue, self._inq))
        setattr(self._queue, self._workq, workq)
        setattr(self._queue, self._inq, inq)
        return self

    def __exit__(self, t, v, e):
        # set outgoing queue
        setattr(self._queue, self._outq, getattr(self._queue, self._utilq))
        # clear work queue
        setattr(self._queue, self._workq, None)
        # clear utility queue
        setattr(self._queue, self._utilq, None)


class FourArmedContext(Context):

    '''four armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collections
        '''
        super(FourArmedContext, self).__init__()
        self._queue = queue
        # incoming queue attribute name
        self._inq = kw.get('inq', 'incoming')
        # outgoing queue attribute name
        self._outq = kw.get('outq', 'outgoing')
        # utility queue attribute name
        self._utilq = kw.get('utilq', '_util')
        # work queue attribute name
        self._workq = kw.get('workq', '_work')

    def __enter__(self):
        # clear outgoing queue
        setattr(self._queue, self._outq, None)
        # clear utility queue
        setattr(self._queue, self._utilq, None)
        # extend work queue with incoming queue
        tmpq, inq = tee(getattr(self._queue, self._inq))
        setattr(self._queue, self._workq, tmpq)
        setattr(self._queue, self._inq, inq)
        return self

    def __exit__(self, t, v, e):
        # set outgoing queue
        setattr(self._queue, self._outq, getattr(self._queue, self._utilq))
        # clear work queue
        setattr(self._queue, self._workq, None)
        # clear utility queue
        setattr(self._queue, self._utilq, None)


class AutoContext(FourArmedContext):

    '''auto-synchronized context manager'''

    def __exit__(self, t, v, e):
        # extend incoming queue with outgoing queue
        outq, inq = tee(getattr(self._queue, self._utilq))
        setattr(self._queue, self._outq, outq)
        setattr(self._queue, self._inq, inq)
        # clear work queue
        setattr(self._queue, self._workq, None)
        # clear utility queue
        setattr(self._queue, self._utilq, None)
