# -*- coding: utf-8 -*-
'''twoq queuing mixins'''

from threading import local
from collections import deque
from operator import methodcaller
from functools import reduce as ireduce, partial
from itertools import islice, tee, starmap, repeat

from twoq.support import (
    lazier, ichain, filterfalse, imap, ifilter, chain, items, range)

__all__ = ['QueueingMixin']


class QueueingMixin(local):

    '''queue management mixin'''

    _INCFG = 'inq'
    _INVAR = 'incoming'
    _OUTCFG = 'outq'
    _OUTVAR = 'outgoing'
    _WORKCFG = 'workq'
    _WORKVAR = '_work'
    _UTILCFG = 'utilq'
    _UTILVAR = '_util'

    def __init__(self, incoming, outgoing):
        '''
        init

        @param incoming: incoming things
        @param outgoing: outgoing things
        '''
        super(QueueingMixin, self).__init__()
        # incoming queue
        self.incoming = incoming
        # outgoing queue
        self.outgoing = outgoing
        # set defaults
        self.detap().unswap()

    ###########################################################################
    ## lookup optimizations ###################################################
    ###########################################################################

    _iterz = lazier(iter)
    _deek = lazier(deque)
    _filterfalse = lazier(filterfalse)
    _ichain = lazier(ichain)
    _ifilter = lazier(ifilter)
    _imap = lazier(imap)
    _ireduce = lazier(ireduce)
    _islice = lazier(islice)
    _join = lazier(chain)
    _len = lazier(len)
    _list = lazier(list)
    _methodcaller = lazier(methodcaller)
    _next = lazier(next)
    _partial = lazier(partial)
    _reversed = lazier(reversed)
    _sorted = lazier(sorted)
    _split = lazier(tee)
    _starmap = lazier(starmap)
    _sum = lazier(sum)
    _items = lazier(items)
    _repeat = lazier(repeat)
    _range = lazier(range)

    ###########################################################################
    ## iteration ##############################################################
    ###########################################################################

    def __iter__(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        return self._iterator(self._OUTQ)

    @property
    def _iterable(self):
        '''iterable'''
        return self._iterator(self._WORKQ)

    @property
    def balanced(self):
        '''if queues are balanced'''
        return self.outcount() == self.__len__()

    def ahead(self, n=None):
        '''
        move iterator for incoming things `n`-steps ahead

        If `n` is `None`, consume entirely.

        @param n: number of steps to advance incoming things (default: None)
        '''
        # use functions that consume iterators at C speed
        if n is None:
            # feed the entire iterator into a zero-length `deque`
            self.incoming = self._deek(self.incoming, maxlen=0)
        else:
            # advance to the empty slice starting at position `n`
            self._next(self._islice(self.incoming, n, n), None)
        return self

    ###########################################################################
    ## queue clearance ########################################################
    ###########################################################################

    def _wclear(self):
        '''clear work queue'''
        return self.ctx1(workq=self._WORKVAR)._pre()._clear().reswap()

    def _uclear(self):
        '''clear utility queue'''
        return self.ctx1(workq=self._UTILVAR)._pre()._clear().reswap()

    def clear(self):
        '''clear every thing'''
        return self.detap().outclear().inclear()._wclear()._uclear()

    def inclear(self):
        '''clear incoming things'''
        return self.ctx1()._pre()._clear().reswap()

    def outclear(self):
        '''clear outgoing things'''
        return self.ctx1(workq=self._OUTVAR)._pre()._clear().reswap()

    ###########################################################################
    ## context management #####################################################
    ###########################################################################

    def ctx1(self, hard=False, **kw):
        '''
        switch to one-armed context manager

        @param hard: keep context-specific settings between context switches
        '''
        q = kw.pop(self._WORKCFG, self._INVAR)
        ctx = lambda: self
        return self.swap(hard=hard, workq=q, utilq=q, pre=ctx, post=ctx, **kw)

    def ctx2(self, hard=False, **kw):
        '''
        switch to two-armed context manager

        @param hard: keep context-specific settings between context switches
        '''
        return self.swap(
            hard=hard,
            outq=kw.get(self._OUTCFG, self._INVAR),
            pre=self._oq2wq,
            post=self._uq2oq,
            **kw
        )

    def ctx4(self, hard=False, **kw):
        '''
        switch to four-armed context manager

        @param hard: keep context-specific settings between context switches
        '''
        return self.swap(hard=hard, post=self._uq2oq, **kw)

    def autoctx(self, hard=False, **kw):
        '''
        switch to auto-synchronizing context manager

        @param hard: keep context-specific settings between context switches
        '''
        return self.swap(hard=hard, post=self._uq2iqoq, **kw)

    def swap(self, hard=False, **kw):
        '''
        swap contexts

        @param hard: keep context-specific settings between context switches
        '''
        self._pre = kw.get('pre', self._iq2wq)
        self._post = kw.get('post', getattr(self, self._default_post))
        # clear out outgoing things before extending them?
        self._clearout = kw.get('clearout', True)
        # incoming queue
        self._INQ = kw.get(self._INCFG, self._INVAR)
        # outgoing queue
        self._OUTQ = kw.get(self._OUTCFG, self._OUTVAR)
        # work queue
        self._WORKQ = kw.get(self._WORKCFG, self._WORKVAR)
        # utility queue
        self._UTILQ = kw.get(self._UTILCFG, self._UTILVAR)
        # preserve configuration or return to defaults
        self._CONFIG = kw if hard else {}
        return self

    def unswap(self):
        '''rotate queues to default'''
        return self.swap()

    def reswap(self):
        '''rotate queues to current configuration'''
        return self.swap(**self._CONFIG)

    rw = unswap

    ###########################################################################
    ## current callable management ############################################
    ###########################################################################

    def args(self, *args, **kw):
        '''arguments for active callable'''
        # set positional arguments
        self._args = args
        # set keyword arguemnts
        self._kw = kw
        return self

    def tap(self, call):
        '''
        set active callable

        @param call: a call
        '''
        self.detap()
        # set active callable
        self._call = call
        return self

    def detap(self):
        '''clear active callable'''
        # reset postitional arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # reset callable
        self._call = None
        return self

    def wrap(self, call):
        '''build active callable from factory'''
        def factory(*args, **kw):
            return call(*args, **kw)
        return self.tap(factory)

    # alias
    unwrap = detap

    ###########################################################################
    ## queue rotation #########################################################
    ###########################################################################

    def reup(self):
        '''put incoming things in incoming things as one incoming thing'''
        return self.ctx1()._pre()._append(list(self._iterable)).reswap()

    def shift(self):
        '''shift outgoing things to incoming things'''
        return self.autoctx(
            inq=self._OUTVAR, outq=self._INVAR
        )._pre()._xtend(self._iterable).reswap()

    sync = shift

    def outshift(self):
        '''shift incoming things to outgoing things'''
        return self.autoctx()._pre()._xtend(self._iterable).reswap()

    outsync = outshift

    ###########################################################################
    ## queue appending ########################################################
    ###########################################################################

    def _inappend(self, call):
        return self._pre()._append(call(self._iterable))

    def _pappend(self, iterable):
        return self._pre()._append(iterable)

    def append(self, thing):
        '''
        append thing to right side of incoming things

        @param thing: some thing
        '''
        return self.ctx1()._pre()._append(thing).reswap()

    def appendleft(self, thing):
        '''
        append `thing` to left side of incoming things

        @param thing: some thing
        '''
        return self.ctx2()._pre()._appendleft(thing).reswap()

    def _areduce(self, call, initial=None):
        '''
        reduce iterable and append results to outgoing things

        @param call: filter callable
        @param initial: initializer (default: None)
        '''
        if initial is None:
            return self._pre()._append(self._ireduce(call, self._iterable))
        return self._pre()._append(
            self._ireduce(call, self._iterable, initial)
        )

    ###########################################################################
    ## queue extension ########################################################
    ###########################################################################

    def _x2map(self, call1, iterator):
        imap_ = self._imap
        return self._pre()._xtend(imap_(call1, iterator(self._iterable)))

    def _xreduce(self, call, initial=None):
        '''
        reduce iterable and extend outgoing things with results

        @param call: filter callable
        @param initial: initializer (default: None)
        '''
        if initial is None:
            return self._pre()._xtend(self._ireduce(call, self._iterable))
        return self._pre()._xtend(
            self._ireduce(call, self._iterable, initial)
        )

    def _pextend(self, iterable):
        return self._pre()._xtend(iterable)

    def _inextend(self, call):
        return self._pre()._xtend(call(self._iterable))

    def _xstarmap(self, call, iterable):
        return self._pre()._xtend(self._starmap(call, iterable))

    def _x2starmap(self, call, iterator):
        return self._pre()._xtend(
            self._starmap(call, iterator(self._iterable))
        )

    def _xinmap(self, call):
        return self._pre()._xtend(self._imap(call, self._iterable))

    def _xinstarmap(self, call):
        return self._pre()._xtend(self._starmap(call, self._iterable))

    def extend(self, things):
        '''
        extend right side of incoming things with `things`

        @param thing: some things
        '''
        return self.ctx1()._pre()._xtend(things).reswap()

    def extendleft(self, things):
        '''
        extend left side of incoming things with `things`

        @param thing: some things
        '''
        return self.ctx1()._pre()._xtendleft(things).reswap()

    def outextend(self, things):
        '''
        extend right side of outgoing things with `things`

        @param thing: some things
        '''
        return self.ctx1(workq=self._OUTVAR)._pre()._xtend(things).reswap()

    ###########################################################################
    ## iteration runners ######################################################
    ###########################################################################

    def _inmap(self, call):
        return self._imap(call, self._iterable)

    @classmethod
    def breakcount(cls, call, length):
        '''
        rotate through iterator until it reaches its original length

        @param iterable: an iterable to exhaust
        '''
        for i in cls._range(0, length):  # @UnusedVariable
            yield call()

    @classmethod
    def exhaust(cls, iterable, exception=StopIteration):
        '''
        call next on an iterator until it's exhausted

        @param iterable: iterable to exhaust
        @param exception: exception marking end of iteration
        '''
        next_ = cls._next
        try:
            while 1:
                next_(iterable)
        except exception:
            pass

    @classmethod
    def exhaustmap(cls, mapr, call, filter=False, exception=StopIteration):
        '''
        call `next` on an iterator until it's exhausted

        @param mapping: a mapping to exhaust
        @param call: call to handle what survives the filter
        @param filter: a filter to apply to mapping (default: `None`)
        @param exception: exception sentinel (default: `StopIteration`)
        '''
        next_, starmap_ = cls._next, cls._starmap
        subiter = cls._ifilter(
            filter, cls._items(mapr)
        ) if filter else cls._items(mapr)
        try:
            while 1:
                next_(starmap_(call, subiter))
        except exception:
            pass

    @staticmethod
    def iterexcept(call, exception, start=None):
        '''
        call a function repeatedly until an exception is raised

        Converts a call-until-exception interface to an iterator interface.
        Like `__builtin__.iter(call, sentinel)` but uses an exception instead
        of a sentinel to end the loop.

        Raymond Hettinger Python Cookbook recipe # 577155
        '''
        try:
            if start is not None:
                yield start()
            while 1:
                yield call()
        except exception:
            pass


class ResultMixin(local):

    '''result queue mixin'''

    def __results(self, iterable):
        list_ = self._list
        self.unswap()
        out, tell = self._split(iterable)
        return self._next(out) if self._len(list_(tell)) == 1 else list_(out)

    def end(self):
        '''return outgoing things then clear out everything'''
        out = self.__results(self.outgoing)
        self.clear()
        return out

    def first(self):
        '''first incoming thing'''
        return self._inappend(self._next)

    def last(self):
        '''last incoming thing'''
        self._pre()
        i1, _ = self._split(self._iterable)
        return self._append(self._deek(i1, maxlen=1).pop())

    def peek(self):
        '''results in read-only mode'''
        out = self._list(self._util)
        return out[0] if self._len(out) == 1 else out

    def results(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        return self.__iter__()

    def value(self):
        '''return outgoing things and clear outgoing things'''
        out = self.__results(self.outgoing)
        self.outclear()
        return out
