# -*- coding: utf-8 -*-
'''twoq core'''

import time
from threading import local
from functools import partial
from math import fsum as ifsum

from heapq import merge as imerge
from functools import reduce as ireduce
from itertools import (
    groupby, islice, repeat as irepeat, starmap, tee, chain)
from operator import methodcaller, contains as icontains, truth, truediv
from random import shuffle as ishuffle, sample as isample, choice as ichoice

from twoq.utils import (
    find as xfind, smash as xsmash, roundrobin as xroundrobin,
    members as xmembers, pick as xpick, pluck as xpluck, unique as xunique)
from twoq.compat import (
    filter as ifilter, filterfalse, map as imap, zip_longest, zip as izip,
    xrange as irange,
)

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

    ##########################################################################
    ## queue management ######################################################
    ##########################################################################

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
        '''pass arguments to current callable in call chain'''
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

    def swap(self):
        '''swap queues'''
        incoming = self.incoming
        self.incoming = self.outgoing
        self.outgoing = incoming
        return self

    ##########################################################################
    ## filter ################################################################
    ##########################################################################

    def compact(self, _filter=ifilter, _truth=truth):
        '''strip "untrue" things from incoming things'''
        with self._sync as _sync:
            _sync.iter(_filter(_truth, self.incoming))
        return self

    def filter(self, _filter=ifilter):
        '''incoming things for which call is `True`'''
        with self._sync as _sync:
            _sync(_filter(self._call, self.incoming))
        return self

    def find(self, _find=xfind):
        '''first incoming thing for which call is `True`'''
        with self._sync as _sync:
            _sync(_find(self._call, self.incoming))
        return self

    def partition(self, _tee=tee, _filterfalse=filterfalse, _filter=ifilter):
        '''
        split incoming things into `True` and `False` things based on results
        of callable

        @param test: a test
        '''
        with self._sync as _sync:
            call = self._call
            falsy, truey = _tee(self.incoming)
            _sync.append(list(_filterfalse(call, falsy)))
            _sync.append(list(_filter(call, truey)))
        return self

    def reject(self, _filterfalse=filterfalse):
        '''incoming things for which call is `False`'''
        with self._sync as _sync:
            _sync(_filterfalse(self._call, self.incoming))
        return self

    def without(self, *things):
        '''strip things from incoming things'''
        with self._sync as _sync:
            _sync(filterfalse(lambda x: x in things, self.incoming))
        return self

    ##########################################################################
    ## execution #############################################################
    ##########################################################################

    def each(self, _map=starmap):
        '''invoke call with passed arguments, keywords in incoming things'''
        with self._sync as _sync:
            _sync(_map(lambda x, y: self._call(*x, **y), self.incoming))
        return self

    def invoke(self, name, _methodcaller=methodcaller, _map=imap):
        '''
        invoke call on each incoming thing with passed arguments, keywords
        but return incoming thing instead if call returns None

        @param name: name of method
        '''
        _caller = methodcaller(name, *self._args, **self._kw)
        def _call(thing, _caller=_caller): #@IgnorePep8
            results = _caller(thing)
            return thing if results is None else results
        with self._sync as _sync:
            _sync(_map(_call, self.incoming))
        return self

    def map(self, _map=imap):
        '''invoke call on each incoming thing'''
        with self._sync as _sync:
            _sync(_map(self._call, self.incoming))
        return self

    ##########################################################################
    ## delayed execution #####################################################
    ##########################################################################

    def delay_each(self, wait, _sleep=time.sleep, _map=starmap):
        '''
        invoke call with passed arguments, keywords in incoming things after a
        delay

        @param wait: time in seconds
        '''
        def _delay(x, y, _wait=wait, _call=self._call, _sleep=_sleep):
            _sleep(_wait)
            return _call(*x, **y)
        with self._sync as _sync:
            _sync(_map(_delay, self.incoming))
        return self

    def delay_invoke(self, name, wait, _sleep=time.sleep, _map=imap):
        '''
        invoke call on each incoming thing with passed arguments, keywords
        after a delay but return incoming thing instead if call returns None

        @param name: name of method
        @param wait: time in seconds
        '''
        _caller = methodcaller(name, *self._args, **self._kw)
        def _call(x, _caller=_caller, _sleep=_sleep): #@IgnorePep8
            _sleep(wait)
            results = _caller(x)
            return x if results is None else results
        with self._sync as _sync:
            _sync(_map(_call, self.incoming))
        return self

    def delay_map(self, wait, _sleep=time.sleep, _map=imap):
        '''
        invoke call on each incoming thing after a delay

        @param wait: time in seconds
        '''
        def _delay(x, _wait=wait, _call=self._call, _sleep=_sleep):
            _sleep(_wait)
            return _call(x)
        with self._sync as _sync:
            _sync(_map(_delay, self.incoming))
        return self

    ##########################################################################
    ## reduce ################################################################
    ##########################################################################

    def flatten(self, _chain=chain.from_iterable):
        '''flatten nested incoming things'''
        with self._sync as _sync:
            _sync(_chain(self.incoming))
        return self

    def merge(self, _merge=imerge):
        '''flatten nested and ordered incoming things'''
        with self._sync as _sync:
            _sync(_merge(*self.incoming))
        return self

    def smash(self, _smash=xsmash):
        '''flatten deeply nested incoming things'''
        with self._sync as _sync:
            _sync(_smash(self.incoming))
        return self

    def pairwise(self, _tee=tee, _next=next, _zip=izip):
        '''
        every two incoming things as a tuple

        s -> (s0,s1), (s1,s2), (s2, s3), ...
        '''
        a, b = _tee(self.incoming)
        _next(b, None)
        with self._sync as _sync:
            _sync(_zip(a, b))
        return self

    def reduce(self, initial=None, _reduce=ireduce):
        '''
        reduce incoming things to one thing using call

        @param initial: initial thing (default: None)
        '''
        with self._sync as _sync:
            if initial:
                _sync.append(_reduce(self._call, self.incoming, initial))
            else:
                _sync.append(_reduce(self._call, self.incoming))
        return self

    def reduce_right(self, initial=None, _reduce=ireduce):
        '''
        reduce incoming things to one thing from right side using call

        @param initial: initial thing (default: None)
        '''
        with self._sync as _sync:
            if initial:
                _sync(_reduce(
                    lambda x, y: self._call(y, x), self.incoming, initial,
                ))
            else:
                _sync(_reduce(lambda x, y: self._call(y, x), self.incoming))
        return self

    def roundrobin(self, _roundrobin=xroundrobin):
        '''
        interleave incoming things into one thing e.g.

        roundrobin('ABC', 'D', 'EF') --> A D E B F C
        '''
        # Recipe credited to George Sakkis

        with self._sync as _sync:
            _sync(_roundrobin(self.incoming))
        return self

    def zip(self, _zip=izip):
        '''
        smash incoming things into single thing, pairing things by iterable
        position
        '''
        with self._sync as _sync:
            _sync(_zip(*self.incoming))
        return self

    ##########################################################################
    ## math reduction ########################################################
    ##########################################################################

    def average(self, _sum=isum, _truediv=truediv, _len=len):
        '''average of all incoming things'''
        with self._sync as _sync:
            incoming = self.incoming
            _sync.append(_truediv(_sum(incoming, 0.0), _len(incoming)))
        return self

    def fsum(self, _fsum=ifsum):
        '''
        add incoming things together

        @param start: starting number (default: 0)
        '''
        with self._sync as _sync:
            _sync.append(_fsum(self.incoming))
        return self

    def max(self, _max=max):
        '''
        find maximum value in incoming things using call for key function
        '''
        with self._sync as _sync:
            if self._call is None:
                _sync.append(_max(self.incoming))
            else:
                _sync.append(_max(self.incoming, key=self._call))
        return self

    def min(self, _min=min):
        '''
        find minimum value in incoming things using call for key function
        '''
        with self._sync as _sync:
            if self._call is None:
                _sync.append(_min(self.incoming))
            else:
                _sync.append(_min(self.incoming, key=self._call))
        return self

    def sum(self, start=0, _sum=sum):
        '''
        add incoming things together

        @param start: starting number (default: 0)
        '''
        with self._sync as _sync:
            _sync.append(_sum(self.incoming, start))
        return self

    ##########################################################################
    ## order #################################################################
    ##########################################################################

    def group(self, _map=imap, _groupby=groupby):
        '''group incoming things using _call for key function'''
        with self._sync as _sync:
            if self._call is None:
                _sync(_map(
                    lambda x: [x[0], list(x[1])], _groupby(self.incoming)
                ))
            else:
                _sync(_map(
                    lambda x: [x[0], list(x[1])],
                    _groupby(self.incoming, self._call),
                ))
        return self

    def grouper(self, n, fill=None, _zipl=zip_longest, _iter=iter):
        '''
        split incoming things into sequences of length `n`, using fill thing to
        pad out incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)

        grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
        '''
        with self._sync as _sync:
            _sync(_zipl(fillvalue=fill, *[_iter(self.incoming)] * n))
        return self

    def reverse(self, _reversed=reversed):
        '''reverse incoming things'''
        with self._sync as _sync:
            _sync(_reversed(self.incoming))
        return self

    def sort(self, _sorted=sorted):
        '''sort incoming things using call for key function'''
        with self._sync as _sync:
            if self._call is None:
                _sync(_sorted(self.incoming))
            else:
                _sync(_sorted(self.incoming, key=self._call))
        return self

    ##########################################################################
    ## random ################################################################
    ##########################################################################

    def choice(self, _choice=ichoice):
        '''random choice from incoming things'''
        with self._sync as _sync:
            _sync.append(_choice(self.incoming))
        return self

    def sample(self, n, _sample=isample, _list=list):
        '''
        random sampling drawn from `n` incoming things

        @param n: number of things
        '''
        with self._sync as _sync:
            _sync(_sample(_list(self.incoming), n))
        return self

    def shuffle(self, _shuffle=ishuffle):
        '''shuffle incoming things'''
        incoming = self.incoming
        with self._sync as _sync:
            _shuffle(incoming)
            _sync(incoming)
        return self

    ##########################################################################
    ## single slice ##########################################################
    ##########################################################################

    def first(self):
        '''first thing among incoming things'''
        with self._sync as _sync:
            _sync.append(self.incoming.popleft())
        return self

    def nth(self, n, default=None, _next=next, _islice=islice):
        '''
        nth incoming thing or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        with self._sync as _sync:
            _sync.append(_next(_islice(self.incoming, n, None), default))
        return self

    def last(self):
        '''last thing among incoming things'''
        with self._sync as _sync:
            _sync.append(self.incoming.pop())
        return self

    ##########################################################################
    ## large slice ###########################################################
    ##########################################################################

    def initial(self, _islice=islice, _len=len):
        '''all incoming things except the last thing'''
        incoming = self.incoming
        with self._sync as _sync:
            _sync(_islice(incoming, _len(incoming) - 1))
        return self

    def rest(self, _islice=islice):
        '''all incoming things except the first thing'''
        with self._sync as _sync:
            _sync(_islice(self.incoming, 1, None))
        return self

    def snatch(self, n, _islice=islice, _len=len):
        '''
        last `n` things of incoming things

        @param n: number of things
        '''
        incoming = self.incoming
        with self._sync as _sync:
            _sync(_islice(incoming, _len(incoming) - n, None))
        return self

    def take(self, n, _islice=islice):
        '''
        first `n` things of incoming things

        @param n: number of things
        '''
        with self._sync as _sync:
            _sync(_islice(self.incoming, n))
        return self

    ###########################################################################
    ## collection #############################################################
    ###########################################################################

    def members(self, _members=xmembers, _map=imap, _fitr=chain.from_iterable):
        '''collect members of incoming things'''
        _members = partial(_members, call=self._call)
        with self._sync as _sync:
            _sync.iter(_fitr(_map(_members, self.incoming)))
        return self

    def pick(self, *names):
        '''attributes of incoming things by attribute `*names`'''
        with self._sync as _sync:
            _sync(xpick(names, self.incoming))
        return self

    def pluck(self, *keys):
        '''items of incoming things by item `*keys`'''
        with self._sync as _sync:
            _sync(xpluck(keys, self.incoming))
        return self

    ##########################################################################
    ## repetition ############################################################
    ##########################################################################

    def padnone(self, _chain=chain, _repeat=irepeat):
        '''
        incoming things and then `None` indefinitely

        (Useful for emulating the behavior of 2.x classic `builtin` `map`)
        '''
        with self._sync as _sync:
            _sync.iter(_chain(self.incoming, _repeat(None)))
        return self

    def range(self, start, stop=0, step=1, _range=irange):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        with self._sync as _sync:
            if stop:
                _sync(_range(start, stop, step))
            else:
                _sync(_range(start))
        return self

    def repeat(self, n, _repeat=irepeat, _tuple=tuple):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        with self._sync as _sync:
            _sync(_repeat(_tuple(self.incoming), n))
        return self

    def times(self, n=None, _starmap=starmap, _repeat=irepeat):
        '''
        repeat call with passed arguments

        @param n: number of times to repeat calls (default: None)
        '''
        with self._sync as _sync:
            if n is None:
                _sync(_starmap(self._call, _repeat(self.incoming)))
            else:
                _sync(_starmap(self._call, _repeat(self.incoming, n)))
        return self

    ##########################################################################
    ## truth #################################################################
    ##########################################################################

    def all(self, _all=all, _map=imap):
        '''if `all` incoming things are `True`'''
        with self._sync as _sync:
            _sync.append(_all(_map(self._call, self.incoming)))
        return self

    def any(self, _any=any, _map=imap):
        '''if `any` incoming things are `True`'''
        with self._sync as _sync:
            _sync.append(_any(_map(self._call, self.incoming)))
        return self

    def contains(self, thing, _contains=icontains):
        '''
        if `thing` is in incoming things

        @param thing: some thing
        '''
        with self._sync as _sync:
            _sync.append(_contains(self.incoming, thing))
        return self

    def quantify(self, _sum=isum, _map=imap):
        '''how many times call is True for incoming things'''
        with self._sync as _sync:
            _sync.append(_sum(_map(self._call, self.incoming)))
        return self

    ##########################################################################
    ## unique slice ##########################################################
    ##########################################################################

    def difference(self, _reduce=ireduce, _set=set):
        '''difference between incoming things'''
        with self._sync as _sync:
            _sync(_reduce(
                lambda x, y: _set(x).difference(_set(y)), self.incoming,
            ))
        return self

    def intersection(self, _reduce=ireduce, _set=set):
        '''intersection between incoming things'''
        with self._sync as _sync:
            _sync(_reduce(
                lambda x, y: _set(x).intersection(_set(y)), self.incoming,
            ))
        return self

    def union(self, _reduce=ireduce, _set=set):
        '''union between incoming things'''
        with self._sync as _sync:
            _sync(_reduce(
                lambda x, y: _set(x).union(_set(y)), self.incoming,
            ))
        return self

    def unique(self, _unique=xunique):
        '''
        list unique incoming things, preserving order and remember all incoming
        things ever seen

        unique_everseen('AAAABBBCCDAABBB') --> A B C D
        unique_everseen('ABBCcAD', str.lower) --> A B C D
        '''
        with self._sync as _sync:
            _sync.iter(_unique(self.incoming, self._call))
        return self
