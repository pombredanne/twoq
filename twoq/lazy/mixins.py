# -*- coding: utf-8 -*-
'''lazy twoq mixins'''

from twoq.mixins.queuing import QueueingMixin, ResultMixin

__all__ = ['AutoQMixin', 'ManQMixin']


class BaseQMixin(QueueingMixin):

    '''base lazy queue'''

    def __init__(self, *args):
        iter_ = self._iterz
        incoming = iter_([args[0]]) if len(args) == 1 else iter_(args)
        self._work = iter_([])
        self._util = iter_([])
        super(BaseQMixin, self).__init__(incoming, iter_([]))

    def __len__(self):
        self.incoming, incoming = self._split(self.incoming)
        return self._len(self._list(incoming))

    def _xtend(self, thing):
        '''build chain'''
        self._pre()
        UTILQ_, sdict_ = self._UTILQ, self.__dict__
        sdict_[UTILQ_] = self._join(thing, sdict_[UTILQ_])
        self._post()
        return self

    def _xreplace(self, thing):
        '''build chain'''
        self._pre().__dict__[self._UTILQ] = thing
        self._post()
        return self

    __buildchain = _xtend

    def _append(self, args):
        '''append `args` to work queue'''
        return self.__buildchain(self._iterz([args]))

    def _appendleft(self, args):
        '''append `args` to left side of work queue'''
        return self.__buildchain(self._iterz([args]))

    def _clear(self):
        '''clear queue'''
        self._pre()
        UTILQ_, sdict_ = self._UTILQ, self.__dict__
        del sdict_[UTILQ_]
        sdict_[UTILQ_] = iter([])
        self._post()
        return self

    def _xtendleft(self, args):
        '''extend left side of work queue with `args`'''
        return self.__buildchain(self._reversed(args))

    def _iter(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        return self.__buildchain(iter(args))

    def _iterator(self, attr='_WORKQ'):
        '''iterator'''
        return self.__dict__[attr]

    def _clearwork(self):
        '''clear work queue and utility queue'''
        sdict_, iter_ = self.__dict__, self._iterz
        WORKQ_, UTILQ_ = self._WORKQ, self._UTILQ
        # clear work queue
        del sdict_[WORKQ_]
        sdict_[WORKQ_] = iter_([])
        # clear utility queue
        del sdict_[UTILQ_]
        sdict_[UTILQ_] = iter_([])

    def _iq2wq(self):
        '''extend work queue with incoming queue'''
        self._clearwork()
        sdict_, INQ_ = self.__dict__, self._INQ
        sdict_[self._WORKQ], sdict_[INQ_] = self._split(sdict_[INQ_])
        return self

    def _uq2oq(self):
        '''extend outgoing queue with utility queue'''
        sdict_ = self.__dict__
        sdict_[self._OUTQ] = sdict_[self._UTILQ]
        self._clearwork()
        return self

    def _uq2iqoq(self):
        '''extend incoming queue and outgoing queue with utility queue'''
        sd_ = self.__dict__
        sd_[self._INQ], sd_[self._OUTQ] = self._split(sd_[self._UTILQ])
        self._clearwork()
        return self

    def _oq2wq(self):
        '''extend work queue with outgoing queue'''
        self._clearwork()
        sd_ = self.__dict__
        sd_[self._WORKQ], sd_[self._OUTQ] = self._split(sd_[self._OUTQ])
        return self

    def outcount(self):
        '''count of outgoing things'''
        self.outgoing, outgoing = self._split(self.outgoing)
        return self._len(self._list(outgoing))

    def ro(self):
        '''switch to read-only mode'''
        return self.ctx3(outq=self._UTILVAR)._pre()._xreplace(
            self._iterable
        ).ctx1(workq=self._UTILVAR)

    def ctx3(self, hard=False, **kw):
        '''switch to three-armed context manager'''
        return self.swap(
            hard=hard,
            utilq=kw.get(self._WORKCFG, self._WORKVAR),
            pre=self._iq2wq,
            post=self._uq2oq,
            **kw
        )


class AutoQMixin(BaseQMixin):

    '''auto-balancing queue mixin'''

    _default_post = '_uq2iqoq'


class ManQMixin(BaseQMixin):

    '''manually balanced queue mixin'''

    _default_post = '_uq2oq'


class AutoResultMixin(ResultMixin, AutoQMixin):

    '''auto-balancing queue (with results extraction) mixin'''


class ManResultMixin(ResultMixin, ManQMixin):

    '''manually balanced queue (with results extraction) mixin'''
