# -*- coding: utf-8 -*-
'''twoq reducing mixins'''

from math import fsum
from heapq import merge
from threading import local
from collections import Iterable
from functools import partial, reduce
from operator import contains, truediv
from itertools import cycle, tee, islice

from twoq.support import Counter, isstring, imap, zip


class MathMixin(local):

    '''math mixin'''

    @classmethod
    def _average(cls, iterable):
        '''average of `iterable`'''
        i1, i2 = tee(iterable)
        return truediv(sum(i1, 0.0), len(list(i2)))

    @classmethod
    def _median(cls, iterable):
        '''median of `iterable`'''
        i = list(sorted(iterable))
        e = truediv(len(i) - 1, 2)
        p = int(e)
        return i[p] if e % 2 == 0 else truediv(i[p] + i[p + 1], 2)

    def average(self):
        '''average of all incoming things'''
        with self._context():
            return self._append(self._average(self._iterable))

    def fsum(self):
        '''add incoming things together'''
        with self._context():
            return self._append(fsum(self._iterable))

    def max(self):
        '''
        find maximum thing in incoming things, optionally using current
        call as key function
        '''
        with self._context():
            return self._append(max(self._iterable, key=self._call))

    def median(self):
        '''median of all incoming things'''
        with self._context():
            return self._append(self._median(self._iterable))

    def min(self):
        '''find minimum thing in incoming things using call as key function'''
        with self._context():
            return self._append(min(self._iterable, key=self._call))

    def minmax(self):
        '''minimum and maximum things among all incoming things'''
        with self._context():
            i1, i2 = tee(self._iterable)
            return self._xtend(iter([min(i1), max(i2)]))

    def mode(self):
        '''mode of all incoming things'''
        with self._context():
            return self._append(
                Counter(self._iterable).most_common(1)[0][0]
            )

    def statrange(self):
        '''statistical range of all incoming things'''
        with self._context():
            iterz = list(sorted(self._iterable))
            return self._append(iterz[-1] - iterz[0])

    def sum(self, start=0):
        '''
        add all incoming things together

        @param start: starting number (default: 0)
        '''
        with self._context():
            return self._append(sum(self._iterable, start))


class TruthMixin(local):

    '''truth mixin'''

    def all(self):
        '''if `all` incoming things are `True`'''
        with self._context():
            return self._append(all(imap(self._call, self._iterable)))

    def any(self):
        '''if `any` incoming things are `True`'''
        with self._context():
            return self._append(any(imap(self._call, self._iterable)))

    def contains(self, thing):
        '''
        if `thing` is found in incoming things

        @param thing: some thing
        '''
        with self._context():
            return self._append(contains(self._iterable, thing))

    def frequency(self):
        '''frequency of each incoming thing'''
        with self._context():
            return self._append(Counter(self._iterable).most_common())

    def quantify(self):
        '''how many times call is `True` for incoming things'''
        with self._context():
            return self._append(sum(imap(self._call, self._iterable)))

    def uncommon(self):
        '''least common incoming thing'''
        with self._context():
            return self._append(
                Counter(self._iterable).most_common()[:-2:-1][0][0]
            )


class ReduceMixin(local):

    '''reduce mixin'''

    @classmethod
    def _roundrobin(cls, iterable):
        '''
        interleave things in iterable into one thing

        @param iterable: an iterable
        '''
        islice_, next_, cycle_ = islice, next, cycle
        nexts_ = cycle_(partial(next_, iter(i)) for i in iterable)
        pending = len(tee(iterable, 1))
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
        with self._context():
            return self._xtend(merge(*self._iterable))

    def pairwise(self):
        '''every two incoming things as a tuple'''
        with self._context():
            i1, i2 = tee(self._iterable)
            next(i2, None)
            return self._xtend(zip(i1, i2))

    def reduce(self, initial=None):
        '''
        reduce incoming things to one thing using call (from left side of
        incoming things)

        @param initial: initial thing (default: None)
        '''
        with self._context():
            if initial is None:
                return self._append(reduce(self._call, self._iterable))
            return self._append(reduce(self._call, self._iterable, initial))

    def reduce_right(self, initial=None):
        '''
        reduce incoming things to one thing from right side of incoming things
        using call

        @param initial: initial thing (default: None)
        '''
        call = self._call
        with self._context():
            if initial is None:
                return self._append(reduce(
                    lambda x, y: call(y, x), self._iterable,
                ))
            return self._append(reduce(
                 lambda x, y: call(y, x), self._iterable, initial,
            ))

    def roundrobin(self):
        '''interleave incoming things into one thing'''
        with self._context():
            return self._xtend(self._roundrobin(self._iterable))
        
    def smash(self):
        '''flatten deeply nested incoming things'''
        with self._context():
            return self._xtend(self._smash(self._iterable))

    flatten = smash

    def zip(self):
        '''
        smash incoming things into one single thing, pairing things by iterable
        position
        '''
        with self._context():
            return self._xtend(zip(*self._iterable))


class ReducingMixin(MathMixin, TruthMixin, ReduceMixin):

    '''reducing mixin'''
