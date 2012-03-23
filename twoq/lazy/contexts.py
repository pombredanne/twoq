# -*- coding: utf-8 -*-
'''twoq lazy contexts'''

from itertools import tee, chain

from twoq.mixins.utils import ContextMixin

__all__ = (
    'AutoContext', 'FourArmContext', 'OneArmContext', 'TwoArmContext',
    'ThreeArmContext',
)


class Context(ContextMixin):

    '''context manager baseline'''

    def __call__(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        self._chain(args)

    def _chain(self, thing):
        '''chain thing'''
        queue_, utilq_ = self._queue, self._utilq
        setattr(queue_, utilq_, chain(thing, self._uget(queue_)))

    def append(self, args):
        '''append `args` to work queue'''
        self._chain(iter([args]))

    def appendleft(self, args):
        '''append `args` to left side of work queue'''
        self._chain(iter([args]))

    def clear(self):
        '''clear queue'''
        setattr(self._queue, self._utilq, iter([]))

    def extendleft(self, args):
        '''extend left side of work queue with `args`'''
        self._chain(reversed(args))

    @staticmethod
    def iterator(queue, attr='_workq'):
        '''iterator'''
        return getattr(queue, attr)

    def iter(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        self._chain(iter(args))


class OneArmContext(Context):

    '''one armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collection
        '''
        super(OneArmContext, self).__init__(queue)
        # work/utility queue
        self._workq = self._utilq = kw.get('workq', 'incoming')


class TwoArmContext(OneArmContext):

    '''two armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collections
        '''
        super(TwoArmContext, self).__init__(queue)
        # work/utility queue
        self._workq = self._utilq = kw.get('workq', '_work')
        # outgoing queue
        self._outq = kw.get('outq', 'incoming')

    def __enter__(self):
        setattr_, iter_ = setattr,  iter
        queue_, workq_, outq_ = self._queue, self._workq, self._outq
        # clear work queue
        setattr_(queue_, workq_, iter_([]))
        # clear utility queue
        setattr_(queue_, self._utilq, iter_([]))
        # extend scratch queue with incoming queue
        workq, outq = tee(self._oget(queue_))
        setattr_(queue_, workq_, workq)
        setattr_(queue_, outq_, outq)
        return self

    def __exit__(self, t, v, e):
        setattr_, iter_ = setattr,  iter
        queue_, utilq_ = self._queue, self._utilq
        # set outgoing queue
        setattr_(queue_, self._outq, self._uget(queue_))
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
        # incoming queue
        self._inq = kw.get('inq', 'incoming')
        # outgoing queue
        self._outq = kw.get('outq', 'outgoing')
        # work/utility queue
        self._workq = self._utilq = kw.get('workq', '_work')

    def __enter__(self):
        setattr_, iter_ = setattr, iter
        queue_, workq_, inq_ = self._queue, self._workq, self._inq
        # clear utility queue
        setattr_(queue_, self._utilq, iter_([]))
        # extend work queue with incoming queue
        tmpq, inq = tee(self._iget(queue_))
        setattr_(queue_, workq_, tmpq)
        setattr_(queue_, inq_, inq)
        return self

    def __exit__(self, t, v, e):
        setattr_, iter_ = setattr,  iter
        queue_, utilq_, outq_ = self._queue, self._utilq, self._outq
        # set outgoing queue
        setattr_(queue_, outq_, self._uget(queue_))
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
        # utility queue
        self._utilq = kw.get('utilq', '_util')


class AutoContext(FourArmContext):

    '''auto-synchronizing four armed context manager'''

    def __exit__(self, t, v, e):
        setattr_, iter_ = setattr,  iter
        queue_, utilq_ = self._queue, self._utilq
        # extend incoming queue with outgoing queue
        outq, inq = tee(self._uget(queue_))
        setattr_(queue_, self._outq, outq)
        setattr_(queue_, self._inq, inq)
        # clear work queue
        setattr_(queue_, self._workq, iter_([]))
        # clear utility queue
        setattr(queue_, utilq_, iter_([]))
