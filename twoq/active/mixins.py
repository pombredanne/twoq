# -*- coding: utf-8 -*-
'''active twoq mixins'''

from collections import deque
from operator import methodcaller

from stuf.utils import breakcount, iterexcept, lazy, lazy_class

from twoq.mixins.queuing import QueueingMixin, ResultMixin


__all__ = ('AutoQMixin', 'ManQMixin')


class BaseQMixin(QueueingMixin):

    '''base active queue'''

    def __init__(self, *args):
        deque_ = deque
        incoming = deque_(args[0]) if len(args) == 1 else deque_(args)
        super(BaseQMixin, self).__init__(incoming, deque_())

    def _iter1(self, attr='_utilq'):
        return iterexcept(getattr(self, attr).popleft, IndexError)

    def _iter2(self, attr='_utilq'):
        return breakcount(getattr(self, attr).popleft, len(self))

    @lazy
    def _util(self):
        '''utility queue'''
        return deque()

    @lazy
    def _work(self):
        ''''work queue'''
        return deque()

    @lazy_class
    def _getextend(self):
        return methodcaller('extend')

    @lazy_class
    def _getappend(self):
        return methodcaller('append')

    @lazy_class
    def _getappendleft(self):
        return methodcaller('appendleft')

    @lazy_class
    def _getclear(self):
        return methodcaller('clear')

    @lazy_class
    def _getextendleft(self):
        return methodcaller('extendleft')

    def __len__(self):
        return len(self.incoming)

    def _extend(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        self._pre()
        self._getextend(getattr(self, self._utilq), args)
        self._post()
        return self

    def _append(self, args):
        '''append `args` to work queue'''
        self._pre()
        self._getappend(getattr(self, self._utilq), args)
        self._post()
        return self

    def _appendleft(self, args):
        '''append `args` to left side of work queue'''
        self._pre()
        self._getappendleft(getattr(self, self._utilq), args)
        return self

    def _iter(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        self._pre()
        return self._getextend(getattr(self, self._utilq), iter(args))

    def _clear(self):
        '''clear queue'''
        self._pre()
        self._getclear(getattr(self, self._utilq))
        self._post()
        return self

    def _extendleft(self, args):
        '''extend left side of work queue with `args`'''
        self._pre()
        self._getextendleft(getattr(self, self._utilq), args)
        self._post()
        return self

    def _iq2wq(self):
        '''extend work queue with incoming queue'''
        self._iterator = self._iter1
        workq_ = getattr(self, self._workq)
        # clear work queue
        workq_.clear()
        workq_.extend(self.__dict__[self._inq])
        return self

    def _uq2oq(self):
        '''extend outgoing queue with utility queue'''
        outq_, utilq_ = self.__dict__[self._outq], getattr(self, self._utilq)
        # clear outgoing queue if set that way
        if self._clearout:
            outq_.clear()
        outq_.extend(utilq_)
        # clear utility queue
        utilq_.clear()
        return self

    def _uq2iqoq(self):
        '''extend outgoing queue and incoming queue with utility queue'''
        sdict_ = self.__dict__
        inq_ = sdict_[self._inq]
        outq_ = sdict_[self._outq]
        utilq_ = getattr(self, self._utilq)
        # clear outgoing queue
        if self._clearout:
            outq_.clear()
        outq_.extend(utilq_)
        # clear incoming queue
        inq_.clear()
        inq_.extend(utilq_)
        # clear utility queue
        utilq_.clear()
        return self

    def _oq2wq(self):
        '''extend work queue with outgoing queue'''
        self._iterator = self._iter2
        workq_ = getattr(self, self._workq)
        # clear work queue
        workq_.clear()
        workq_.extend(self.__dict__[self._outq])
        return self

    def outcount(self):
        '''count of outgoing things'''
        return len(self.outgoing)


class AutoQMixin(BaseQMixin):

    '''auto-balancing queue mixin'''

    _default_post = '_uq2iqoq'


class ManQMixin(BaseQMixin):

    '''manually balanced queue mixin'''

    _default_post = '_uq2oq'


class AutoResultMixin(AutoQMixin, ResultMixin):

    '''auto-balancing manipulation queue (with results extractor) mixin'''


class ManResultMixin(ManQMixin, ResultMixin):

    '''manually balanced queue (with results extractor) mixin'''
