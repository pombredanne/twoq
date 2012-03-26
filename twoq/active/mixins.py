# -*- coding: utf-8 -*-
'''active twoq mixins'''

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
        return self._post()

    def _xtendleft(self, things):
        '''extend left side of utility things with `things`'''
        self.__dict__[self._UTILQ].extendleft(things)
        return self._post()

    def _iter(self, things):
        '''extend work things with `things` wrapped in iterator'''
        self.__dict__[self._UTILQ].extend(iter(things))
        return self._post()

    ###########################################################################
    ## append #################################################################
    ###########################################################################

    def _append(self, things):
        '''append `things` to utility things'''
        self.__dict__[self._UTILQ].append(things)
        return self._post()

    def _appendleft(self, things):
        '''append `things` to left side of utility things'''
        self.__dict__[self._UTILQ].appendleft(things)
        return self._post()

    ###########################################################################
    ## enter context ##########################################################
    ###########################################################################

    def _iq2wq(self):
        '''extend work things with incoming things'''
        sdict = self.__dict__
        workq = sdict[self._WORKQ]
        # clear work things
        workq.clear()
        # extend work things with incoming things
        workq.extend(sdict[self._INQ])
        # switch iterator
        self._iterator = self._iterexcept
        return self

    def _iq2wq2(self):
        '''extend work things with incoming things'''
        sdict = self.__dict__
        workq = sdict[self._WORKQ]
        # clear work things
        workq.clear()
        # extend work things with incoming things
        workq.extend(sdict[self._INQ])
        # switch iterator
        self._iterator = self._breakcount
        return self

    def _oq2wq(self):
        '''extend work things with outgoing things'''
        sdict = self.__dict__
        workq = sdict[self._WORKQ]
        # clear all work things
        workq.clear()
        # extend work things with outgoing things
        workq.extend(sdict[self._OUTQ])
        # switch iterator
        self._iterator = self._breakcount
        return self

    ###########################################################################
    ## exit context ###########################################################
    ###########################################################################

    def _uq2oq(self):
        '''extend outgoing things with utility things'''
        sdict = self.__dict__
        outq, utilq = sdict[self._OUTQ], sdict[self._UTILQ]
        # clear outgoing things if so configured
        if self._clearout:
            outq.clear()
        # extend outgoing things with utility things
        outq.extend(utilq)
        # clear utility things
        utilq.clear()
        return self

    def _uq2iqoq(self):
        '''extend outgoing things, incoming things with utility things'''
        sdict = self.__dict__
        inq = sdict[self._INQ]
        outq = sdict[self._OUTQ]
        utilq = sdict[self._UTILQ]
        # clear outgoing things if so configured
        if self._clearout:
            outq.clear()
        outq.extend(utilq)
        # clear incoming things
        inq.clear()
        inq.extend(utilq)
        # clear utility things
        utilq.clear()
        return self

    ###########################################################################
    ## rotate context #########################################################
    ###########################################################################

    def ro(self):
        '''switch to read-only context'''
        return self.ctx3(outq=self._UTILVAR)._pre()._xtend(
            self._iterable
        ).ctx1(workq=self._UTILVAR)

    def ctx3(self, **kw):
        '''switch to three-armed context'''
        return self.swap(
            utilq=kw.get(self._WORKCFG, self._WORKVAR),
            pre=self._iq2wq2,
            post=self._uq2oq,
            **kw
        )


class AutoQMixin(BaseQMixin):

    '''auto-balancing things mixin'''

    _default_post = '_uq2iqoq'


class ManQMixin(BaseQMixin):

    '''manually balanced things mixin'''

    _default_post = '_uq2oq'


class AutoResultMixin(AutoQMixin, ResultMixin):

    '''auto-balancing manipulation things (with results extractor) mixin'''


class ManResultMixin(ManQMixin, ResultMixin):

    '''manually balanced things (with results extractor) mixin'''
