# -*- coding: utf-8 -*-
'''twoq core'''

import time

import math as mt
import copy as cp
import heapq as hq
import random as rm
import operator as op
import itertools as it
import functools as ft
from threading import local
from functools import partial

from twoq import compat as ct
from twoq import support as ut
from twoq.support import pick as xpick, pluck as xpluck

__all__ = ['coreq']
isum = sum


class coreq(local):

    '''processing queue'''

    def __init__(self, incoming, outgoing):
        '''init'''
        super(coreq, self).__init__()
        self._call = None
        self._args = ()
        self._kw = {}
        self.incoming = incoming
        self.outgoing = outgoing

    def __iter__(self):
        # outgoing things iterator
        return iter(self.outgoing)

    ###########################################################################
    ## queue management #######################################################
    ###########################################################################

    def tap(self, call):
        '''
        add call

        @param call: a call
        '''
        self._args = ()
        self._kw = {}
        self._call = call
        return self

    def args(self, *args, **kw):
        '''pass arguments to current callable in call it.chain'''
        self._args = args
        self._kw = kw
        return self

    def detap(self):
        '''clear call'''
        self._args = ()
        self._kw = {}
        self._call = None
        return self

    def wrap(self, call):
        '''build factory callable and make call'''
        def factory(*args, **kw):
            return call(*args, **kw)
        self._call = factory
        return self

    # alias
    clear = unwrap = detap

    ###########################################################################
    ## duplication ############################################################
    ###########################################################################

    def copy(self, _map=ct.map, _copy=cp.copy):
        '''copy each incoming thing'''
        with self._sync as sync:
            sync(_map(_copy, sync.iterable))
        return self

    def deepcopy(self, _map=ct.map, _deepcopy=cp.deepcopy):
        '''copy each incoming thing deeply'''
        with self._sync as sync:
            sync(_map(_deepcopy, sync.iterable))
        return self

    ###########################################################################
    ## filter #################################################################
    ###########################################################################

    def compact(self, _filter=ct.filter, _truth=op.truth):
        '''strip "untrue" things from incoming things'''
        with self._sync as sync:
            sync.iter(_filter(_truth, sync.iterable))
        return self

    def filter(self, _filter=ct.filter):
        '''incoming things for which call is `True`'''
        with self._sync as sync:
            sync(_filter(self._call, sync.iterable))
        return self

    def find(self, _find=ut.find):
        '''first incoming thing for which call is `True`'''
        with self._sync as sync:
            sync(_find(self._call, self.incoming))
        return self

    def partition(self, _t=it.tee, _ff=ct.filterfalse, _filter=ct.filter):
        '''
        split incoming things into `True` and `False` things based on results
        of callable

        @param test: a test
        '''
        with self._sync as sync:
            call = self._call
            falsy, truey = _t(sync.iterable)
            sync.append(list(_ff(call, falsy)))
            sync.append(list(_filter(call, truey)))
        return self

    def reject(self, _filterfalse=ct.filterfalse):
        '''incoming things for which call is `False`'''
        with self._sync as sync:
            sync(_filterfalse(self._call, sync.iterable))
        return self

    def without(self, *things):
        '''strip things from incoming things'''
        with self._sync as sync:
            sync(ct.filterfalse(lambda x: x in things, sync.iterable))
        return self

    ###########################################################################
    ## execution ##############################################################
    ###########################################################################

    def each(self, _map=it.starmap):
        '''invoke call with passed arguments, keywords in incoming things'''
        with self._sync as sync:
            sync(_map(lambda x, y: self._call(*x, **y), sync.iterable))
        return self

    def invoke(self, name, _methodcaller=op.methodcaller, _map=ct.map):
        '''
        invoke call on each incoming thing with passed arguments, keywords
        but return incoming thing instead if call returns None

        @param name: name of method
        '''
        _caller = op.methodcaller(name, *self._args, **self._kw)
        def _call(thing, _caller=_caller): #@IgnorePep8
            results = _caller(thing)
            return thing if results is None else results
        with self._sync as sync:
            sync(_map(_call, sync.iterable))
        return self

    def map(self, _map=ct.map):
        '''invoke call on each incoming thing'''
        with self._sync as sync:
            sync(_map(self._call, sync.iterable))
        return self

    ###########################################################################
    ## delayed execution ######################################################
    ###########################################################################

    def delay_each(self, wait, _sleep=time.sleep, _map=it.starmap):
        '''
        invoke call with passed arguments, keywords in incoming things after a
        delay

        @param wait: time in seconds
        '''
        def _delay(x, y, _wait=wait, _call=self._call, _sleep=_sleep):
            _sleep(_wait)
            return _call(*x, **y)
        with self._sync as sync:
            sync(_map(_delay, sync.iterable))
        return self

    def delay_invoke(self, name, wait, _sleep=time.sleep, _map=ct.map):
        '''
        invoke call on each incoming thing with passed arguments, keywords
        after a delay but return incoming thing instead if call returns None

        @param name: name of method
        @param wait: time in seconds
        '''
        _caller = op.methodcaller(name, *self._args, **self._kw)
        def _call(x, _caller=_caller, _sleep=_sleep): #@IgnorePep8
            _sleep(wait)
            results = _caller(x)
            return x if results is None else results
        with self._sync as sync:
            sync(_map(_call, sync.iterable))
        return self

    def delay_map(self, wait, _sleep=time.sleep, _map=ct.map):
        '''
        invoke call on each incoming thing after a delay

        @param wait: time in seconds
        '''
        def _delay(x, _wait=wait, _call=self._call, _sleep=_sleep):
            _sleep(_wait)
            return _call(x)
        with self._sync as sync:
            sync(_map(_delay, sync.iterable))
        return self

    ###########################################################################
    ## reduce #################################################################
    ###########################################################################

    def flatten(self, _chain=it.chain.from_iterable):
        '''flatten nested incoming things'''
        with self._sync as sync:
            sync(_chain(sync.iterable))
        return self

    def merge(self, _merge=hq.merge):
        '''flatten nested and ordered incoming things'''
        with self._sync as sync:
            sync(_merge(*sync.iterable))
        return self

    def smash(self, _smash=ut.smash):
        '''flatten deeply nested incoming things'''
        with self._sync as sync:
            sync(_smash(sync.iterable))
        return self

    def pairwise(self, _tee=it.tee, _next=next, _zip=ct.zip):
        '''
        every two incoming things as a tuple

        s -> (s0,s1), (s1,s2), (s2, s3), ...
        '''
        with self._sync as sync:
            a, b = _tee(sync.iterable)
            _next(b, None)
            sync(_zip(a, b))
        return self

    def reduce(self, initial=None, _reduce=ft.reduce):
        '''
        reduce incoming things to one thing using call

        @param initial: initial thing (default: None)
        '''
        with self._sync as sync:
            if initial:
                sync.append(_reduce(self._call, sync.iterable, initial))
            else:
                sync.append(_reduce(self._call, sync.iterable))
        return self

    def reduce_right(self, initial=None, _reduce=ft.reduce):
        '''
        reduce incoming things to one thing from right side using call

        @param initial: initial thing (default: None)
        '''
        with self._sync as sync:
            if initial:
                sync(_reduce(
                    lambda x, y: self._call(y, x), sync.iterable, initial,
                ))
            else:
                sync(_reduce(lambda x, y: self._call(y, x), sync.iterable))
        return self

    def roundrobin(self, _roundrobin=ut.roundrobin):
        '''
        interleave incoming things into one thing e.g.

        roundrobin('ABC', 'D', 'EF') --> A D E B F C
        '''
        with self._sync as sync:
            sync(_roundrobin(sync.iterable))
        return self

    def zip(self, _zip=ct.zip):
        '''
        smash incoming things into single thing, pairing things by iterable
        position
        '''
        with self._sync as sync:
            sync(_zip(*sync.iterable))
        return self

    ###########################################################################
    ## math reduction #########################################################
    ###########################################################################

    def average(self, _sum=isum, _truediv=op.truediv, _len=len):
        '''average of all incoming things'''
        with self._sync as sync:
            iterable = sync.iterable
            sync.append(_truediv(_sum(iterable, 0.0), _len(iterable)))
        return self

    def fsum(self, _fsum=mt.fsum):
        '''
        add incoming things together

        @param start: starting number (default: 0)
        '''
        with self._sync as sync:
            sync.append(_fsum(sync.iterable))
        return self

    def max(self, _max=max):
        '''
        find maximum value in incoming things using call for key function
        '''
        with self._sync as sync:
            if self._call is None:
                sync.append(_max(sync.iterable))
            else:
                sync.append(_max(sync.iterable, key=self._call))
        return self

    def min(self, _min=min):
        '''
        find minimum value in incoming things using call for key function
        '''
        with self._sync as sync:
            if self._call is None:
                sync.append(_min(sync.iterable))
            else:
                sync.append(_min(sync.iterable, key=self._call))
        return self

    def sum(self, start=0, _sum=sum):
        '''
        add incoming things together

        @param start: starting number (default: 0)
        '''
        with self._sync as sync:
            sync.append(_sum(sync.iterable, start))
        return self

    ###########################################################################
    ## order ##################################################################
    ###########################################################################

    def group(self, _map=ct.map, _groupby=it.groupby):
        '''group incoming things using _call for key function'''
        with self._sync as sync:
            if self._call is None:
                sync(_map(
                    lambda x: [x[0], list(x[1])], _groupby(sync.iterable)
                ))
            else:
                sync(_map(
                    lambda x: [x[0], list(x[1])],
                    _groupby(sync.iterable, self._call),
                ))
        return self

    def grouper(self, n, fill=None, _zipl=ct.zip_longest, _iter=iter):
        '''
        split incoming things into sequences of length `n`, using fill thing to
        pad out incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)

        grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
        '''
        with self._sync as sync:
            sync(_zipl(fillvalue=fill, *[_iter(sync.iterable)] * n))
        return self

    def reverse(self, _reversed=reversed):
        '''reverse incoming things'''
        with self._sync as sync:
            sync(_reversed(sync.iterable))
        return self

    def sort(self, _sorted=sorted):
        '''sort incoming things using call for key function'''
        with self._sync as sync:
            if self._call is None:
                sync(_sorted(sync.iterable))
            else:
                sync(_sorted(sync.iterable, key=self._call))
        return self

    ###########################################################################
    ## random #################################################################
    ###########################################################################

    def choice(self, _choice=rm.choice):
        '''random choice from incoming things'''
        with self._sync as sync:
            sync.append(_choice(sync.iterable))
        return self

    def sample(self, n, _sample=rm.sample, _list=list):
        '''
        random sampling drawn from `n` incoming things

        @param n: number of things
        '''
        with self._sync as sync:
            sync(_sample(_list(sync.iterable), n))
        return self

    def shuffle(self, _shuffle=rm.shuffle):
        '''shuffle incoming things'''
        with self._sync as sync:
            iterable = sync.iterable
            _shuffle(iterable)
            sync(iterable)
        return self

    ##########################################################################
    ## large slice ###########################################################
    ##########################################################################

    def nth(self, n, default=None, _next=next, _islice=it.islice):
        '''
        nth incoming thing or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        with self._sync as sync:
            sync.append(_next(_islice(sync.iterable, n, None), default))
        return self

    def initial(self, _islice=it.islice, _len=len):
        '''all incoming things except the last thing'''
        with self._sync as sync:
            iterable = sync.iterable
            sync(_islice(iterable, _len(iterable) - 1))
        return self

    def rest(self, _islice=it.islice):
        '''all incoming things except the first thing'''
        with self._sync as sync:
            sync(_islice(sync.iterable, 1, None))
        return self

    def snatch(self, n, _islice=it.islice, _len=len):
        '''
        last `n` things of incoming things

        @param n: number of things
        '''
        with self._sync as sync:
            iterable = sync.iterable
            sync(_islice(iterable, _len(iterable) - n, None))
        return self

    def take(self, n, _islice=it.islice):
        '''
        first `n` things of incoming things

        @param n: number of things
        '''
        with self._sync as sync:
            sync(_islice(sync.iterable, n))
        return self

    ###########################################################################
    ## collection #############################################################
    ###########################################################################

    def members(self, _mz=ut.members, _map=ct.map, _ci=it.chain.from_iterable):
        '''collect members of incoming things'''
        _members = partial(_mz, call=self._call)
        with self._sync as sync:
            sync(_ci(_map(_members, sync.iterable)))
        return self

    def pick(self, *names):
        '''attributes of incoming things by attribute `*names`'''
        with self._sync as sync:
            sync(xpick(names, sync.iterable))
        return self

    def pluck(self, *keys):
        '''items of incoming things by item `*keys`'''
        with self._sync as sync:
            sync(xpluck(keys, sync.iterable))
        return self

    ###########################################################################
    ## repetition #############################################################
    ###########################################################################

    def padnone(self, _chain=it.chain, _repeat=it.repeat):
        '''
        incoming things and then `None` indefinitely

        (Useful for emulating the behavior of 2.x classic `builtin` `map`)
        '''
        with self._sync as sync:
            sync.iter(_chain(sync.iterable, _repeat(None)))
        return self

    def range(self, start, stop=0, step=1, _range=ct.xrange):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        with self._sync as sync:
            if stop:
                sync(_range(start, stop, step))
            else:
                sync(_range(start))
        return self

    def repeat(self, n, _repeat=it.repeat, _tuple=tuple):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        with self._sync as sync:
            sync(_repeat(_tuple(sync.iterable), n))
        return self

    def times(self, n=None, _starmap=it.starmap, _repeat=it.repeat):
        '''
        repeat call with passed arguments

        @param n: number of times to repeat calls (default: None)
        '''
        with self._sync as sync:
            if n is None:
                sync(_starmap(self._call, _repeat(sync.iterable)))
            else:
                sync(_starmap(self._call, _repeat(sync.iterable, n)))
        return self

    ###########################################################################
    ## truth ##################################################################
    ###########################################################################

    def all(self, _all=all, _map=ct.map):
        '''if `all` incoming things are `True`'''
        with self._sync as sync:
            sync.append(_all(_map(self._call, sync.iterable)))
        return self

    def any(self, _any=any, _map=ct.map):
        '''if `any` incoming things are `True`'''
        with self._sync as sync:
            sync.append(_any(_map(self._call, sync.iterable)))
        return self

    def contains(self, thing, _contains=op.contains):
        '''
        if `thing` is in incoming things

        @param thing: some thing
        '''
        with self._sync as sync:
            sync.append(_contains(sync.iterable, thing))
        return self

    def quantify(self, _sum=isum, _map=ct.map):
        '''how many times call is True for incoming things'''
        with self._sync as sync:
            sync.append(_sum(_map(self._call, sync.iterable)))
        return self

    ###########################################################################
    ## unique slice ###########################################################
    ###########################################################################

    def difference(self, _reduce=ft.reduce, _set=set):
        '''difference between incoming things'''
        with self._sync as sync:
            sync(_reduce(
                lambda x, y: _set(x).difference(_set(y)), sync.iterable,
            ))
        return self

    def intersection(self, _reduce=ft.reduce, _set=set):
        '''intersection between incoming things'''
        with self._sync as sync:
            sync(_reduce(
                lambda x, y: _set(x).intersection(_set(y)), sync.iterable,
            ))
        return self

    def union(self, _reduce=ft.reduce, _set=set):
        '''union between incoming things'''
        with self._sync as sync:
            sync(_reduce(
                lambda x, y: _set(x).union(_set(y)), sync.iterable,
            ))
        return self

    def unique(self, _unique=ut.unique):
        '''
        list unique incoming things, preserving order and remember all incoming
        things ever seen

        unique_everseen('AAAABBBCCDAABBB') --> A B C D
        unique_everseen('ABBCcAD', str.lower) --> A B C D
        '''
        with self._sync as sync:
            sync.iter(_unique(sync.iterable, self._call))
        return self
