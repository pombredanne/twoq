# -*- coding: utf-8 -*-
'''twoq core'''

from threading import local
from collections import Iterable

from random import shuffle as ishuffle, sample as isample, choice as ichoice
from functools import reduce as ireduce, partial
from itertools import (
    groupby, islice, repeat, starmap, cycle, tee, chain)
from operator import (
    itemgetter as iget, attrgetter, methodcaller, contains as icontains)

from twoq.compat import (
    port, filter as ifilter, filterfalse, map as imap, zip_longest,
    zip as izip,
)

__all__ = ['coreq']


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

    def value(self, _list=list, _len=len):
        '''return outgoing things and clear'''
        if _len(self.outgoing) == 1:
            return self.outgoing.pop()
        results = _list(self.outgoing)
        self.clear()
        return results

    def reup(self, _list=list):
        '''put incoming things in incoming things as one incoming thing'''
        with self._sync as _sync:
            _sync.append(_list(self.incoming))
        return self

    ##########################################################################
    ## filter ################################################################
    ##########################################################################

    def filter(self, _filter=ifilter):
        '''incoming things for which call is `True`'''
        with self._sync as _sync:
            _sync(_filter(self._call, self.incoming))
        return self

    def find(self, _filter=ifilter):
        '''first incoming thing for which call is `True`'''
        def _find(call, incoming, _filter=_filter):
            for thing in _filter(call, incoming):
                yield thing
                break
        with self._sync as _sync:
            _sync(_find(self._call, self.incoming))
        return self

    def reject(self, _filterfalse=filterfalse):
        '''incoming things for which call is `False`'''
        with self._sync as _sync:
            _sync(_filterfalse(self._call, self.incoming))
        return self

    ##########################################################################
    ## map ###################################################################
    ##########################################################################

    def each(self, _map=imap):
        '''
        invoke call with passed arguments, keywords in incoming things
        '''
        with self._sync as _sync:
            _sync(_map(lambda x: self._call(*x[0], **x[1]), self.incoming))
        return self

    def invoke(self, name, _methodcaller=methodcaller, _map=imap):
        '''
        invoke call on each incoming thing with passed arguments, keywords
        but return incoming thing instead if call returns None
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
    ## reduce ################################################################
    ##########################################################################

    def flatten(self, _chain=chain.from_iterable):
        '''flatten nested incoming things'''
        with self._sync as _sync:
            _sync(_chain(self.incoming))
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

    def smash(self, _isstring=port.isstring, _Iterable=Iterable):
        '''flatten deeply nested incoming things'''
        def _smash(iterable, _isstring=_isstring, _Iterable=_Iterable):
            for i in iterable:
                if isinstance(i, _Iterable) and not _isstring(i):
                    for j in _smash(i):
                        yield j
                else:
                    yield i
        with self._sync as _sync:
            _sync(_smash(self.incoming))
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

    def roundrobin(self, _s=islice, _c=cycle, _p=partial, _i=iter, _n=next):
        '''
        interleave incoming things into one thing e.g.

        roundrobin('ABC', 'D', 'EF') --> A D E B F C
        '''
        # Recipe credited to George Sakkis
        def _roundrobin(iterable, _s=_s, _c=_c, _p=_p, _i=_i, _n=_n):
            pending = len(iterable)
            nexts = _c(_p(_n, _i(i)) for i in iterable)
            while pending:
                try:
                    for n in nexts:
                        yield n()
                except StopIteration:
                    pending -= 1
                    nexts = _c(_s(nexts, pending))
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

    def reverse(self):
        '''iterate over reversed incoming things, clearing as it goes'''
        self.outgoing.extendleft(self.incoming)
        self._inclear()
        self._inextend(self.outgoing)
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

    def take(self, n, _islice=islice):
        '''
        first `n` things of incoming things

        @param n: number of things
        '''
        with self._sync as _sync:
            _sync(_islice(self.incoming, n))
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

    ##########################################################################
    ## collection ############################################################
    ##########################################################################

    def members(self, _filter=ifilter, _map=imap, _chain=chain.from_iterable):
        '''collect members of incoming things'''
        def _members(this, _filter=_filter, _get=getattr):
            for key in _filter(self._call, dir(this)):
                try:
                    thing = _get(this, key)
                except AttributeError:
                    pass
                else:
                    yield key, thing
        with self._sync as _sync:
            _sync.iter(_chain(_map(_members, self.incoming)))
        return self

    def pick(self, *names):
        '''attributes of incoming things by attribute `*names`'''
        def _pick(names, iterable):
            find = attrgetter(*names)
            for thing in iterable:
                try:
                    yield find(thing)
                except AttributeError:
                    pass
        with self._sync as _sync:
            _sync(_pick(names, self.incoming))
        return self

    def pluck(self, *keys):
        '''items of incoming things by item `*keys`'''
        def _pluck(keys, iterable):
            find = iget(*keys)
            for thing in iterable:
                try:
                    yield find(thing)
                except (IndexError, KeyError, TypeError):
                    pass
        with self._sync as _sync:
            _sync(_pluck(keys, self.incoming))
        return self

    ##########################################################################
    ## repetition ############################################################
    ##########################################################################

    def ncycles(self, n, _repeat=repeat, _tuple=tuple):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        with self._sync as _sync:
            _sync(_repeat(_tuple(self.incoming), n))
        return self

    def padnone(self, _chain=chain, _repeat=repeat):
        '''
        incoming things and then `None` indefinitely

        (Useful for emulating the behavior of 2.x classic `builtin` `map`)
        '''
        with self._sync as _sync:
            _sync.iter(_chain(self.incoming, _repeat(None)))
        return self

    def times(self, n=None, _starmap=starmap, _repeat=repeat):
        '''
        repeat call with passed arguments

        @param n: number of times to repeat calls (default: None)
        '''
        with self._sync as _sync:
            if n is None:
                _sync(_starmap(self._call, _repeat(self.incoming)))
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

    def quantify(self, _sum=sum, _map=imap):
        '''how many times call is True for incoming things'''
        with self._sync as _sync:
            _sync.append(_sum(_map(self._call, self.incoming)))
        return self

    ##########################################################################
    ## strip #################################################################
    ##########################################################################

    def compact(self, _filter=ifilter, _bool=bool):
        '''strip "untrue" things from incoming things'''
        with self._sync as _sync:
            _sync.iter(_filter(_bool, self.incoming))
        return self

    def without(self, *things):
        '''strip things from incoming things'''
        with self._sync as _sync:
            _sync(filterfalse(lambda x: x in things, self.incoming))
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

    def unique(self, _ff=filterfalse, _set=set):
        '''
        list unique incoming things, preserving order and remember all incoming
        things ever seen

        unique_everseen('AAAABBBCCDAABBB') --> A B C D
        unique_everseen('ABBCcAD', str.lower) --> A B C D
        '''
        def _unique_everseen(iterable, key=None, _ff=_ff, _set=_set):
            seen = _set()
            seen_add = seen.add
            if key is None:
                for element in _ff(seen.__contains__, iterable):
                    seen_add(element)
                    yield element
            else:
                for element in iterable:
                    k = key(element)
                    if k not in seen:
                        seen_add(k)
                        yield element
        with self._sync as _sync:
            _sync.iter(_unique_everseen(self.incoming, self._call))
        return self
