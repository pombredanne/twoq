# -*- coding: utf-8 -*-
'''active twoq mixins'''

from twoq.mixins.queuing import QueueingMixin, ResultMixin


__all__ = ('AutoQMixin', 'ManQMixin')


class BaseQMixin(QueueingMixin):

    '''base active queue'''

    def __init__(self, *args):
        deque_ = self._deek
        incoming = deque_(args[0]) if len(args) == 1 else deque_(args)
        self._iterator = self._iter1
        # work queue
        self._work = deque_()
        # utility queue
        self._util = deque_()
        super(BaseQMixin, self).__init__(incoming, deque_())

    def _iter1(self, attr='_UTILQ'):
        return self.iterexcept(self.__dict__[attr].popleft, IndexError)

    def _iter2(self, attr='_UTILQ'):
        return self.breakcount(self.__dict__[attr].popleft, self.__len__())

    def __len__(self):
        return self._len(self.incoming)

    def _xtend(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        self.__dict__[self._UTILQ].extend(args)
        return self._post()

    def _append(self, args):
        '''append `args` to work queue'''
        self.__dict__[self._UTILQ].append(args)
        return self._post()

    def _appendleft(self, args):
        '''append `args` to left side of work queue'''
        self.__dict__[self._UTILQ].appendleft(args)
        return self._post()

    def _iter(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        self.__dict__[self._UTILQ].extend(iter(args))
        return self._post()

    def _clear(self):
        '''clear queue'''
        self.__dict__[self._WORKQ].clear()
        return self._post()

    def _xtendleft(self, args):
        '''extend left side of work queue with `args`'''
        self.__dict__[self._UTILQ].extendleft(args)
        return self._post()

    def _iq2wq(self):
        '''extend work queue with incoming queue'''
        self._iterator = self._iter1
        sdict_ = self.__dict__
        workq_ = sdict_[self._WORKQ]
        # clear work queue
        workq_.clear()
        workq_.extend(sdict_[self._INQ])
        return self

    def _iq2wq2(self):
        '''extend work queue with incoming queue'''
        self._iterator = self._iter2
        sdict_ = self.__dict__
        workq_ = sdict_[self._WORKQ]
        # clear work queue
        workq_.clear()
        workq_.extend(sdict_[self._INQ])
        return self

    def _uq2oq(self):
        '''extend outgoing queue with utility queue'''
        sdict_ = self.__dict__
        outq_, UTILQ_ = sdict_[self._OUTQ], sdict_[self._UTILQ]
        # clear outgoing queue if set that way
        if self._clearout:
            outq_.clear()
        outq_.extend(UTILQ_)
        # clear utility queue
        UTILQ_.clear()
        return self

    def _uq2iqoq(self):
        '''extend outgoing queue and incoming queue with utility queue'''
        sdict_ = self.__dict__
        inq_ = sdict_[self._INQ]
        outq_ = sdict_[self._OUTQ]
        UTILQ_ = sdict_[self._UTILQ]
        # clear outgoing queue
        if self._clearout:
            outq_.clear()
        outq_.extend(UTILQ_)
        # clear incoming queue
        inq_.clear()
        inq_.extend(UTILQ_)
        # clear utility queue
        UTILQ_.clear()
        return self

    def _oq2wq(self):
        '''extend work queue with outgoing queue'''
        self._iterator = self._iter2
        sdict_ = self.__dict__
        workq_ = sdict_[self._WORKQ]
        # clear work queue
        workq_.clear()
        workq_.extend(sdict_[self._OUTQ])
        return self

    def outcount(self):
        '''count of outgoing things'''
        return self._len(self.outgoing)

    def ro(self):
        '''switch to read-only mode'''
        return self.ctx3(outq=self._UTILVAR)._pre()._xtend(
            self._iterable
        ).ctx1(workq=self._UTILVAR)

    def ctx3(self, hard=False, **kw):
        '''switch to three-armed context manager'''
        return self.swap(
            hard=hard,
            utilq=kw.get(self._WORKCFG, self._WORKVAR),
            pre=self._iq2wq2,
            post=self._uq2oq,
            **kw
        )


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
