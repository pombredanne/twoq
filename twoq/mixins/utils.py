# -*- coding: utf-8 -*-
'''twoq utilities'''

from operator import attrgetter

from stuf.utils import lazy


class ContextMixin(object):

    '''context manager baseline'''

    @lazy
    def _iget(self):
        '''get inq'''
        return attrgetter(self._inq)

    @lazy
    def _oget(self):
        '''get outq'''
        return attrgetter(self._outq)

    @lazy
    def _wget(self):
        '''get workq'''
        return attrgetter(self._workq)

    @lazy
    def _uget(self):
        '''get utilq'''
        return attrgetter(self._utilq)

    def __init__(self, queue, **kw):
        '''
        init

        @param queue: queue collection
        '''
        super(ContextMixin, self).__init__()
        self._queue = queue
        self._clearout = kw.get('clearout', True)

    @property
    def iterable(self):
        '''iterable'''
        return self.iterator(self._queue, self._workq)

    def __enter__(self):
        return self

    def __exit__(self, t, v, e):
        pass
