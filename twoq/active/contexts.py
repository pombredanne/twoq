# -*- coding: utf-8 -*-
'''twoq active contexts'''

from stuf.utils import breakcount, iterexcept

__all__ = (
    'AutoContext', 'FourArmedContext', 'TwoArmedContext', 'ThreeArmedContext',
)


class Context(object):

    '''context manager baseline'''

    def __call__(self, args):
        '''extend work queue with `args`'''
        self._utilq.extend(args)

    @property
    def iterable(self):
        '''iterable object'''
        return iterexcept(self._workq.popleft, IndexError)

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


class TwoArmedContext(Context):

    '''two armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collection
        '''
        super(TwoArmedContext, self).__init__()
        # work/utility queue attribute name (default: 'incoming')
        self._workq = self._utilq = getattr(queue, kw.get('workq', 'incoming'))

    def __enter__(self):
        return self

    @property
    def iterable(self):
        '''`iterator'''
        return breakcount(self._workq.popleft, len(self._workq))


class ThreeArmedContext(Context):

    '''three armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collections
        '''
        super(ThreeArmedContext, self).__init__()
        # work/utility queue attribute name (default: '_workq')
        self._workq = self._utilq = getattr(queue, kw.get('workq', '_work'))
        # outgoing queue attribute name (default: 'incoming')
        self._outq = getattr(queue, kw.get('outq', 'incoming'))

    def __enter__(self):
        # clear work queue
        self._workq.clear()
        # extend work queue with outgoing queue
        self._workq.extend(self._outq)
        return self

    def __exit__(self, t, v, e):
        # clear outgoing queue
        self._outq.clear()
        # extend outgoing queue with utility queue
        self._outq.extend(self._utilq)
        # clear work queue
        self._workq.clear()

    @property
    def iterable(self):
        '''iterable object'''
        return iterexcept(self._workq.popleft, IndexError)


class FourArmedContext(Context):

    '''four armed context manager'''

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collections
        '''
        super(FourArmedContext, self).__init__()
        # outgoing queue attribute name (default: 'outgoing')
        self._outq = getattr(queue, kw.get('outq', 'outgoing'))
        # incoming queue attribute name (default: 'incoming')
        self._inq = getattr(queue, kw.get('inq', 'incoming'))
        # work queue attribute name (default: '_workq')
        self._workq = getattr(queue, kw.get('workq', '_work'))
        # utility queue attribute name (default: '_utilq')
        self._utilq = getattr(queue, kw.get('utilq', '_util'))

    def __enter__(self):
        # clear work queue
        self._workq.clear()
        # extend work queue with incoming queue
        self._workq.extend(self._inq)
        return self

    def __exit__(self, t, v, e):
        # clear outgoing queue
        self._outq.clear()
        # extend outgoing queue with utility queue
        self._outq.extend(self._utilq)
        # clear utility queue
        self._utilq.clear()


class AutoContext(FourArmedContext):

    '''auto-synchronizing four armed context manager'''

    def __exit__(self, t, v, e):
        # clear incoming queue
        self._inq.clear()
        # clear outgoing queue
        self._outq.clear()
        # extend outgoing queue with outgoing queue
        self._outq.extend(self._utilq)
        # extend incoming queue with outgoing queue
        self._inq.extend(self._utilq)
        # clear utility queue
        self._utilq.clear()
