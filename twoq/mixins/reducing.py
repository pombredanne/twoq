# -*- coding: utf-8 -*-
'''twoq reducing mixins'''

import math as mt
import heapq as hq
import operator as op
import itertools as it
import functools as ft
from threading import local
from functools import partial
from collections import Iterable

from twoq import support as ct

__all__ = ('MathMixin', 'ReducingMixin', 'TruthMixin', 'ReduceMixin')
isum = sum

###############################################################################
## reducing subroutines #######################################################
###############################################################################


def roundrobin(iterable, s=it.islice, c=it.cycle, p=partial, _i=iter, n=next):
    '''
    interleave things in iterable into one thing e.g.

    @param iterable: an iterable
    '''
    pending = len(it.tee(iterable, 1))
    nexts = c(p(n, _i(i)) for i in iterable)
    while pending:
        try:
            for nextz in nexts:
                yield nextz()
        except StopIteration:
            pending -= 1
            nexts = c(s(nexts, pending))


def smash(iterable, _isstring=ct.port.isstring, _Iterable=Iterable):
    '''
    flatten deeply nested iterable

    @param iterable: an iterable
    '''
    for i in iterable:
        if isinstance(i, _Iterable) and not _isstring(i):
            for j in smash(i):
                yield j
        else:
            yield i

###############################################################################
## reducing mixins ############################################################
###############################################################################


class MathMixin(local):

    '''math mixin'''

    def average(self, _sum=isum, _truediv=op.truediv, _len=len):
        '''average of all incoming things'''
        with self._sync as sync:
            iterable1, iterable2 = it.tee(sync.iterable)
            sync.append(_truediv(_sum(iterable1, 0.0), _len(list(iterable2))))
        return self

    _oaverage = average

    def fsum(self, _fsum=mt.fsum):
        '''
        add incoming things together

        @param start: starting number (default: 0)
        '''
        with self._sync as sync:
            sync.append(_fsum(sync.iterable))
        return self

    _ofsum = average

    def max(self, _max=max):
        '''find maximum value in incoming things using call for key function'''
        with self._sync as sync:
            if self._call is None:
                sync.append(_max(sync.iterable))
            else:
                sync.append(_max(sync.iterable, key=self._call))
        return self

    _omax = max

    def median(self, _div=op.truediv, _len=len, _srt=sorted, _l=list, _i=int):
        '''mean of incoming things'''
        with self._sync as sync:
            i = list(_srt(sync.iterable))
            e = _div(_len(i) - 1, 2)
            p = _i(e)
            sync.append(i[p] if e % 2 == 0 else _div(i[p] + i[p + 1], 2))
        return self

    _omedian = median

    def min(self, _min=min):
        '''find minimum value in incoming things using call for key function'''
        with self._sync as sync:
            if self._call is None:
                sync.append(_min(sync.iterable))
            else:
                sync.append(_min(sync.iterable, key=self._call))
        return self

    _omin = min

    def minmax(self):
        '''minimum and maximum values among incoming things'''
        with self._sync as sync:
            iterable1, iterable2 = it.tee(sync.iterable)
            sync(iter([min(iterable1), max(iterable2)]))
        return self

    _minmax = minmax

    def mode(self, _cnt=ct.Counter):
        '''mode of incoming things'''
        with self._sync as sync:
            sync.append(_cnt(sync.iterable).most_common(1)[0][0])
        return self

    _omode = mode

    def uncommon(self, _cnt=ct.Counter):
        '''least common incoming thing'''
        with self._sync as sync:
            sync.append(_cnt(sync.iterable).most_common()[:-2:-1][0][0])
        return self

    _ouncommon = uncommon

    def frequency(self, _cnt=ct.Counter):
        '''frequency of each incoming thing'''
        with self._sync as sync:
            sync.append(_cnt(sync.iterable).most_common())
        return self

    _ofrequency = frequency

    def statrange(self, _srt=sorted, _list=list):
        '''statistical range of incoming things'''
        with self._sync as sync:
            iterz = _list(_srt(sync.iterable))
            sync.append(iterz[-1] - iterz[0])
        return self

    _ostatrange = statrange

    def sum(self, start=0, _sum=sum):
        '''
        add incoming things together

        @param start: starting number (default: 0)
        '''
        with self._sync as sync:
            sync.append(_sum(sync.iterable, start))
        return self

    _osum = sum


class ReducingMixin(local):

    '''reduce mixin'''

    def merge(self, _merge=hq.merge):
        '''flatten nested and ordered incoming things'''
        with self._sync as sync:
            sync(_merge(*sync.iterable))
        return self

    _omerge = merge

    def smash(self, _smash=smash):
        '''flatten deeply nested incoming things'''
        with self._sync as sync:
            sync(_smash(sync.iterable))
        return self

    _osmash = flatten = smash

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

    _opairwise = pairwise

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

    _oreduce = reduce

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

    _oreduce_right = reduce_right

    def roundrobin(self, _roundrobin=roundrobin):
        '''
        interleave incoming things into one thing e.g.

        roundrobin('ABC', 'D', 'EF') --> A D E B F C
        '''
        with self._sync as sync:
            sync(_roundrobin(sync.iterable))
        return self

    _oroundrobin = roundrobin

    def zip(self, _zip=ct.zip):
        '''
        smash incoming things into single thing, pairing things by iterable
        position
        '''
        with self._sync as sync:
            sync(_zip(*sync.iterable))
        return self

    _ozip = zip


class TruthMixin(local):

    '''truth mixin'''

    def all(self, _all=all, _map=ct.map):
        '''if `all` incoming things are `True`'''
        with self._sync as sync:
            sync.append(_all(_map(self._call, sync.iterable)))
        return self

    _oall = all

    def any(self, _any=any, _map=ct.map):
        '''if `any` incoming things are `True`'''
        with self._sync as sync:
            sync.append(_any(_map(self._call, sync.iterable)))
        return self

    _oany = any

    def contains(self, thing, _contains=op.contains):
        '''
        if `thing` is in incoming things

        @param thing: some thing
        '''
        with self._sync as sync:
            sync.append(_contains(sync.iterable, thing))
        return self

    _ocontains = contains

    def quantify(self, _sum=isum, _map=ct.map):
        '''how many times call is True for incoming things'''
        with self._sync as sync:
            sync.append(_sum(_map(self._call, sync.iterable)))
        return self

    _oquantify = quantify


class ReduceMixin(MathMixin, ReducingMixin, TruthMixin):

    '''reducing mixin'''
