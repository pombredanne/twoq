# -*- coding: utf-8 -*-
'''twoq active contexts'''

__all__ = ('AutoContext', 'ManContext')


class ManContext(object):

    '''manual sync context manager'''

    def __init__(self, q, inq='incoming', outq='outgoing', tmpq='_scratch'):
        '''
        init

        @param queue: queue
        '''
        super(ManContext, self).__init__()
        _inq = getattr(q, inq)
        _outq = getattr(q, outq)
        self._outextend = _outq.extend
        self._outappend = _outq.append
        self._outclear = _outq.clear
        self._inq = _inq
        self._iterable = getattr(q, tmpq)
        self._sxtend = self._iterable.extend
        self._sappend = self._iterable.append
        self._sclear = self._iterable.clear

    def __enter__(self):
        # clear scratch queue
        self._sclear()
        # clear outgoing queue
        self._outclear()
        # extend scratch queue with incoming things
        self._sxtend(self._inq)
        return self

    def __exit__(self, t, v, e):
        # clear scratch queue
        self._sclear()

    def __call__(self, args):
        self._outextend(args)

    def iter(self, args):
        self._outextend(iter(args))

    def append(self, args):
        self._outappend(args)

    @property
    def iterable(self):
        return self._iterable


class AutoContext(ManContext):

    '''auto sync context manager'''

    def __init__(self, q, inq='incoming', outq='outgoing', tmpq='_scratch'):
        '''
        init

        @param queue: queue
        '''
        super(AutoContext, self).__init__(q, inq, outq, tmpq)
        self._inclear = self._inq.clear
        self._inextend = self._inq.extend
        self._outq = q.outgoing

    def __exit__(self, t, v, e):
        # clear scratch queue
        self._sclear()
        # clear incoming items
        self._inclear()
        # extend incoming items with outgoing items
        self._inextend(self._outq)
