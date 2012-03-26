# -*- coding: utf-8 -*-
'''twoq queuing mixins'''

import itertools
import functools
from threading import local
from collections import deque
from operator import methodcaller
from contextlib import contextmanager

from twoq.support import lazier, filterfalse, imap, ifilter, items, range

__all__ = ['QueueingMixin']


class QueueingMixin(local):

    '''queue management mixin'''

    _INCFG = 'inq'
    _INVAR = 'incoming'
    _OUTCFG = 'outq'
    _OUTVAR = 'outgoing'
    _UTILCFG = 'utilq'
    _UTILVAR = '_util'
    _WORKCFG = 'workq'
    _WORKVAR = '_work'

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

    _deek = lazier(deque)
    _filterfalse = lazier(filterfalse)
    _ichain = lazier(itertools.chain.from_iterable)
    _ifilter = lazier(ifilter)
    _imap = lazier(imap)
    _ireduce = lazier(functools.reduce)
    _islice = lazier(itertools.islice)
    _items = lazier(items)
    _iterz = lazier(iter)
    _join = lazier(itertools.chain)
    _len = lazier(len)
    _list = lazier(list)
    _methodcaller = lazier(methodcaller)
    _next = lazier(next)
    _partial = lazier(functools.partial)
    _range = lazier(range)
    _repeat = lazier(itertools.repeat)
    _reversed = lazier(reversed)
    _sorted = lazier(sorted)
    _split = lazier(itertools.tee)
    _starmap = lazier(itertools.starmap)
    _sum = lazier(sum)

    ###########################################################################
    ## iteration ##############################################################
    ###########################################################################

    @property
    def balanced(self):
        '''if queues are balanced'''
        return self.outcount() == self.__len__()

    ###########################################################################
    ## queue clearance ########################################################
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
        '''
        swap contexts

        @param hard: keep context-specific settings between context switches
        '''
        self._context = kw.get('context', getattr(self, self._default_context))
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
        self._CONFIG = kw if kw.get('hard', False) else {}
        return self

    def unswap(self):
        '''rotate queues to default'''
        return self.swap()

    rw = unswap

    def reswap(self):
        '''rotate queues to current configuration'''
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
    ## queue rotation #########################################################
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
    ## queue appending ########################################################
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
    ## queue extension ########################################################
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
    def exhaustmap(cls, map, call, filter=False, exception=StopIteration):
        '''
        call `next` on an iterator until it's exhausted

        @param mapping: a mapping to exhaust
        @param call: call to handle what survives the filter
        @param filter: a filter to apply to mapping (default: `None`)
        @param exception: exception sentinel (default: `StopIteration`)
        '''
        next_, starmap_, items_ = cls._next, cls._starmap, cls._items
        subiter = cls._ifilter(filter, items_(map)) if filter else items_(map)
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


class ResultMixin(local):

    '''result queue mixin'''

    def end(self):
        '''return outgoing things then clear out everything'''
        self.unswap()
        out, tell = self._split(self.outgoing)
        list_ = self._list
        out = self._next(out) if self._len(list_(tell)) == 1 else list_(out)
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
        '''results in read-only mode'''
        out = self._list(self._util)
        return out[0] if self._len(out) == 1 else out

    def results(self):
        '''yield outgoing things, clearing outgoing things as it iterates'''
        return self.__iter__()

    def value(self):
        '''return outgoing things and clear outgoing things'''
        self.unswap()
        out, tell = self._split(self.outgoing)
        list_ = self._list
        out = self._next(out) if self._len(list_(tell)) == 1 else list_(out)
        self.outclear()
        return out
