# -*- coding: utf-8 -*-
'''active twoq mixins'''

from collections import deque

from stuf.utils import breakcount, iterexcept

from twoq.mixins.queuing import QueueingMixin, ResultMixin


__all__ = ('AutoQMixin', 'ManQMixin')


class BaseQMixin(QueueingMixin):

    '''base active queue'''

    def __init__(self, *args):
        deque_ = deque
        incoming = deque_(args[0]) if len(args) == 1 else deque_(args)
        self._iterator = self._iter1
        # work queue
        self._work = deque()
        # utility queue
        self._util = deque()
        super(BaseQMixin, self).__init__(incoming, deque_())

    def _iter1(self, attr='_utilq'):
        return iterexcept(self.__dict__[attr].popleft, IndexError)

    def _iter2(self, attr='_utilq'):
        return breakcount(self.__dict__[attr].popleft, len(self))

    def __len__(self):
        return len(self.incoming)

    def _extend(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        self.__dict__[self._utilq].extend(args)
        return self._post()

    def _append(self, args):
        '''append `args` to work queue'''
        self.__dict__[self._utilq].append(args)
        return self._post()

    def _appendleft(self, args):
        '''append `args` to left side of work queue'''
        self.__dict__[self._utilq].appendleft(args)
        return self._post()

    def _iter(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        self.__dict__[self._utilq].extend(iter(args))
        return self._post()

    def _clear(self):
        '''clear queue'''
        self.__dict__[self._workq].clear()
        return self._post()

    def _extendleft(self, args):
        '''extend left side of work queue with `args`'''
        self.__dict__[self._utilq].extendleft(args)
        return self._post()

    def _iq2wq(self):
        '''extend work queue with incoming queue'''
        self._iterator = self._iter1
        sdict_ = self.__dict__
        workq_ = sdict_[self._workq]
        # clear work queue
        workq_.clear()
        workq_.extend(sdict_[self._inq])
        return self

    def _uq2oq(self):
        '''extend outgoing queue with utility queue'''
        sdict_ = self.__dict__
        outq_, utilq_ = sdict_[self._outq], sdict_[self._utilq]
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
        utilq_ = sdict_[self._utilq]
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
        sdict_ = self.__dict__
        workq_ = sdict_[self._workq]
        # clear work queue
        workq_.clear()
        workq_.extend(sdict_[self._outq])
        return self

    def outcount(self):
        '''count of outgoing things'''
        return len(self.outgoing)

    def ctx3(self, **kw):
        '''switch to three-armed context manager'''
        self._clearout = kw.pop('clearout', True)
        self._workq = self._utilq = kw.pop('workq', '_work')
        self._outq = kw.pop('outq', 'outgoing')
        self._inq = kw.pop('inq', 'incoming')
        self._pre = self._oq2wq
        self._post = self._uq2oq
        return self


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
