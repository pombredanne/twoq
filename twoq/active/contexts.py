# -*- coding: utf-8 -*-
'''twoq active contexts'''

from stuf.utils import breakcount, iterexcept


class Context(object):

    '''context manager baseline'''

    def __call__(self, args):
        '''extend work queue with `args`'''
        self._utilq.extend(args)

    @property
    def iterable(self):
        '''`iterator'''
        return breakcount(self._workq.popleft, len(self._workq))

    def iter(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        self._utilq.extend(iter(args))

    def append(self, args):
        '''append `args` to work queue'''
        self._utilq.append(args)

    def pop(self):
        '''right side `pop` from work queue'''
        return self._workq.pop()

    def popleft(self):
        '''left-side pop from work queue'''
        return self._workq.popleft()

    def appendleft(self, thing):
        '''left side append from work queue'''
        self._utilq.appendleft(thing)

    def extendleft(self, thing):
        '''left side extend from work queue'''
        self._utilq.extendleft(thing)

    def clear(self):
        '''clear queue'''
        self._utilq.clear()


class OneArmContext(Context):

    '''one armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collection
        '''
        super(OneArmContext, self).__init__()
        # work/utility queue attribute name
        self._workq = self._utilq = getattr(queue, kw.get('workq', 'incoming'))

    def __enter__(self):
        return self

    def __exit__(self, t, v, e):
        pass


class TwoArmContext(Context):

    '''two armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collections
        '''
        super(TwoArmContext, self).__init__()
        # outgoing queue attribute name
        self._outq = getattr(queue, kw.get('outq', 'incoming'))
        # work/utility queue attribute name
        self._workq = self._utilq = getattr(queue, kw.get('workq', '_workq'))

    def __enter__(self):
        workq_ = self._workq
        # clear work queue
        workq_.clear()
        # extend work queue with outgoing queue
        workq_.extend(self._outq)
        return self

    def __exit__(self, t, v, e):
        outq_ = self._outq
        # clear outgoing queue
        outq_.clear()
        # extend outgoing queue with utility queue
        outq_.extend(self._utilq)
        # clear work queue
        self._workq.clear()


class ThreeArmContext(Context):

    '''three armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collections
        '''
        super(ThreeArmContext, self).__init__()
        # incoming queue attribute name
        self._inq = getattr(queue, kw.get('inq', 'incoming'))
        # outgoing queue attribute name
        self._outq = getattr(queue, kw.get('outq', 'outgoing'))
        # work/utility queue attribute name
        self._workq = self._utilq = getattr(queue, kw.get('workq', '_workq'))

    def __enter__(self):
        workq_ = self._workq
        # clear work queue
        workq_.clear()
        # extend work queue with incoming queue
        workq_.extend(self._inq)
        return self

    def __exit__(self, t, v, e):
        outq_ = self._outq
        # clear outgoing queue
        outq_.clear()
        # extend outgoing queue with utility queue
        outq_.extend(self._utilq)
        # clear utility queue
        self._utilq.clear()

    @property
    def iterable(self):
        '''iterable object'''
        return iterexcept(self._workq.popleft, IndexError)


class FourArmContext(ThreeArmContext):

    '''four armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collections
        '''
        super(FourArmContext, self).__init__(queue, **kw)
        # utility queue attribute name (default: '_utilq')
        self._utilq = getattr(queue, kw.get('utilq', '_util'))


class AutoContext(FourArmContext):

    '''auto-synchronizing four armed context manager'''

    def __exit__(self, t, v, e):
        inq_, outq_, utilq_ = self._inq, self._outq, self._utilq
        # clear incoming queue
        inq_.clear()
        # clear outgoing queue
        outq_.clear()
        # extend outgoing queue with outgoing queue
        outq_.extend(utilq_)
        # extend incoming queue with outgoing queue
        inq_.extend(utilq_)
        # clear utility queue
        utilq_.clear()
