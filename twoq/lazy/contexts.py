# -*- coding: utf-8 -*-
'''twoq lazy contexts'''

from itertools import tee, chain

__all__ = (
    'AutoContext', 'FourArmContext', 'OneArmContext', 'TwoArmContext',
    'ThreeArmContext',
)


class Context(object):

    '''base context manager'''

    def _chain(self, thing):
        queue_, utilq_ = self._queue, self._utilq
        setattr(queue_, utilq_, chain(thing, getattr(queue_, utilq_)))

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


class OneArmContext(Context):

    '''one armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue
        '''
        super(OneArmContext, self).__init__()
        self._queue = queue
        # work/utility queue attribute name
        self._workq = self._utilq = kw.get('workq', 'incoming')

    def __enter__(self):
        return self

    def __exit__(self, e, v, b):
        self


class TwoArmContext(OneArmContext):

    '''two armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue
        '''
        super(TwoArmContext, self).__init__(queue)
        # work/utility queue attribute name
        self._workq = self._utilq = kw.get('workq', '_work')
        # outgoing queue attribute name
        self._outq = kw.get('outq', 'incoming')

    def __enter__(self):
        setattr_, iter_ = setattr,  iter
        queue_, workq_, outq_ = self._queue, self._workq, self._outq
        # clear work queue
        setattr_(queue_, workq_, iter_([]))
        # clear utility queue
        setattr_(queue_, self._utilq, iter_([]))
        # extend scratch queue with incoming queue
        workq, outq = tee(getattr(queue_, outq_))
        setattr_(queue_, workq_, workq)
        setattr_(queue_, outq_, outq)
        return self

    def __exit__(self, t, v, e):
        setattr_, iter_ = setattr,  iter
        queue_, utilq_ = self._queue, self._utilq
        # set outgoing queue
        setattr_(queue_, self._outq, getattr(queue_, utilq_))
        # clear work queue
        setattr_(queue_, self._workq, iter_([]))
        # clear utility queue
        setattr_(queue_, utilq_, iter_([]))


class ThreeArmContext(TwoArmContext):

    '''three armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collections
        '''
        super(ThreeArmContext, self).__init__(queue)
        # incoming queue attribute name
        self._inq = kw.get('inq', 'incoming')
        # outgoing queue attribute name
        self._outq = kw.get('outq', 'outgoing')
        # work/utility queue attribute name
        self._workq = self._utilq = kw.get('workq', '_work')

    def __enter__(self):
        setattr_, iter_ = setattr,  iter
        queue_, workq_, inq_ = self._queue, self._workq, self._inq
        # clear utility queue
        setattr_(queue_, self._utilq, iter_([]))
        # extend work queue with incoming queue
        tmpq, inq = tee(getattr(queue_, inq_))
        setattr_(queue_, workq_, tmpq)
        setattr_(queue_, inq_, inq)
        return self

    def __exit__(self, t, v, e):
        setattr_, iter_ = setattr,  iter
        queue_, utilq_, outq_ = self._queue, self._utilq, self._outq
        # set outgoing queue
        setattr_(queue_, outq_, getattr(queue_, utilq_))
        # clear work queue
        setattr_(queue_, self._workq, iter_([]))
        # clear utility queue
        setattr_(queue_, utilq_, iter_([]))


class FourArmContext(ThreeArmContext):

    '''four armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collections
        '''
        super(FourArmContext, self).__init__(queue, **kw)
        self._utilq = kw.get('utilq', '_util')


class AutoContext(FourArmContext):

    '''auto-synchronized context manager'''

    def __exit__(self, t, v, e):
        setattr_, iter_ = setattr,  iter
        queue_, utilq_ = self._queue, self._utilq
        # extend incoming queue with outgoing queue
        outq, inq = tee(getattr(queue_, utilq_))
        setattr_(queue_, self._outq, outq)
        setattr_(queue_, self._inq, inq)
        # clear work queue
        setattr_(queue_, self._workq, iter_([]))
        # clear utility queue
        setattr(queue_, utilq_, iter_([]))
