# -*- coding: utf-8 -*-
'''twoq reducing mixins'''

from math import fsum
from heapq import merge
from threading import local
from collections import Iterable
from operator import truediv, contains
from itertools import cycle, tee, islice
from functools import partial, reduce as ireduce

from twoq import support as ct

__all__ = ('MathMixin', 'TruthMixin', 'ReduceMixin')
Counter = ct.Counter
_zip = zip
_map = ct.map

###############################################################################
## reducing subroutines #######################################################
###############################################################################


def roundrobin(iterable):
    '''
    interleave things in iterable into one thing e.g.

    @param iterable: an iterable
    '''
    pending = len(tee(iterable, 1))
    _cycle = cycle
    _islice = islice
    nexts = _cycle(partial(next, iter(i)) for i in iterable)
    while pending:
        try:
            for nextz in nexts:
                yield nextz()
        except StopIteration:
            pending -= 1
            nexts = _cycle(_islice(nexts, pending))


def smash(iterable):
    '''
    flatten deeply nested iterable

    @param iterable: an iterable
    '''
    isstring = ct.port.isstring
    _Iterable = Iterable
    _smash = smash
    for i in iterable:
        if isinstance(i, _Iterable) and not isstring(i):
            for j in _smash(i):
                yield j
        else:
            yield i

###############################################################################
## reducing mixins ############################################################
###############################################################################


class MathMixin(local):

    '''math mixin'''

    def average(self):
        '''average of all incoming things'''
        with self._sync as sync:
            iterable1, iterable2 = tee(sync.iterable)
            sync.append(truediv(sum(iterable1, 0.0), len(list(iterable2))))
        return self

    _oaverage = average

    def fsum(self):
        '''add incoming things together'''
        with self._sync as sync:
            sync.append(fsum(sync.iterable))
        return self

    _ofsum = average

    def max(self):
        '''find maximum thing in incoming things using call as key function'''
        call = self._call
        with self._sync as sync:
            if call is None:
                sync.append(max(sync.iterable))
            else:
                sync.append(max(sync.iterable, key=call))
        return self

    _omax = max

    def median(self):
        '''mean of all incoming things'''
        with self._sync as sync:
            i = list(sorted(sync.iterable))
            e = truediv(len(i) - 1, 2)
            p = int(e)
            sync.append(i[p] if e % 2 == 0 else truediv(i[p] + i[p + 1], 2))
        return self

    _omedian = median

    def min(self):
        '''find minimum thing in incoming things using call as key function'''
        call = self._call
        with self._sync as sync:
            if call is None:
                sync.append(min(sync.iterable))
            else:
                sync.append(min(sync.iterable, key=call))
        return self

    _omin = min

    def minmax(self):
        '''minimum and maximum things among all incoming things'''
        with self._sync as sync:
            iterable1, iterable2 = tee(sync.iterable)
            sync(iter([min(iterable1), max(iterable2)]))
        return self

    _minmax = minmax

    def mode(self):
        '''mode of all incoming things'''
        with self._sync as sync:
            sync.append(Counter(sync.iterable).most_common(1)[0][0])
        return self

    _omode = mode

    def uncommon(self):
        '''least common incoming thing'''
        with self._sync as sync:
            sync.append(Counter(sync.iterable).most_common()[:-2:-1][0][0])
        return self

    _ouncommon = uncommon

    def frequency(self):
        '''frequency of each incoming thing'''
        with self._sync as sync:
            sync.append(Counter(sync.iterable).most_common())
        return self

    _ofrequency = frequency

    def statrange(self):
        '''statistical range of all incoming things'''
        with self._sync as sync:
            iterz = list(sorted(sync.iterable))
            sync.append(iterz[-1] - iterz[0])
        return self

    _ostatrange = statrange

    def sum(self, start=0):
        '''
        add all incoming things together

        @param start: starting number (default: 0)
        '''
        with self._sync as sync:
            sync.append(sum(sync.iterable, start))
        return self

    _osum = sum


class TruthMixin(local):

    '''truth mixin'''

    def all(self):
        '''if `all` incoming things are `True`'''
        call = self._call
        with self._sync as sync:
            sync.append(all(_map(call, sync.iterable)))
        return self

    _oall = all

    def any(self):
        '''if `any` incoming things are `True`'''
        call = self._call
        with self._sync as sync:
            sync.append(any(_map(call, sync.iterable)))
        return self

    _oany = any

    def contains(self, thing):
        '''
        if `thing` is in incoming things

        @param thing: some thing
        '''
        with self._sync as sync:
            sync.append(contains(sync.iterable, thing))
        return self

    _ocontains = contains

    def quantify(self):
        '''how many times call is `True` for incoming things'''
        call = self._call
        with self._sync as sync:
            sync.append(sum(_map(call, sync.iterable)))
        return self

    _oquantify = quantify


class ReduceMixin(MathMixin, TruthMixin):

    '''reducing mixin'''

    def merge(self):
        '''flatten nested but ordered incoming things'''
        with self._sync as sync:
            sync(merge(*sync.iterable))
        return self

    _omerge = merge

    def smash(self):
        '''flatten deeply nested incoming things'''
        with self._sync as sync:
            sync(smash(sync.iterable))
        return self

    _osmash = flatten = smash

    def pairwise(self):
        '''every two incoming things as a tuple'''
        with self._sync as sync:
            a, b = tee(sync.iterable)
            next(b, None)
            sync(_zip(a, b))
        return self

    _opairwise = pairwise

    def reduce(self, initial=None):
        '''
        reduce incoming things to one thing using call (from left side of
        incoming things)

        @param initial: initial thing (default: None)
        '''
        call = self._call
        with self._sync as sync:
            if initial:
                sync.append(ireduce(call, sync.iterable, initial))
            else:
                sync.append(ireduce(call, sync.iterable))
        return self

    _oreduce = reduce

    def reduce_right(self, initial=None):
        '''
        reduce incoming things to one thing from right side of incoming things
        using call

        @param initial: initial thing (default: None)
        '''
        call = self._call
        with self._sync as sync:
            if initial:
                sync(ireduce(lambda x, y: call(y, x), sync.iterable, initial))
            else:
                sync(ireduce(lambda x, y: call(y, x), sync.iterable))
        return self

    _oreduce_right = reduce_right

    def roundrobin(self):
        '''interleave incoming things into one thing'''
        with self._sync as sync:
            sync(roundrobin(sync.iterable))
        return self

    _oroundrobin = roundrobin

    def zip(self):
        '''
        smash incoming things into one single thing, pairing things by iterable
        position
        '''
        with self._sync as sync:
            sync(_zip(*sync.iterable))
        return self

    _ozip = zip
