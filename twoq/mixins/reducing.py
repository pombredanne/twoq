# -*- coding: utf-8 -*-
'''twoq reducing mixins'''

from math import fsum
from heapq import merge
from threading import local
from collections import Iterable
from operator import truediv, contains
from itertools import cycle, tee, islice
from functools import partial, reduce as ireduce

from stuf.utils import imap
from twoq.support import Counter, isstring, zip

__all__ = ('MathMixin', 'TruthMixin', 'ReduceMixin', 'ReducingMixin')


class MathMixin(local):

    '''math mixin'''

    def average(self):
        '''average of all incoming things'''
        self._pre()
        i1, i2 = self._split(self._iterable)
        return self._append(truediv(sum(i1, 0.0), len(list(i2))))

    def fsum(self):
        '''add incoming things together'''
        return self._pre()._append(fsum(self._iterable))

    def max(self):
        '''find maximum thing in incoming things using call_ as key function'''
        call_ = self._call
        if call_ is None:
            return self._pre()._append(max(self._iterable))
        return self._pre()._append(max(self._iterable, key=call_))

    def median(self):
        '''mean of all incoming things'''
        self._pre()
        i = list(sorted(self._iterable))
        e = truediv(len(i) - 1, 2)
        p = int(e)
        return self._append(
            i[p] if e % 2 == 0 else truediv(i[p] + i[p + 1], 2)
        )

    def min(self):
        '''find minimum thing in incoming things using call_ as key function'''
        call_ = self._call
        if call_ is None:
            return self._pre()._append(min(self._iterable))
        return self._pre()._append(min(self._iterable, key=call_))

    def minmax(self):
        '''minimum and maximum things among all incoming things'''
        self._pre()
        iterable1, iterable2 = self._split(self._iterable)
        return self._extend(iter([min(iterable1), max(iterable2)]))

    def mode(self):
        '''mode of all incoming things'''
        return self._pre()._append(Counter(
            self._iterable
        ).most_common(1)[0][0])

    def uncommon(self):
        '''least common incoming thing'''
        return self._pre()._append(
            Counter(self._iterable).most_common()[:-2:-1][0][0]
        )

    def frequency(self):
        '''frequency of each incoming thing'''
        return self._pre()._append(Counter(self._iterable).most_common())

    def statrange(self):
        '''statistical range of all incoming things'''
        self._pre()
        iterz = list(sorted(self._iterable))
        return self._append(iterz[-1] - iterz[0])

    def sum(self, start=0):
        '''
        add all incoming things together

        @param start: starting number (default: 0)
        '''
        return self._pre()._append(sum(self._iterable, start))


class TruthMixin(local):

    '''truth mixin'''

    def all(self):
        '''if `all` incoming things are `True`'''
        self._pre()._append(all(imap(self._call, self._iterable)))
        return self

    def any(self):
        '''if `any` incoming things are `True`'''
        return self._pre()._append(any(imap(self._call, self._iterable)))

    def contains(self, thing):
        '''
        if `thing` is in incoming things

        @param thing: some thing
        '''
        return self._pre()._append(contains(self._iterable, thing))

    def quantify(self):
        '''how many times call is `True` for incoming things'''
        return self._pre()._append(sum(imap(self._call, self._iterable)))


class ReduceMixin(local):

    '''reduce mixin'''

    @staticmethod
    def _roundrobin(iterable):
        '''
        interleave things in iterable into one thing

        @param iterable: an iterable
        '''
        pending = len(tee(iterable, 1))
        cycle_ = cycle
        islice_ = islice
        nexts_ = cycle_(partial(next, iter(i)) for i in iterable)
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
        return self._pre()._extend(merge(*self._iterable))

    def smash(self):
        '''flatten deeply nested incoming things'''
        return self._pre()._extend(self._smash(self._iterable))

    flatten = smash

    def pairwise(self):
        '''every two incoming things as a tuple'''
        self._pre()
        a, b = self._split(self._iterable)
        next(b, None)
        return self._extend(zip(a, b))

    def reduce(self, initial=None):
        '''
        reduce incoming things to one thing using call (from left side of
        incoming things)

        @param initial: initial thing (default: None)
        '''
        if initial is None:
            return self._pre()._append(ireduce(self._call, self._iterable))
        return self._pre()._append(
            ireduce(self._call, self._iterable, initial)
        )

    def reduce_right(self, initial=None):
        '''
        reduce incoming things to one thing from right side of incoming things
        using call

        @param initial: initial thing (default: None)
        '''
        call_, filt_ = self._call, lambda x, y: call_(y, x)
        if initial:
            return self._pre()._extend(ireduce(filt_, self._iterable, initial))
        return self._pre()._extend(ireduce(filt_, self._iterable))

    def roundrobin(self):
        '''interleave incoming things into one thing'''
        return self._pre()._extend(self._roundrobin(self._iterable))

    def zip(self):
        '''
        smash incoming things into one single thing, pairing things by iterable
        position
        '''
        return self._pre()._extend(zip(*self._iterable))


class ReducingMixin(MathMixin, TruthMixin, ReduceMixin):

    '''reducing mixin'''
