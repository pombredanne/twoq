# -*- coding: utf-8 -*-
'''twoq core'''

from threading import local
from collections import Iterable
from functools import reduce, partial
from random import shuffle, sample, choice
from itertools import (
    groupby, islice, repeat, starmap, cycle, tee, chain)
from operator import itemgetter as iget, attrgetter, methodcaller, contains

from twoq.compat import port, filter, filterfalse, map, zip_longest

__all__ = ['coreq']


class coreq(local):

    '''processing queue'''

    def __init__(self, incoming, outgoing):
        '''init'''
        super(coreq, self).__init__()
        self.call = None
        self.incoming = incoming
        self.outgoing = outgoing

    def __iter__(self):
        # outgoing things iterator
        return iter(self.outgoing)

    ##########################################################################
    ## queue management & execution ##########################################
    ##########################################################################

    def tap(self, call):
        '''
        add call

        @param call: a call
        '''
        self.call = call
        return self

    def detap(self):
        '''clear call'''
        self.call = None
        return self

    def wrap(self, call):
        '''build factory callable and make call'''
        def factory(*args, **kw):
            return call(*args, **kw)
        self.call = factory
        return self

    # alias
    clear = unwrap = detap

    def swap(self):
        '''swap queues'''
        incoming = self.incoming
        self.incoming = self.outgoing
        self.outgoing = incoming
        return self

    def value(self):
        '''return outgoing things and clear'''
        if len(self.outgoing) == 1:
            return self.outgoing.pop()
        results = list(self.outgoing)
        self.clear()
        return results

    def reup(self):
        '''put incoming things in incoming things as one incoming thing'''
        with self._sync as _sync:
            _sync.append(list(self.incoming))
        return self

    ##########################################################################
    ## filter ################################################################
    ##########################################################################

    def filter(self):
        '''incoming things for which call is `True`'''
        with self._sync as _sync:
            _sync(filter(self.call, self.incoming))
        return self

    def find(self):
        '''first incoming thing for which call is `True`'''
        def _find(call, incoming):
            for thing in filter(call, incoming):
                yield thing
                break
        with self._sync as _sync:
            _sync(_find(self.call, self.incoming))
        return self

    def reject(self):
        '''incoming things for which call is `False`'''
        with self._sync as _sync:
            _sync(filterfalse(self.call, self.incoming))
        return self

    ##########################################################################
    ## map ###################################################################
    ##########################################################################

    def each(self):
        '''
        invoke call with passed arguments, keywords in incoming things
        '''
        with self._sync as _sync:
            _sync(map(lambda x: self.call(*x[0], **x[1]), self.incoming))
        return self

    def invoke(self, name, *args, **kw):
        '''
        invoke call on each incoming thing with passed arguments, keywords
        but return incoming thing instead if call returns None
        '''
        caller = methodcaller(name, *args, **kw)
        def call(thing): #@IgnorePep8
            results = caller(thing)
            return thing if results is None else results
        with self._sync as _sync:
            _sync(map(call, self.incoming))
        return self

    def map(self):
        '''invoke call on each incoming thing'''
        with self._sync as _sync:
            _sync(map(self.call, self.incoming))
        return self

    ##########################################################################
    ## reduce ################################################################
    ##########################################################################

    def flatten(self):
        '''flatten nested incoming things'''
        with self._sync as _sync:
            _sync(chain.from_iterable(self.incoming))
        return self

    def max(self):
        '''
        find maximum value in incoming things using call for key function
        '''
        with self._sync as _sync:
            if self.call is None:
                _sync.append(max(self.incoming))
            else:
                _sync.append(max(self.incoming, key=self.call))
        return self

    def smash(self):
        '''flatten deeply nested incoming things'''
        def _smash(iterable):
            isstring = port.isstring
            for i in iterable:
                if isinstance(i, Iterable) and not isstring(i):
                    for j in _smash(i):
                        yield j
                else:
                    yield i
        with self._sync as _sync:
            _sync(_smash(self.incoming))
        return self

    def min(self):
        '''
        find minimum value in incoming things using call for key function
        '''
        with self._sync as _sync:
            if self.call is None:
                _sync.append(min(self.incoming))
            else:
                _sync.append(min(self.incoming, key=self.call))
        return self

    def pairwise(self):
        '''
        every two incoming things as a tuple

        s -> (s0,s1), (s1,s2), (s2, s3), ...
        '''
        a, b = tee(self.incoming)
        next(b, None)
        with self._sync as _sync:
            _sync(zip(a, b))
        return self

    def reduce(self, initial=None):
        '''
        reduce incoming things to one thing using call

        @param initial: initial thing (default: None)
        '''
        with self._sync as _sync:
            if initial:
                _sync.append(reduce(self.call, self.incoming, initial))
            else:
                _sync.append(reduce(self.call, self.incoming))
        return self

    def reduce_right(self, initial=None):
        '''
        reduce incoming things to one thing from right side using call

        @param initial: initial thing (default: None)
        '''
        with self._sync as _sync:
            func = lambda x, y: self.call(y, x)
            if initial:
                _sync(reduce(func, self.incoming, initial))
            else:
                _sync(reduce(func, self.incoming))
        return self

    def roundrobin(self):
        '''
        interleave incoming things into one thing e.g.

        roundrobin('ABC', 'D', 'EF') --> A D E B F C
        '''
        # Recipe credited to George Sakkis
        def _roundrobin(iterable):
            pending = len(iterable)
            nexts = cycle(partial(next, iter(it)) for it in iterable)
            while pending:
                try:
                    for nxt in nexts:
                        yield nxt()
                except StopIteration:
                    pending -= 1
                    nexts = cycle(islice(nexts, pending))
        with self._sync as _sync:
            _sync(_roundrobin(self.incoming))
        return self

    def zip(self):
        '''
        smash incoming things into single thing, pairing things by iterable
        position
        '''
        with self._sync as _sync:
            _sync(zip(*self.incoming))
        return self

    ##########################################################################
    ## order #################################################################
    ##########################################################################

    def group(self):
        '''group incoming things using call for key function'''
        with self._sync as _sync:
            if self.call is None:
                _sync(map(
                    lambda x: [x[0], list(x[1])], groupby(self.incoming)
                ))
            else:
                _sync(map(
                    lambda x: [x[0], list(x[1])],
                    groupby(self.incoming, self.call),
                ))
        return self

    def grouper(self, n, fill=None):
        '''
        split incoming things into sequences of length `n`, using fill thing to
        pad out incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)

        grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
        '''
        with self._sync as _sync:
            _sync(zip_longest(fillvalue=fill, *[iter(self.incoming)] * n))
        return self

    def reverse(self):
        '''iterate over reversed incoming things, clearing as it goes'''
        self.outgoing.extendleft(self.incoming)
        self._inclear()
        self._inextend(self.outgoing)
        return self

    def sort(self):
        '''sort incoming things using call for key function'''
        with self._sync as _sync:
            if self.call is None:
                _sync(sorted(self.incoming))
            else:
                _sync(sorted(self.incoming, key=self.call))
        return self

    ##########################################################################
    ## random ################################################################
    ##########################################################################

    def choice(self):
        '''random choice from incoming things'''
        with self._sync as _sync:
            _sync.append(choice(self.incoming))
        return self

    def sample(self, n):
        '''
        random sampling drawn from `n` incoming things

        @param n: number of things
        '''
        with self._sync as _sync:
            _sync(sample(list(self.incoming), n))
        return self

    def shuffle(self):
        '''shuffle incoming things'''
        incoming = self.incoming
        with self._sync as _sync:
            shuffle(incoming)
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

    def nth(self, n, default=None):
        '''
        nth incoming thing or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        with self._sync as _sync:
            _sync.append(next(islice(self.incoming, n, None), default))
        return self

    def last(self):
        '''last thing among incoming things'''
        with self._sync as _sync:
            _sync.append(self.incoming.pop())
        return self

    ##########################################################################
    ## large slice ###########################################################
    ##########################################################################

    def initial(self):
        '''all incoming things except the last thing'''
        incoming = self.incoming
        with self._sync as _sync:
            _sync(islice(incoming, len(incoming) - 1))
        return self

    def rest(self):
        '''all incoming things except the first thing'''
        with self._sync as _sync:
            _sync(islice(self.incoming, 1, None))
        return self

    def take(self, n):
        '''
        first `n` things of incoming things

        @param n: number of things
        '''
        with self._sync as _sync:
            _sync(islice(self.incoming, n))
        return self

    def snatch(self, n):
        '''
        last `n` things of incoming things

        @param n: number of things
        '''
        incoming = self.incoming
        with self._sync as _sync:
            _sync(islice(incoming, len(incoming) - n, None))
        return self

    ##########################################################################
    ## collection ############################################################
    ##########################################################################

    def members(self):
        '''collect members of incoming things'''
        def _members(this):
            for key in filter(self.call, dir(this)):
                try:
                    thing = getattr(this, key)
                except AttributeError:
                    pass
                else:
                    yield key, thing
        with self._sync as _sync:
            _sync.iter(chain.from_iterable(map(_members, self.incoming)))
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

    def ncycles(self, n):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        with self._sync as _sync:
            _sync(repeat(tuple(self.incoming), n))
        return self

    def padnone(self):
        '''
        incoming things and then `None` indefinitely

        (Useful for emulating the behavior of 2.x classic `builtin` `map`)
        '''
        with self._sync as _sync:
            _sync.iter(chain(self.incoming, repeat(None)))
        return self

    def times(self, n=None):
        '''
        repeat call with passed arguments

        @param n: number of times to repeat calls (default: None)
        '''
        with self._sync as _sync:
            if n is None:
                _sync(starmap(self.call, repeat(self.incoming)))
            _sync(starmap(self.call, repeat(self.incoming, n)))
        return self

    ##########################################################################
    ## truth #################################################################
    ##########################################################################

    def all(self):
        '''if `all` incoming things are `True`'''
        with self._sync as _sync:
            _sync.append(all(map(self.call, self.incoming)))
        return self

    def any(self):
        '''if `any` incoming things are `True`'''
        with self._sync as _sync:
            _sync.append(any(map(self.call, self.incoming)))
        return self

    def contains(self, thing):
        '''
        if `thing` is in incoming things

        @param thing: some thing
        '''
        with self._sync as _sync:
            _sync.append(contains(self.incoming, thing))
        return self

    def quantify(self):
        '''how many times call is True for incoming things'''
        with self._sync as _sync:
            _sync.append(sum(map(self.call, self.incoming)))
        return self

    ##########################################################################
    ## strip #################################################################
    ##########################################################################

    def compact(self):
        '''strip "untrue" things from incoming things'''
        with self._sync as _sync:
            _sync.iter(filter(bool, self.incoming))
        return self

    def without(self, *things):
        '''strip things from incoming things'''
        with self._sync as _sync:
            _sync(filterfalse(lambda x: x in things, self.incoming))
        return self

    ##########################################################################
    ## unique slice ##########################################################
    ##########################################################################

    def difference(self):
        '''difference between incoming things'''
        with self._sync as _sync:
            _sync(reduce(
                lambda x, y: set(x).difference(set(y)), self.incoming,
            ))
        return self

    def intersection(self):
        '''intersection between incoming things'''
        with self._sync as _sync:
            _sync(reduce(
                lambda x, y: set(x).intersection(set(y)), self.incoming,
            ))
        return self

    def union(self):
        '''union between incoming things'''
        with self._sync as _sync:
            _sync(reduce(
                lambda x, y: set(x).union(set(y)), self.incoming,
            ))
        return self

    def unique(self):
        '''
        list unique incoming things, preserving order and remember all incoming
        things ever seen

        unique_everseen('AAAABBBCCDAABBB') --> A B C D
        unique_everseen('ABBCcAD', str.lower) --> A B C D
        '''
        def _unique_everseen(iterable, key=None):
            seen = set()
            seen_add = seen.add
            if key is None:
                for element in filterfalse(seen.__contains__, iterable):
                    seen_add(element)
                    yield element
            else:
                for element in iterable:
                    k = key(element)
                    if k not in seen:
                        seen_add(k)
                        yield element
        with self._sync as _sync:
            _sync.iter(_unique_everseen(self.incoming, self.call))
        return self
