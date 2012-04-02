# -*- coding: utf-8 -*-
'''twoq queuing mixins'''

import itertools
import functools
from threading import local
from collections import deque
from operator import methodcaller
from contextlib import contextmanager

from stuf.utils import lazy, clsname

from twoq import support

__all__ = ('ResultMixin', 'ThingsMixin')

lazier = support.lazier


class ThingsMixin(local):

    '''things management mixin'''

    # 1. incoming things
    _INCFG = 'inq'
    _INVAR = 'incoming'
    # 2. utility things
    _UTILCFG = 'utilq'
    _UTILVAR = '_util'
    # 3. work things
    _WORKCFG = 'workq'
    _WORKVAR = '_work'
    # 4. outgoing things
    _OUTCFG = 'outq'
    _OUTVAR = 'outgoing'

    def __init__(self, incoming, outgoing):
        '''
        init

        @param incoming: incoming things
        @param outgoing: outgoing things
        '''
        super(ThingsMixin, self).__init__()
        # incoming things
        self.incoming = incoming
        # outgoing things
        self.outgoing = outgoing
        # current callable
        self._call = None
        # reset postitional arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # set defaults
        self.unswap()

    ###########################################################################
    ## optimize lookups #######################################################
    ###########################################################################

    _clsname = lazier(clsname)
    _deek = lazier(deque)
    _filterfalse = lazier(support.filterfalse)
    _ichain = lazier(itertools.chain.from_iterable)
    _ifilter = lazier(support.ifilter)
    _imap = lazier(support.imap)
    _ireduce = lazier(functools.reduce)
    _islice = lazier(itertools.islice)
    _items = lazier(support.items)
    _iterz = lazier(iter)
    _join = lazier(itertools.chain)
    _len = lazier(len)
    _list = lazier(list)
    _methodcaller = lazier(methodcaller)
    _next = lazier(next)
    _partial = lazier(functools.partial)
    _range = lazier(support.range)
    _repeat = lazier(itertools.repeat)
    _reversed = lazier(reversed)
    _sorted = lazier(sorted)
    _split = lazier(itertools.tee)
    _starmap = lazier(itertools.starmap)
    _sum = lazier(sum)

    @lazy
    def _getr(self):
        '''local getter'''
        return self._partial(local.__getattribute__, self)

    @lazy
    def _setr(self):
        '''local setter'''
        return self._partial(local.__setattr__, self)

    @lazy
    def _delr(self):
        '''local deleter'''
        return self._partial(local.__delattr__, self)

    ###########################################################################
    ## iteration ##############################################################
    ###########################################################################

    @property
    def balanced(self):
        '''if queues are balanced'''
        return self.outcount() == self.__len__()

    ###########################################################################
    ## things clearance #######################################################
    ###########################################################################

    def clear(self):
        '''clear every thing'''
        return self.detap().outclear().inclear()._wclear()._uclear()

    ###########################################################################
    ## context rotation #######################################################
    ###########################################################################

    @contextmanager
    def ctx1(self, **kw):
        '''swap to one-armed context'''
        q = kw.pop(self._WORKCFG, self._INVAR)
        self.swap(workq=q, utilq=q, context=self.ctx1, **kw)
        yield
        # return to global context
        self.reswap()

    def swap(self, hard=False, **kw):
        '''swap contexts'''
        self._context = kw.get('context', self._getr(self._default_context))
        # clear out outgoing things before extending them?
        self._clearout = kw.get('clearout', True)
        # keep context-specific settings between context swaps
        self._CONFIG = kw if kw.get('hard', False) else {}
        # 1. incoming things
        self._INQ = kw.get(self._INCFG, self._INVAR)
        # 2. work things
        self._WORKQ = kw.get(self._WORKCFG, self._WORKVAR)
        # 3. utility things
        self._UTILQ = kw.get(self._UTILCFG, self._UTILVAR)
        # 4. outgoing things
        self._OUTQ = kw.get(self._OUTCFG, self._OUTVAR)
        return self

    def unswap(self):
        '''swap context to default context'''
        return self.swap()

    rw = unswap

    def reswap(self):
        '''swap contexts to current preferred context'''
        return self.swap(**self._CONFIG)

    ###########################################################################
    ## current callable management ############################################
    ###########################################################################

    def args(self, *args, **kw):
        '''arguments for current callable'''
        # set positional arguments
        self._args = args
        # set keyword arguemnts
        self._kw = kw
        return self

    def tap(self, call):
        '''
        set current callable

        @param call: a callabler
        '''
        # reset postitional arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # set current callable
        self._call = call
        return self

    def detap(self):
        '''clear current callable'''
        # reset postitional arguments
        self._args = ()
        # reset keyword arguments
        self._kw = {}
        # reset current callable
        self._call = None
        return self

    unwrap = detap

    def wrap(self, call):
        '''
        build current callable from factory

        @param call: a callable
        '''
        def factory(*args, **kw):
            return call(*args, **kw)
        return self.tap(factory)

    ###########################################################################
    ## things rotation ########################################################
    ###########################################################################

    def outshift(self):
        '''shift incoming things to outgoing things'''
        with self.autoctx():
            return self._xtend(self._iterable)

    outsync = outshift

    def reup(self):
        '''put incoming things in incoming things as one incoming thing'''
        with self.ctx2():
            return self._append(self._list(self._iterable))

    def shift(self):
        '''shift outgoing things to incoming things'''
        with self.autoctx(inq=self._OUTVAR, outq=self._INVAR):
            return self._xtend(self._iterable)

    sync = shift

    ###########################################################################
    ## things appending #######################################################
    ###########################################################################

    def append(self, thing):
        '''
        append thing to right side of incoming things

        @param thing: some thing
        '''
        with self.ctx1():
            return self._append(thing)

    def appendleft(self, thing):
        '''
        append `thing` to left side of incoming things

        @param thing: some thing
        '''
        with self.ctx1():
            return self._appendleft(thing)

    ###########################################################################
    ## things extension #######################################################
    ###########################################################################

    def extend(self, things):
        '''
        extend right side of incoming things with `things`

        @param thing: some things
        '''
        with self.ctx1():
            return self._xtend(things)

    def extendleft(self, things):
        '''
        extend left side of incoming things with `things`

        @param thing: some things
        '''
        with self.ctx1():
            return self._xtendleft(things)

    def outextend(self, things):
        '''
        extend right side of outgoing things with `things`

        @param thing: some things
        '''
        with self.ctx1(workq=self._OUTVAR):
            return self._xtend(things)

    ###########################################################################
    ## iteration runners ######################################################
    ###########################################################################

    @classmethod
    def breakcount(cls, call, length, exception=StopIteration):
        '''
        rotate through iterator until it reaches its original length

        @param iterable: an iterable to exhaust
        '''
        for i in cls._repeat(None, length):  # @UnusedVariable
            try:
                yield call()
            except exception:
                pass

    @staticmethod
    def iterexcept(call, exception, start=None):
        '''
        call a function repeatedly until an exception is raised

        Converts a call-until-exception interface to an iterator interface.
        Like `iter(call, sentinel)` but uses an exception instead of a sentinel
        to end the loop.

        Raymond Hettinger, Python Cookbook recipe # 577155
        '''
        try:
            if start is not None:
                yield start()
            while 1:
                yield call()
        except exception:
            pass

    ###########################################################################
    ## exhaustion iterators ###################################################
    ###########################################################################

    def exhaust(self, iterable, exception=StopIteration):
        '''
        call next on an iterator until it's exhausted

        @param iterable: iterable to exhaust
        @param exception: exception marking end of iteration
        '''
        next_ = self._next
        try:
            while 1:
                next_(iterable)
        except exception:
            pass

    def exhaustcall(self, call, iterable, exception=StopIteration):
        '''
        call function on an iterator until it's exhausted

        @param call: call that does the exhausting
        @param iterable: iterable to exhaust
        @param exception: exception marking end of iteration
        '''
        next_ = self._next
        iterable = self._imap(call, iterable)
        try:
            while True:
                next_(iterable)
        except exception:
            pass
        return self

    def exhaustitems(self, maps, call, filter=False, exception=StopIteration):
        '''
        call `next` on an iterator until it's exhausted

        @param mapping: a mapping to exhaust
        @param call: call to handle what survives the filter
        @param filter: a filter to apply to mapping (default: `None`)
        @param exception: exception sentinel (default: `StopIteration`)
        '''
        next_, items = self._next, self._items
        iterable = self._starmap(
            call, self._ifilter(filter, items(maps)) if filter else items(maps)
        )
        try:
            while 1:
                next_(iterable)
        except exception:
            pass
        return self


class ResultMixin(local):

    '''result things mixin'''

    def end(self):
        '''return outgoing things then clear out everything'''
        # return to default context
        self.unswap()
        out, tell = self._split(self.outgoing)
        list_ = self._list
        out = self._next(out) if self._len(list_(tell)) == 1 else list_(out)
        # clear every last thing
        self.clear()
        return out

    def first(self):
        '''first incoming thing'''
        with self._context():
            return self._append(self._next(self._iterable))

    def last(self):
        '''last incoming thing'''
        with self._context():
            i1, _ = self._split(self._iterable)
            return self._append(self._deek(i1, maxlen=1).pop())

    def peek(self):
        '''results from read-only context'''
        out = self._list(self._util)
        return out[0] if self._len(out) == 1 else out

    def results(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        return self.__iter__()

    def value(self):
        '''return outgoing things and clear outgoing things'''
        # return to default context
        self.unswap()
        out, tell = self._split(self.outgoing)
        list_ = self._list
        out = self._next(out) if self._len(list_(tell)) == 1 else list_(out)
        # clear outgoing things
        self.outclear()
        return out
