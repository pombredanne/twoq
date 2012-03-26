# -*- coding: utf-8 -*-
'''active twoq mixins'''

from contextlib import contextmanager

from twoq.mixins.queuing import QueueingMixin, ResultMixin


__all__ = ('AutoQMixin', 'ManQMixin')


class BaseQMixin(QueueingMixin):

    '''base active things'''

    def __init__(self, *things):
        deque_ = self._deek
        incoming = deque_(things[0]) if len(things) == 1 else deque_(things)
        self._iterator = self._iterexcept
        # work things
        self._work = deque_()
        # utility things
        self._util = deque_()
        super(BaseQMixin, self).__init__(incoming, deque_())

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
        return self._iterator(self._OUTQ)

    @property
    def _iterable(self):
        '''iterable'''
        return self._iterator(self._WORKQ)

    def _iterexcept(self, attr='_UTILQ'):
        '''
        iterator broken on exception

        @param attr: things to iterate over
        '''
        return self.iterexcept(self.__dict__[attr].popleft, IndexError)

    def _breakcount(self, attr='_UTILQ'):
        '''
        breakcount iterator

        @param attr: things to iterate over
        '''
        return self.breakcount(self.__dict__[attr].popleft, self.__len__())

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
        self.__dict__[self._UTILQ].extend(things)
        return self

    def _xtendleft(self, things):
        '''extend left side of utility things with `things`'''
        self.__dict__[self._UTILQ].extendleft(things)
        return self

    def _iter(self, things):
        '''extend work things with `things` wrapped in iterator'''
        self.__dict__[self._UTILQ].extend(iter(things))
        return self

    ###########################################################################
    ## append #################################################################
    ###########################################################################

    def _append(self, things):
        '''append `things` to utility things'''
        self.__dict__[self._UTILQ].append(things)
        return self

    def _appendleft(self, things):
        '''append `things` to left side of utility things'''
        self.__dict__[self._UTILQ].appendleft(things)
        return self

    ###########################################################################
    ## context rotation #######################################################
    ###########################################################################

    @contextmanager
    def ctx2(self, **kw):
        '''swap context to two-armed context manager'''
        sd = self.swap(
            outq=kw.get(self._OUTCFG, self._INVAR), context=self.ctx2(),
        **kw).__dict__
        outq, utilq, workq = sd[self._OUTQ], sd[self._UTILQ], sd[self._WORKQ]
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
        '''swap context to three-armed context'''
        sd = self.swap(
            utilq=kw.get(self._WORKCFG, self._WORKVAR),
            context=self.ctx3,
            **kw
        ).__dict__
        outq, utilq, workq = sd[self._OUTQ], sd[self._UTILQ], sd[self._WORKQ]
        # clear work things
        workq.clear()
        # extend work things with incoming things
        workq.extend(sd[self._INQ])
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
        '''swap context to four-armed context manager'''
        sd = self.swap(context=self.ctx4, **kw).__dict__
        outq, utilq, workq = sd[self._OUTQ], sd[self._UTILQ], sd[self._WORKQ]
        # clear work things
        workq.clear()
        # extend work things with incoming things
        workq.extend(sd[self._INQ])
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
        '''swap context to auto-synchronizing context manager'''
        sd = self.swap(context=self.autoctx, **kw).__dict__
        outq, utilq, workq = sd[self._OUTQ], sd[self._UTILQ], sd[self._WORKQ]
        inq = sd[self._INQ]
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
        '''swap context to read-only context'''
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
