# -*- coding: utf-8 -*-
'''twoq contexts'''

__all__ = ('SyncContext', 'ShiftContext', 'ManContext')


class Context(object):

    '''manual sync context manager'''

    def __init__(self, queue):
        '''
        init

        @param queue: queue
        '''
        super(Context, self).__init__()
        self._outextend = queue._outextend
        self._outappend = queue._outappend
        self._outclear = queue._outclear
        self._incoming = queue.incoming

    def __exit__(self, t, v, e):
        pass


class ManContext(Context):

    '''manual sync context manager'''

    def __init__(self, queue):
        '''
        init

        @param queue: queue
        '''
        super(ManContext, self).__init__(queue)
        self._sextend = queue._sextend
        self._sappend = queue._sappend
        self._sclear = queue._sclear
        self._scratch = queue._scratch

    def __enter__(self):
        self._sclear()
        self._outclear()
        self._sextend(self._incoming)
        return self

    def __exit__(self, t, v, e):
        self._sclear()

    @property
    def iterable(self):
        return self._scratch

    def __call__(self, args):
        self._outextend(args)

    def iter(self, args):
        self._outextend(iter(args))

    def append(self, args):
        self._outappend(args)


class ShiftContext(ManContext):

    '''shift context manager'''

    def __init__(self, queue):
        '''
        init

        @param queue: queue
        '''
        super(ShiftContext, self).__init__(queue)
        self._inextend = queue._inextend
        self._outgoing = queue.outgoing

    def __exit__(self, t, v, e):
        # extend incoming items with outgoing items
        self._inextend(self._outgoing)

    @property
    def iterable(self):
        return self._incoming

    def __call__(self, args):
        self._outextend(args)

    def iter(self, args):
        self._outextend(iter(args))

    def append(self, args):
        self._outappend(args)


class SyncContext(ShiftContext):

    '''sync context manager'''

    def __init__(self, queue):
        '''
        init

        @param queue: queue
        '''
        super(SyncContext, self).__init__(queue)
        self._inclear = queue._inclear

    def __exit__(self, t, v, e):
        # clear incoming items
        self._inclear()
        # extend incoming items with outgoing items
        self._inextend(self._outgoing)

    @property
    def iterable(self):
        return self._incoming

    def __call__(self, args):
        self._outextend(args)

    def iter(self, args):
        self._outextend(iter(args))

    def append(self, args):
        self._outappend(args)
