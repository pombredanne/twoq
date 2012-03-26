# -*- coding: utf-8 -*-
'''twoq reducing mixins'''

from math import fsum
from heapq import merge
from threading import local
from itertools import cycle
from collections import Iterable
from operator import truediv, contains

from twoq.support import Counter, isstring, zip, lazier

__all__ = ('MathMixin', 'TruthMixin', 'ReduceMixin', 'ReducingMixin')


class MathMixin(local):

    '''math mixin'''

    _counter = lazier(Counter)
    _fsum = lazier(fsum)
    _max = lazier(max)
    _min = lazier(min)
    _truediv = lazier(truediv)

    @classmethod
    def _average(cls, iterable):
        '''average of `iterable`'''
        i1, i2 = cls._split(iterable)
        return cls._truediv(cls._sum(i1, 0.0), cls._len(cls._list(i2)))

    @classmethod
    def _median(cls, iterable):
        '''median of `iterable`'''
        truediv_ = cls._truediv
        i = cls._list(cls._sorted(iterable))
        e = truediv_(cls._len(i) - 1, 2)
        p = int(e)
        return i[p] if e % 2 == 0 else truediv_(i[p] + i[p + 1], 2)

    def average(self):
        '''average of all incoming things'''
        return self._inappend(self._average)

    def fsum(self):
        '''add incoming things together'''
        return self._inappend(self._fsum)

    def max(self):
        '''
        find maximum thing in incoming things, optionally using current
        call as key function
        '''
        call_, max_ = self._call, self._max
        if call_ is None:
            return self._inappend(max_)
        return self._inappend(lambda x: max_(x, key=call_))

    def median(self):
        '''median of all incoming things'''
        return self._inappend(self._median)

    def min(self):
        '''find minimum thing in incoming things using call as key function'''
        call_, min_ = self._call, self._min
        if call_ is None:
            return self._inappend(min_)
        return self._inappend(lambda x: min_(x, key=call_))

    def minmax(self):
        '''minimum and maximum things among all incoming things'''
        self._pre()
        iterable1, iterable2 = self._split(self._iterable)
        return self._xtend(iter([min(iterable1), max(iterable2)]))

    def mode(self):
        '''mode of all incoming things'''
        return self._inappend(lambda x: self._counter(x).most_common(1)[0][0])

    def uncommon(self):
        '''least common incoming thing'''
        return self._inappend(
            lambda x: self._counter(x).most_common()[:-2:-1][0][0]
        )

    def frequency(self):
        '''frequency of each incoming thing'''
        return self._inappend(lambda x: self._counter(x).most_common())

    def statrange(self):
        '''statistical range of all incoming things'''
        self._pre()
        iterz = self._list(self._sorted(self._iterable))
        return self._append(iterz[-1] - iterz[0])

    def sum(self, start=0):
        '''
        add all incoming things together

        @param start: starting number (default: 0)
        '''
        sum_ = self._sum
        return self._inappend(lambda x: sum_(x, start))


class TruthMixin(local):

    '''truth mixin'''

    _contains = lazier(contains)

    def all(self):
        '''if `all` incoming things are `True`'''
        return self._pre()._append(all(self._inmap(self._call)))

    def any(self):
        '''if `any` incoming things are `True`'''
        return self._pre()._append(any(self._imap(self._call, self._iterable)))

    def contains(self, thing):
        '''
        if `thing` is in incoming things

        @param thing: some thing
        '''
        contains_ = self._contains
        return self._inappend(lambda x: contains_(x, thing))

    def quantify(self):
        '''how many times call is `True` for incoming things'''
        return self._pre()._append(self._sum(self._inmap(self._call)))


class ReduceMixin(local):

    '''reduce mixin'''

    _zip = lazier(zip)

    @classmethod
    def _roundrobin(cls, iterable):
        '''
        interleave things in iterable into one thing

        @param iterable: an iterable
        '''
        pending = len(cls._split(iterable, 1))
        cycle_ = cycle
        islice_, next_ = cls._islice, cls._next
        nexts_ = cycle_(cls._partial(next_, iter(i)) for i in iterable)
        while pending:
            try:
                for nextz in nexts_:
                    yield nextz()
            except StopIteration:
                pending -= 1
                nexts_ = cycle_(islice_(nexts_, pending))

    @classmethod
    def _smash(cls, iterable):
        '''
        flatten deeply nested iterable

        @param iterable: an iterable
        '''
        isstring_, Iterable_, smash_ = isstring, Iterable, cls._smash
        for i in iterable:
            if isinstance(i, Iterable_) and not isstring_(i):
                for j in smash_(i):
                    yield j
            else:
                yield i

    def merge(self):
        '''flatten nested but ordered incoming things'''
        merge_ = merge
        return self._inxtend(lambda x: merge_(*x))

    def smash(self):
        '''flatten deeply nested incoming things'''
        return self._inxtend(self._smash)

    flatten = smash

    def pairwise(self):
        '''every two incoming things as a tuple'''
        self._pre()
        a, b = self._split(self._iterable)
        next(b, None)
        return self._xtend(self._zip(a, b))

    def reduce(self, initial=None):
        '''
        reduce incoming things to one thing using call (from left side of
        incoming things)

        @param initial: initial thing (default: None)
        '''
        return self._areduce(self._call, initial)

    def reduce_right(self, initial=None):
        '''
        reduce incoming things to one thing from right side of incoming things
        using call

        @param initial: initial thing (default: None)
        '''
        call_ = self._call
        return self._areduce(lambda x, y: call_(y, x), initial)

    def roundrobin(self):
        '''interleave incoming things into one thing'''
        return self._inxtend(self._roundrobin)

    def zip(self):
        '''
        smash incoming things into one single thing, pairing things by iterable
        position
        '''
        zip_ = self._zip
        return self._inxtend(lambda x: zip_(*x))


class ReducingMixin(MathMixin, TruthMixin, ReduceMixin):

    '''reducing mixin'''
