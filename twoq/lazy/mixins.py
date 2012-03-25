# -*- coding: utf-8 -*-
'''lazy twoq mixins'''

from twoq.mixins.queuing import QueueingMixin, ResultMixin

__all__ = ['AutoQMixin', 'ManQMixin']


class BaseQMixin(QueueingMixin):

    '''base lazy queue'''

    def __init__(self, *args):
        iter_ = iter
        incoming = iter_([args[0]]) if len(args) == 1 else iter_(args)
        self._work = iter_([])
        self._util = iter_([])
        super(BaseQMixin, self).__init__(incoming, iter_([]))

    def __len__(self):
        self.incoming, incoming = self._split(self.incoming)
        return len(self._list(incoming))

    def _extend(self, thing):
        '''build chain'''
        self._pre()
        utilq_, sdict_ = self._utilq, self.__dict__
        sdict_[utilq_] = self._join(thing, sdict_[utilq_])
        self._post()
        return self

    def _exreplace(self, thing):
        '''build chain'''
        self._pre().__dict__[self._utilq] = thing
        self._post()
        return self

    __buildchain = _extend

    def _append(self, args):
        '''append `args` to work queue'''
        return self.__buildchain(iter([args]))

    def _appendleft(self, args):
        '''append `args` to left side of work queue'''
        return self.__buildchain(iter([args]))

    def _clear(self):
        '''clear queue'''
        self._pre()
        utilq_, sdict_ = self._utilq, self.__dict__
        del sdict_[utilq_]
        sdict_[utilq_] = iter([])
        self._post()
        return self

    def _extendleft(self, args):
        '''extend left side of work queue with `args`'''
        return self.__buildchain(self._reversed(args))

    def _iter(self, args):
        '''extend work queue with `args` wrapped in iterator'''
        return self.__buildchain(iter(args))

    def _iterator(self, attr='_workq'):
        '''iterator'''
        return self.__dict__[attr]

    def _clearwork(self):
        '''clear work queue and utility queue'''
        sdict_, iter_ = self.__dict__, iter
        workq_, utilq_ = self._workq, self._utilq
        # clear work queue
        del sdict_[workq_]
        sdict_[workq_] = iter_([])
        # clear utility queue
        del sdict_[utilq_]
        sdict_[utilq_] = iter_([])

    def _iq2wq(self):
        '''extend work queue with incoming queue'''
        self._clearwork()
        sdict_, inq_ = self.__dict__, self._inq
        sdict_[self._workq], sdict_[inq_] = self._split(sdict_[inq_])
        return self

    def _uq2oq(self):
        '''extend outgoing queue with utility queue'''
        sdict_ = self.__dict__
        sdict_[self._outq] = sdict_[self._utilq]
        self._clearwork()
        return self

    def _uq2iqoq(self):
        '''extend incoming queue and outgoing queue with utility queue'''
        sd_ = self.__dict__
        sd_[self._inq], sd_[self._outq] = self._split(sd_[self._utilq])
        self._clearwork()
        return self

    def _oq2wq(self):
        '''extend work queue with outgoing queue'''
        self._clearwork()
        sd_ = self.__dict__
        sd_[self._workq], sd_[self._outq] = self._split(sd_[self._outq])
        return self

    def outcount(self):
        '''count of outgoing things'''
        self.outgoing, outgoing = self._split(self.outgoing)
        return len(list(outgoing))

    def ro(self):
        '''switch to read-only mode'''
        return self.ctx3(outq='_util')._pre()._exreplace(
            self._iterable
        ).ctx1(workq='_util')

    def ctx3(self, **kw):
        '''switch to three-armed context manager'''
        self._clearout = kw.pop('clearout', True)
        self._workq = self._utilq = kw.pop('workq', '_work')
        self._outq = kw.pop('outq', 'outgoing')
        self._inq = kw.pop('inq', 'incoming')
        self._pre = self._iq2wq
        self._post = self._uq2oq
        return self


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
