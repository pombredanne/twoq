# -*- coding: utf-8 -*-
'''lazy twoq mixins'''

from contextlib import contextmanager

from twoq.mixins.queuing import QueueingMixin, ResultMixin

__all__ = ['AutoQMixin', 'ManQMixin']


class BaseQMixin(QueueingMixin):

    '''base lazy queue'''

    def __init__(self, *things):
        iter_ = self._iterz
        incoming = iter_([things[0]]) if len(things) == 1 else iter_(things)
        # work things
        self._work = iter_([])
        # utility things
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
        return self._getr(self._OUTQ)

    @property
    def _iterable(self):
        '''iterable'''
        return self._getr(self._WORKQ)

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _clearwork(self):
        '''clear work queue and utility queue'''
        iter_ = self._iterz
        setr_, delr_ = self._setr, self._delr
        WORKQ, UTILQ = self._WORKQ, self._UTILQ
        # clear work queue
        delr_(WORKQ)
        setr_(WORKQ, iter_([]))
        # clear utility queue
        delr_(UTILQ)
        setr_(UTILQ, iter_([]))
        return self

    def _uclear(self):
        '''clear utility queue'''
        UTILQ = self._UTILQ
        self._delr(UTILQ)
        self._setr(UTILQ, self._iterz([]))
        return self

    def _wclear(self):
        '''clear work queue'''
        WORKQ = self._WORKQ
        self._delr(WORKQ)
        self._setr(WORKQ, self._iterz([]))
        return self

    def inclear(self):
        '''clear incoming things'''
        INQ = self._INQ
        self._delr(INQ)
        self._setr(INQ, self._iterz([]))
        return self

    def outclear(self):
        '''clear outgoing things'''
        OUTQ = self._OUTQ
        self._delr(OUTQ)
        self._setr(OUTQ, self._iterz([]))
        return self

    ###########################################################################
    ## extend #################################################################
    ###########################################################################

    def _xtend(self, thing):
        '''build chain'''
        UTILQ = self._UTILQ
        self._setr(UTILQ, self._join(thing, self._getr(UTILQ)))
        return self

    __buildchain = _xtend

    def _xtendleft(self, things):
        '''extend left side of work queue with `things`'''
        return self.__buildchain(self._reversed(things))

    def _xreplace(self, thing):
        '''build chain'''
        self._setr(self._UTILQ, thing)
        return self

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
    ## context rotation #######################################################
    ###########################################################################

    @contextmanager
    def ctx2(self, **kw):
        '''swap context to two-armed context'''
        self.swap(
            context=self.ctx2, outq=kw.get(self._OUTCFG, self._INVAR), **kw
        )._clearwork()
        setr_, getr_, OUTQ = self._setr, self._getr, self._OUTQ
        # extend work queue with outgoing queue
        work, out = self._split(getr_(OUTQ))
        setr_(self._WORKQ, work)
        setr_(OUTQ, out)
        yield
        # extend outgoing queue with utility queue
        util = getr_(self._UTILQ)
        setr_(
            self._OUTQ,
            util if self._clearout else self._join(util, getr_(self._OUTQ)),
        )
        self._clearwork()
        # return to global context
        self.reswap()

    @contextmanager
    def ctx3(self, **kw):
        '''swap context to three-armed context'''
        self.swap(
            utilq=kw.get(self._WORKCFG, self._WORKVAR), context=self.ctx3, **kw
        )._clearwork()
        setr_, getr_, INQ = self._setr, self._getr, self._INQ
        # extend work queue with incoming queue
        work, inq = self._split(getr_(INQ))
        setr_(self._WORKQ, work)
        setr_(INQ, inq)
        yield
        # extend outgoing queue with utility queue
        util = getr_(self._UTILQ)
        setr_(
            self._OUTQ,
            util if self._clearout else self._join(util, getr_(self._OUTQ)),
        )
        self._clearwork()
        # return to global context
        self.reswap()

    @contextmanager
    def ctx4(self, **kw):
        '''swap context to three-armed context'''
        self.swap(context=self.ctx4, **kw)._clearwork()
        setr_, getr_, INQ = self._setr, self._getr, self._INQ
        # extend work queue with incoming queue
        work, inq = self._split(getr_(INQ))
        setr_(self._WORKQ, work)
        setr_(INQ, inq)
        yield
        # extend outgoing queue with utility queue
        util = getr_(self._UTILQ)
        setr_(
            self._OUTQ,
            util if self._clearout else self._join(util, getr_(self._OUTQ)),
        )
        self._clearwork()
        # return to global context
        self.reswap()

    @contextmanager
    def autoctx(self, **kw):
        '''swap context to four-armed context'''
        self.swap(context=self.autoctx, **kw)._clearwork()
        setr_, getr_ = self._setr, self._getr
        INQ, split_ = self._INQ, self._split
        # extend work queue with incoming queue
        work, inq = self._split(getr_(INQ))
        setr_(self._WORKQ, work)
        setr_(INQ, inq)
        yield
        # extend incoming queue and outgoing queue with utility queue
        inq, out = split_(getr_(self._UTILQ))
        setr_(
            self._OUTQ,
            out if self._clearout else self._join(out, getr_(self._OUTQ)),
        )
        setr_(INQ, inq)
        self._clearwork()
        # return to global context
        self.reswap()

    def ro(self):
        '''swap context to read-only context'''
        with self.ctx3(outq=self._UTILVAR):
            self._xreplace(self._iterable)
        with self.ctx1(hard=True, workq=self._UTILVAR):
            return self


class AutoQMixin(BaseQMixin):

    '''auto-balancing queue mixin'''

    _default_context = 'autoctx'


class ManQMixin(BaseQMixin):

    '''manually balanced queue mixin'''

    _default_context = 'ctx4'


class AutoResultMixin(ResultMixin, AutoQMixin):

    '''auto-balancing queue (with results extraction) mixin'''


class ManResultMixin(ResultMixin, ManQMixin):

    '''manually balanced queue (with results extraction) mixin'''
