# -*- coding: utf-8 -*-
'''twoq active contexts'''

__all__ = ('SyncContext', 'ManContext')


class Context(object):

    '''base context manager'''

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

    def __call__(self, args):
        self._outextend(args)

    def iter(self, args):
        self._outextend(iter(args))

    def append(self, args):
        self._outappend(args)


class ScratchContext(Context):

    '''manual sync context manager'''

    def __init__(self, queue):
        '''
        init

        @param queue: queue
        '''
        super(ScratchContext, self).__init__(queue)
        self._sxtend = queue._sxtend
        self._sappend = queue._sappend
        self._sclear = queue._sclear
        self._scratch = queue._scratch

    def __enter__(self):
        # clear scratch queue
        self._sclear()
        # clear outgoing queue
        self._outclear()
        # extend scratch queue with incoming things
        self._sxtend(self._incoming)
        return self

    def __exit__(self, t, v, e):
        # clear scratch queue
        self._sclear()

    @property
    def iterable(self):
        return self._scratch


class AutoContext(ScratchContext):

    '''auto sync context manager'''

    def __init__(self, queue):
        '''
        init

        @param queue: queue
        '''
        super(AutoContext, self).__init__(queue)
        self._inclear = queue._inclear
        self._inextend = queue._inextend
        self._outgoing = queue.outgoing

    def __exit__(self, t, v, e):
        # clear scratch queue
        self._sclear()
        # clear incoming items
        self._inclear()
        # extend incoming items with outgoing items
        self._inextend(self._outgoing)


class ManContext(ScratchContext):

    '''manual sync context manager'''

    def __exit__(self, t, v, e):
        # clear scratch queue
        self._sclear()


class SyncContext(Context):

    '''sync context manager'''

    def __init__(self, queue):
        '''
        init

        @param queue: queue
        '''
        super(SyncContext, self).__init__(queue)
        self._inclear = queue._inclear
        self._inextend = queue._inextend
        self._outgoing = queue.outgoing

    def __enter__(self):
        # clear outgoing queue
        self._outclear()
        return self

    def __exit__(self, t, v, e):
        # clear incoming items
        self._inclear()
        # extend incoming items with outgoing items
        self._inextend(self._outgoing)

    @property
    def iterable(self):
        return self._incoming
