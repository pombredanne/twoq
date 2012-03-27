# -*- coding: utf-8 -*-
'''active twoq mixins'''

from contextlib import contextmanager

from twoq.mixins.queuing import ThingsMixin, ResultMixin

__all__ = ('AutoQMixin', 'ManQMixin', 'AutoResultMixin', 'ManResultMixin')


class BaseQMixin(ThingsMixin):

    '''base active things'''

    def __init__(self, *things):
        deque_ = self._deek
        incoming = deque_(things[0]) if len(things) == 1 else deque_(things)
        super(BaseQMixin, self).__init__(incoming, deque_())
        # set iterator
        self._iterator = self._iterexcept
        # work things
        self._work = deque_()
        # utility things
        self._util = deque_()

    ###########################################################################
    ## thing length ###########################################################
    ###########################################################################

    def __len__(self):
        '''number of incoming things'''
        return self._len(self.incoming)

    def outcount(self):
        '''number of outgoing things'''
        return self._len(self.outgoing)

    ###########################################################################
    ## iterators ##############################################################
    ###########################################################################

    def __iter__(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        return self.iterexcept(self.outgoing.popleft, IndexError)

    @property
    def _iterable(self):
        '''iterable'''
        return self._iterator(self._WORKQ)

    def _iterexcept(self, attr='_UTILQ'):
        '''
        iterator broken on exception

        @param attr: things to iterate over
        '''
        return self.iterexcept(self._getr(attr).popleft, IndexError)

    def _breakcount(self, attr='_UTILQ'):
        '''
        breakcount iterator

        @param attr: things to iterate over
        '''
        dq = self._getr(attr)
        length = len(dq)
        return self.breakcount(dq.popleft, length, IndexError,)

    ###########################################################################
    ## clear things ###########################################################
    ###########################################################################

    def _uclear(self):
        '''clear utility things'''
        self._util.clear()
        return self

    def _wclear(self):
        '''clear work things'''
        self._work.clear()
        return self

    def inclear(self):
        '''clear incoming things'''
        self.incoming.clear()
        return self

    def outclear(self):
        '''clear outgoing things'''
        self.outgoing.clear()
        return self

    ###########################################################################
    ## extend #################################################################
    ###########################################################################

    def _xtend(self, things):
        '''extend utility things with `things` wrapped'''
        self._getr(self._UTILQ).extend(things)
        return self

    def _xtendleft(self, things):
        '''extend left side of utility things with `things`'''
        self._getr(self._UTILQ).extendleft(things)
        return self

    def _iter(self, things):
        '''extend work things with `things` wrapped in iterator'''
        self._getr(self._UTILQ).extend(iter(things))
        return self

    ###########################################################################
    ## append #################################################################
    ###########################################################################

    def _append(self, things):
        '''append `things` to utility things'''
        self._getr(self._UTILQ).append(things)
        return self

    def _appendleft(self, things):
        '''append `things` to left side of utility things'''
        self._getr(self._UTILQ).appendleft(things)
        return self

    ###########################################################################
    ## context rotation #######################################################
    ###########################################################################

    @contextmanager
    def ctx2(self, **kw):
        '''swap to two-armed context'''
        self.swap(
            outq=kw.get(self._OUTCFG, self._INVAR), context=self.ctx2(), **kw
        )
        getr_ = self._getr
        outq = getr_(self._OUTQ)
        utilq = getr_(self._UTILQ)
        workq = getr_(self._WORKQ)
        # clear all work things
        workq.clear()
        # extend work things with outgoing things
        workq.extend(outq)
        # swap iterator
        self._iterator = self._breakcount
        yield
        # clear outgoing things if so configured
        if self._clearout:
            outq.clear()
        # extend outgoing things with utility things
        outq.extend(utilq)
        # clear utility things
        utilq.clear()
        # return to global context
        self.reswap()

    @contextmanager
    def ctx3(self, **kw):
        '''swap to three-armed context'''
        self.swap(
            utilq=kw.get(self._WORKCFG, self._WORKVAR), context=self.ctx3, **kw
        )
        getr_ = self._getr
        outq = getr_(self._OUTQ)
        utilq = getr_(self._UTILQ)
        workq = getr_(self._WORKQ)
        # clear work things
        workq.clear()
        # extend work things with incoming things
        workq.extend(getr_(self._INQ))
        # swap iterators
        self._iterator = self._breakcount
        yield
        # clear outgoing things if so configured
        if self._clearout:
            outq.clear()
        # extend outgoing things with utility things
        outq.extend(utilq)
        # clear utility things
        utilq.clear()
        # return to global context
        self.reswap()

    @contextmanager
    def ctx4(self, **kw):
        '''swap to four-armed context'''
        self.swap(context=self.ctx4, **kw)
        getr_ = self._getr
        outq = getr_(self._OUTQ)
        utilq = getr_(self._UTILQ)
        workq = getr_(self._WORKQ)
        # clear work things
        workq.clear()
        # extend work things with incoming things
        workq.extend(getr_(self._INQ))
        # swap iterators
        self._iterator = self._iterexcept
        yield
        # clear outgoing things if so configured
        if self._clearout:
            outq.clear()
        # extend outgoing things with utility things
        outq.extend(utilq)
        # clear utility things
        utilq.clear()
        # return to global context
        self.reswap()

    @contextmanager
    def autoctx(self, **kw):
        '''swap to auto-synchronizing context'''
        self.swap(context=self.autoctx, **kw)
        getr_ = self._getr
        outq = getr_(self._OUTQ)
        utilq = getr_(self._UTILQ)
        workq = getr_(self._WORKQ)
        inq = getr_(self._INQ)
        # clear work things
        workq.clear()
        # extend work things with incoming things
        workq.extend(inq)
        # swap iterators
        self._iterator = self._iterexcept
        yield
        # clear outgoing things if so configured
        if self._clearout:
            outq.clear()
        outq.extend(utilq)
        # clear incoming things
        inq.clear()
        inq.extend(utilq)
        # clear utility things
        utilq.clear()
        # return to global context
        self.reswap()

    def ro(self):
        '''swap to read-only context'''
        with self.ctx3(outq=self._UTILVAR):
            self._xtend(self._iterable)
        with self.ctx1(hard=True, workq=self._UTILVAR):
            return self


class AutoQMixin(BaseQMixin):

    '''auto-balancing queue mixin'''

    _default_context = 'autoctx'


class ManQMixin(BaseQMixin):

    '''manually balanced queue mixin'''

    _default_context = 'ctx4'


class AutoResultMixin(AutoQMixin, ResultMixin):

    '''auto-balancing manipulation things (with results extractor) mixin'''


class ManResultMixin(ManQMixin, ResultMixin):

    '''manually balanced things (with results extractor) mixin'''
