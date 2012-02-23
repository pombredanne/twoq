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

__all__ = ('MathMixin', 'ReduceMixin', 'TruthMixin', 'ReducingMixin')

###############################################################################
## reducing subroutines #######################################################
###############################################################################

isum = sum


def roundrobin(iterable, s=it.islice, c=it.cycle, p=partial, _i=iter, n=next):
    pending = len(iterable)
    nexts = c(p(n, _i(i)) for i in iterable)
    while pending:
        try:
            for nextz in nexts:
                yield nextz()
        except StopIteration:
            pending -= 1
            nexts = c(s(nexts, pending))


def smash(iterable, _isstring=ct.port.isstring, _Iterable=Iterable):
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


class ReduceMixin(local):

    '''reduce mixin'''

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

    def smash(self, _smash=smash):
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

    def roundrobin(self, _roundrobin=roundrobin):
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


class TruthMixin(local):

    '''truth mixin'''

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


class ReducingMixin(MathMixin, ReduceMixin, TruthMixin):

    '''reducing mixin'''