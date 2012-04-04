# -*- coding: utf-8 -*-
'''active twoq mixins'''

from collections import deque
from contextlib import contextmanager

from stuf.utils import clsname

from twoq.queuing import ThingsMixin, ResultMixin


__all__ = ('AutoQMixin', 'ManQMixin', 'AutoResultMixin', 'ManResultMixin')


class BaseQMixin(ThingsMixin):

    '''base active things'''

    def __init__(self, *things):
        deque_ = deque
        incoming = deque_(things[0]) if len(things) == 1 else deque_(things)
        super(BaseQMixin, self).__init__(incoming, deque_())
        # set iterator
        self._iterator = self._iterexcept
        # work things
        self._work = deque_()
        # utility things
        self._util = deque_()

    def __repr__(self):
        getr_, list_ = lambda x: getattr(self, x), list
        return (
            '<{}.{}([IN: {}({}) => WORK: {}({}) => UTIL: {}({}) => '
            'OUT: {}: ({})]) at {}'
        ).format(
            self.__module__,
            clsname(self),
            self._INQ,
            list_(getr_(self._INQ)),
            self._WORKQ,
            list_(getr_(self._WORKQ)),
            self._UTILQ,
            list_(getr_(self._UTILQ)),
            self._OUTQ,
            list_(getr_(self._OUTQ)),
            id(self),
        )

    ###########################################################################
    ## thing length ###########################################################
    ###########################################################################

    def __len__(self):
        '''number of incoming things'''
        return len(self.incoming)

    def outcount(self):
        '''number of outgoing things'''
        return len(self.outgoing)

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
        return self.iterexcept(getattr(self, attr).popleft, IndexError)

    def _breakcount(self, attr='_UTILQ'):
        '''
        breakcount iterator

        @param attr: things to iterate over
        '''
        dq = getattr(self, attr)
        return self.breakcount(dq.popleft, len(dq), IndexError,)

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
        getattr(self, self._UTILQ).extend(things)
        return self

    def _xtendleft(self, things):
        '''extend left side of utility things with `things`'''
        getattr(self, self._UTILQ).extendleft(things)
        return self

    def _iter(self, things):
        '''extend work things with `things` wrapped in iterator'''
        getattr(self, self._UTILQ).extend(iter(things))
        return self

    ###########################################################################
    ## append #################################################################
    ###########################################################################

    def _append(self, things):
        '''append `things` to utility things'''
        getattr(self, self._UTILQ).append(things)
        return self

    def _appendleft(self, things):
        '''append `things` to left side of utility things'''
        getattr(self, self._UTILQ).appendleft(things)
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
        getr_ = lambda x: getattr(self, x)
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
        getr_ = lambda x: getattr(self, x)
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
        getr_ = lambda x: getattr(self, x)
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
        getr_ = lambda x: getattr(self, x)
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


class EndMixin(ResultMixin):

    '''result things mixin'''

    def end(self):
        '''return outgoing things then clear out everything'''
        # return to default context
        self.unswap()
        wrap, outgoing = self._wrapper, self.outgoing
        out = self.outgoing.pop() if len(outgoing) == 1 else wrap(outgoing)
        # clear every last thing
        self.clear()
        return out

    def value(self):
        '''return outgoing things and clear outgoing things'''
        # return to default context
        self.unswap()
        wrap, outgoing = self._wrapper, self.outgoing
        out = self.outgoing.pop() if len(outgoing) == 1 else wrap(outgoing)
        # clear outgoing things
        self.outclear()
        return out


class AutoResultMixin(AutoQMixin, EndMixin):

    '''auto-balancing manipulation things (with results extractor) mixin'''


class ManResultMixin(ManQMixin, EndMixin):

    '''manually balanced things (with results extractor) mixin'''
