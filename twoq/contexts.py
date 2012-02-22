# -*- coding: utf-8 -*-
'''twoq contexts'''

__all__ = ('ShiftContext', 'ManContext')


class ManContext(object):

    '''manual sync context manager'''

    def __init__(self, queue):
        '''
        init

        @param queue: queue
        '''
        super(ManContext, self).__init__()
        self._outextend = queue._outextend
        self._outappend = queue._outappend

    def __enter__(self):
        return self

    def __exit__(self, t, v, e):
        pass

    def __call__(self, args):
        self._outextend(args)

    def iter(self, args):
        self._outextend(iter(args))

    def append(self, args):
        self._outappend(args)


class SyncContext(ManContext):

    '''sync context manager'''

    def __init__(self, queue):
        '''
        init

        @param queue: queue
        '''
        super(SyncContext, self).__init__(queue)
        self._inextend = queue._inextend
        self._inclear = queue._inclear
        self._outclear = queue._outclear
        self._outgoing = queue.outgoing

    def __enter__(self):
        self._outclear()
        return self

    def __exit__(self, t, v, e):
        # extend incoming items with outgoing items
        self._inextend(self._outgoing)


class ShiftContext(SyncContext):

    '''shift context manager'''

    def __exit__(self, t, v, e):
        # clear incoming items
        self._inclear()
        # extend incoming items with outgoing items
        self._inextend(self._outgoing)
