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
        with self._sync as sync:
            iterable1, iterable2 = tee(sync.iterable)
            sync.append(truediv(sum(iterable1, 0.0), len(list(iterable2))))
        return self

    def fsum(self):
        '''add incoming things together'''
        with self._sync as sync:
            sync.append(fsum(sync.iterable))
        return self

    def max(self):
        '''find maximum thing in incoming things using call_ as key function'''
        call_ = self._call
        with self._sync as sync:
            if call_ is None:
                sync.append(max(sync.iterable))
            else:
                sync.append(max(sync.iterable, key=call_))
        return self

    def median(self):
        '''mean of all incoming things'''
        with self._sync as sync:
            i = list(sorted(sync.iterable))
            e = truediv(len(i) - 1, 2)
            p = int(e)
            sync.append(i[p] if e % 2 == 0 else truediv(i[p] + i[p + 1], 2))
        return self

    def min(self):
        '''find minimum thing in incoming things using call_ as key function'''
        call_ = self._call
        with self._sync as sync:
            if call_ is None:
                sync.append(min(sync.iterable))
            else:
                sync.append(min(sync.iterable, key=call_))
        return self

    def minmax(self):
        '''minimum and maximum things among all incoming things'''
        with self._sync as sync:
            iterable1, iterable2 = tee(sync.iterable)
            sync(iter([min(iterable1), max(iterable2)]))
        return self

    def mode(self):
        '''mode of all incoming things'''
        with self._sync as sync:
            sync.append(Counter(sync.iterable).most_common(1)[0][0])
        return self

    def uncommon(self):
        '''least common incoming thing'''
        with self._sync as sync:
            sync.append(Counter(sync.iterable).most_common()[:-2:-1][0][0])
        return self

    def frequency(self):
        '''frequency of each incoming thing'''
        with self._sync as sync:
            sync.append(Counter(sync.iterable).most_common())
        return self

    def statrange(self):
        '''statistical range of all incoming things'''
        with self._sync as sync:
            iterz = list(sorted(sync.iterable))
            sync.append(iterz[-1] - iterz[0])
        return self

    def sum(self, start=0):
        '''
        add all incoming things together

        @param start: starting number (default: 0)
        '''
        with self._sync as sync:
            sync.append(sum(sync.iterable, start))
        return self


class TruthMixin(local):

    '''truth mixin'''

    def all(self):
        '''if `all` incoming things are `True`'''
        call_ = self._call
        with self._sync as sync:
            sync.append(all(imap(call_, sync.iterable)))
        return self

    def any(self):
        '''if `any` incoming things are `True`'''
        call_ = self._call
        with self._sync as sync:
            sync.append(any(imap(call_, sync.iterable)))
        return self

    def contains(self, thing):
        '''
        if `thing` is in incoming things

        @param thing: some thing
        '''
        with self._sync as sync:
            sync.append(contains(sync.iterable, thing))
        return self

    def quantify(self):
        '''how many times call is `True` for incoming things'''
        call_ = self._call
        with self._sync as sync:
            sync.append(sum(imap(call_, sync.iterable)))
        return self


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
        with self._sync as sync:
            sync(merge(*sync.iterable))
        return self

    def smash(self):
        '''flatten deeply nested incoming things'''
        with self._sync as sync:
            sync(self._smash(sync.iterable))
        return self

    flatten = smash

    def pairwise(self):
        '''every two incoming things as a tuple'''
        with self._sync as sync:
            a, b = tee(sync.iterable)
            next(b, None)
            sync(zip(a, b))
        return self

    def reduce(self, initial=None):
        '''
        reduce incoming things to one thing using call (from left side of
        incoming things)

        @param initial: initial thing (default: None)
        '''
        call_ = self._call
        with self._sync as sync:
            if initial:
                sync.append(ireduce(call_, sync.iterable, initial))
            else:
                sync.append(ireduce(call_, sync.iterable))
        return self

    def reduce_right(self, initial=None):
        '''
        reduce incoming things to one thing from right side of incoming things
        using call

        @param initial: initial thing (default: None)
        '''
        call_ = self._call
        filt_ = lambda x, y: call_(y, x)
        with self._sync as sync:
            if initial:
                sync(ireduce(filt_, sync.iterable, initial))
            else:
                sync(ireduce(filt_, sync.iterable))
        return self

    def roundrobin(self):
        '''interleave incoming things into one thing'''
        with self._sync as sync:
            sync(self._roundrobin(sync.iterable))
        return self

    def zip(self):
        '''
        smash incoming things into one single thing, pairing things by iterable
        position
        '''
        with self._sync as sync:
            sync(zip(*sync.iterable))
        return self


class ReducingMixin(MathMixin, TruthMixin, ReduceMixin):

    '''reducing mixin'''
