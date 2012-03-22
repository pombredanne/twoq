# -*- coding: utf-8 -*-
'''twoq lazy contexts'''

from itertools import tee, chain

__all__ = (
    'AutoContext', 'FourArmedContext', 'OneArmedContext', 'TwoArmedContext',
    'ThreeArmedContext',
)


class Context(object):

    def _chain(self, thing):
        setattr(
            self._queue,
            self._utilq,
            chain(thing, getattr(self._queue, self._utilq)),
        )

    @property
    def iterable(self):
        '''iterable object'''
        return getattr(self._queue, self._workq)

    def __call__(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        self._chain(args)

    def iter(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        self._chain(iter(args))

    def append(self, args):
        '''append `args` to work queue'''
        self._chain(iter([args]))

    def appendleft(self, thing):
        '''
        append `thing` to left side of incoming things

        @param thing: some thing
        '''
        self._chain(iter([thing]))

    def extendleft(self, things):
        '''
        extend left side of incoming things with `things`

        @param thing: some things
        '''
        self._chain(reversed(things))

    def clear(self):
        '''clear queue'''
        setattr(self._queue, self._utilq, iter([]))


class OneArmedContext(Context):

    '''one armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue
        '''
        super(OneArmedContext, self).__init__()
        self._queue = queue
        # work/utility queue attribute name
        self._workq = self._utilq = kw.get('workq', 'incoming')

    def __enter__(self):
        return self

    def __exit__(self, e, v, b):
        self


class TwoArmedContext(OneArmedContext):

    '''two armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue
        '''
        super(TwoArmedContext, self).__init__(queue)
        # work/utility queue attribute name
        self._workq = self._utilq = kw.get('workq', '_work')
        # outgoing queue attribute name
        self._outq = kw.get('outq', 'incoming')

    def __enter__(self):
        # clear work queue
        setattr(self._queue, self._workq, iter([]))
        # clear utility queue
        setattr(self._queue, self._utilq, iter([]))
        # extend scratch queue with incoming queue
        workq, outq = tee(getattr(self._queue, self._outq))
        setattr(self._queue, self._workq, workq)
        setattr(self._queue, self._outq, outq)
        return self

    def __exit__(self, t, v, e):
        # set outgoing queue
        setattr(self._queue, self._outq, getattr(self._queue, self._utilq))
        # clear work queue
        setattr(self._queue, self._workq, iter([]))
        # clear utility queue
        setattr(self._queue, self._utilq, iter([]))


class ThreeArmedContext(TwoArmedContext):

    '''three armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collections
        '''
        super(ThreeArmedContext, self).__init__(queue)
        # incoming queue attribute name
        self._inq = kw.get('inq', 'incoming')
        # outgoing queue attribute name
        self._outq = kw.get('outq', 'outgoing')
        # work/utility queue attribute name
        self._workq = self._utilq = kw.get('workq', '_work')

    def __enter__(self):
        # clear outgoing queue
        setattr(self._queue, self._outq, iter([]))
        # clear utility queue
        setattr(self._queue, self._utilq, iter([]))
        # extend work queue with incoming queue
        tmpq, inq = tee(getattr(self._queue, self._inq))
        setattr(self._queue, self._workq, tmpq)
        setattr(self._queue, self._inq, inq)
        return self

    def __exit__(self, t, v, e):
        # set outgoing queue
        setattr(self._queue, self._outq, getattr(self._queue, self._utilq))
        # clear work queue
        setattr(self._queue, self._workq, iter([]))
        # clear utility queue
        setattr(self._queue, self._utilq, iter([]))


class FourArmedContext(ThreeArmedContext):

    '''four armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collections
        '''
        super(FourArmedContext, self).__init__(queue, **kw)
        self._utilq = kw.get('utilq', '_util')


class AutoContext(FourArmedContext):

    '''auto-synchronized context manager'''

    def __exit__(self, t, v, e):
        # extend incoming queue with outgoing queue
        outq, inq = tee(getattr(self._queue, self._utilq))
        setattr(self._queue, self._outq, outq)
        setattr(self._queue, self._inq, inq)
        # clear work queue
        setattr(self._queue, self._workq, iter([]))
        # clear utility queue
        setattr(self._queue, self._utilq, iter([]))
