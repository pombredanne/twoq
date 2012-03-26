# -*- coding: utf-8 -*-
'''lazy twoq mixins'''

from twoq.mixins.queuing import QueueingMixin, ResultMixin

__all__ = ['AutoQMixin', 'ManQMixin']


class BaseQMixin(QueueingMixin):

    '''base lazy queue'''

    def __init__(self, *things):
        iter_ = self._iterz
        incoming = iter_([things[0]]) if len(things) == 1 else iter_(things)
        self._work = iter_([])
        self._util = iter_([])
        super(BaseQMixin, self).__init__(incoming, iter_([]))

    ###########################################################################
    ## length #################################################################
    ###########################################################################

    def __len__(self):
        '''number of incoming things'''
        self.incoming, incoming = self._split(self.incoming)
        return self._len(self._list(incoming))

    def outcount(self):
        '''number of outgoing things'''
        self.outgoing, outgoing = self._split(self.outgoing)
        return self._len(self._list(outgoing))

    ###########################################################################
    ## iterators ##############################################################
    ###########################################################################

    def __iter__(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        return self.__dict__[self._OUTQ]

    @property
    def _iterable(self):
        '''iterable'''
        return self.__dict__[self._WORKQ]

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearwork(self):
        '''clear work queue and utility queue'''
        sdict, iter_ = self.__dict__, self._iterz
        WORKQ, UTILQ = self._WORKQ, self._UTILQ
        # clear work queue
        del sdict[WORKQ]
        sdict[WORKQ] = iter_([])
        # clear utility queue
        del sdict[UTILQ]
        sdict[UTILQ] = iter_([])
        return self

    def _uclear(self):
        '''clear utility queue'''
        UTILQ, sdict = self._UTILQ, self.__dict__
        del sdict[UTILQ]
        sdict[UTILQ] = iter([])
        return self

    def _wclear(self):
        '''clear work queue'''
        WORKQ, sdict = self._WORKQ, self.__dict__
        del sdict[WORKQ]
        sdict[WORKQ] = iter([])
        return self

    def inclear(self):
        '''clear incoming things'''
        INQ, sdict = self._INQ, self.__dict__
        del sdict[INQ]
        sdict[INQ] = iter([])
        return self

    def outclear(self):
        '''clear outgoing things'''
        OUTQ, sdict = self._OUTQ, self.__dict__
        del sdict[OUTQ]
        sdict[OUTQ] = iter([])
        return self

    ###########################################################################
    ## extend #################################################################
    ###########################################################################

    def _xtend(self, thing):
        '''build chain'''
        UTILQ, sdict = self._UTILQ, self.__dict__
        sdict[UTILQ] = self._join(thing, sdict[UTILQ])
        return self._post()

    __buildchain = _xtend

    def _xtendleft(self, things):
        '''extend left side of work queue with `things`'''
        return self.__buildchain(self._reversed(things))

    def _xreplace(self, thing):
        '''build chain'''
        self.__dict__[self._UTILQ] = thing
        return self._post()

    def _iter(self, things):
        '''extend work queue with `things` wrapped in iterator'''
        return self.__buildchain(iter(things))

    ###########################################################################
    ## append #################################################################
    ###########################################################################

    def _append(self, things):
        '''append `things` to work queue'''
        return self.__buildchain(self._iterz([things]))

    def _appendleft(self, things):
        '''append `things` to left side of work queue'''
        return self.__buildchain(self._iterz([things]))

    ###########################################################################
    ## enter context ##########################################################
    ###########################################################################

    def _iq2wq(self):
        '''extend work queue with incoming queue'''
        sdict = self._clearwork().__dict__
        sdict[self._WORKQ], sdict[self._INQ] = self._split(sdict[self._INQ])
        return self

    def _oq2wq(self):
        '''extend work queue with outgoing queue'''
        sd = self._clearwork().__dict__
        sd[self._WORKQ], sd[self._OUTQ] = self._split(sd[self._OUTQ])
        return self

    ###########################################################################
    ## exit context ###########################################################
    ###########################################################################

    def _uq2oq(self):
        '''extend outgoing queue with utility queue'''
        sdict = self.__dict__
        sdict[self._OUTQ] = sdict[self._UTILQ]
        return self._clearwork()

    def _uq2iqoq(self):
        '''extend incoming queue and outgoing queue with utility queue'''
        sd = self.__dict__
        sd[self._INQ], sd[self._OUTQ] = self._split(sd[self._UTILQ])
        return self._clearwork()

    ###########################################################################
    ## switch context #########################################################
    ###########################################################################

    def ro(self):
        '''switch to read-only cotext'''
        return self.ctx3(outq=self._UTILVAR)._pre()._xreplace(
            self._iterable
        ).ctx1(workq=self._UTILVAR)

    def ctx3(self, **kw):
        '''switch to three-armed context'''
        return self.swap(
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
