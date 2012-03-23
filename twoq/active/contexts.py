# -*- coding: utf-8 -*-
'''twoq active contexts'''

from stuf.utils import breakcount, iterexcept

from twoq.mixins.utils import ContextMixin

__all__ = (
    'AutoContext', 'FourArmContext', 'OneArmContext', 'TwoArmContext',
    'ThreeArmContext',
)


class Context(ContextMixin):

    '''context manager baseline'''

    def __call__(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        self._uget(self._queue).extend(args)

    def append(self, args):
        '''append `args` to work queue'''
        self._uget(self._queue).append(args)

    def appendleft(self, args):
        '''append `args` to left side of work queue'''
        self._uget(self._queue).appendleft(args)

    def clear(self):
        '''clear queue'''
        self._uget(self._queue).clear()

    def extendleft(self, args):
        '''extend left side of work queue with `args`'''
        self._uget(self._queue).extendleft(args)

    @staticmethod
    def iterator(queue, attr='_workq'):
        '''iterator'''
        return breakcount(getattr(queue, attr).popleft, len(queue))

    def iter(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        self._uget(self._queue).extend(iter(args))


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


class TwoArmContext(Context):

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
        q_ = self._queue
        workq_ = self._wget(q_)
        # clear work queue
        workq_.clear()
        # extend work queue with outgoing queue
        workq_.extend(self._oget(q_))
        return self

    def __exit__(self, t, v, e):
        q_ = self._queue
        outq_ = self._oget(q_)
        # clear outgoing queue
        if self._clearout:
            outq_.clear()
        # extend outgoing queue with utility queue
        outq_.extend(self._uget(q_))
        # clear work queue
        self._wget(q_).clear()


class ThreeArmContext(Context):

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
        q_ = self._queue
        workq_ = self._wget(q_)
        # clear work queue
        workq_.clear()
        # extend work queue with incoming queue
        workq_.extend(self._iget(q_))
        return self

    def __exit__(self, t, v, e):
        q_ = self._queue
        outq_, utilq_ = self._oget(q_), self._uget(q_)
        # clear outgoing queue
        if self._clearout:
            outq_.clear()
        # extend outgoing queue with utility queue
        outq_.extend(utilq_)
        # clear utility queue
        utilq_.clear()


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

    @staticmethod
    def iterator(queue, attr='_workq'):
        '''iterable object'''
        return iterexcept(getattr(queue, attr).popleft, IndexError)


class AutoContext(FourArmContext):

    '''auto-synchronizing four armed context manager'''

    def __exit__(self, t, v, e):
        q_ = self._queue
        iq_, oq_, uq_ = self._iget(q_), self._oget(q_), self._uget(q_)
        # clear incoming queue
        iq_.clear()
        # clear outgoing queue
        if self._clearout:
            oq_.clear()
        # extend outgoing queue with outgoing queue
        oq_.extend(uq_)
        # extend incoming queue with outgoing queue
        iq_.extend(uq_)
        # clear utility queue
        uq_.clear()
