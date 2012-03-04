# -*- coding: utf-8 -*-
'''twoq ordering mixins'''

from threading import local
from itertools import groupby
from random import choice, shuffle, sample

from twoq import support as ct

__all__ = ('OrderMixin', 'RandomMixin', 'OrderingMixin')
_map = ct.map
_zip_longest = ct.zip_longest


class RandomMixin(local):

    '''random mixin'''

    def choice(self):
        '''random choice of/from incoming things'''
        with self._sync as sync:
            sync.append(choice(list(sync.iterable)))
        return self

    _ochoice = choice

    def sample(self, n):
        '''
        random sampling drawn from `n` incoming things

        @param n: number of incoming things
        '''
        with self._sync as sync:
            sync(sample(list(sync.iterable), n))
        return self

    _osample = sample

    def shuffle(self):
        '''randomly order incoming things'''
        with self._sync as sync:
            iterable = list(sync.iterable)
            shuffle(iterable)
            sync(iterable)
        return self

    _oshuffle = shuffle


class OrderMixin(local):

    '''order mixin'''

    def group(self):
        '''group incoming things using call for key function'''
        call = self._call
        with self._sync as sync:
            if call is None:
                sync(_map(
                    lambda x: [x[0], list(x[1])], groupby(sync.iterable)
                ))
            else:
                sync(_map(
                    lambda x: [x[0], list(x[1])], groupby(sync.iterable, call),
                ))
        return self

    _ogroup = group

    def grouper(self, n, fill=None):
        '''
        split incoming things into sequences of length `n`, using `fill` thing
        to pad incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)
        '''
        with self._sync as sync:
            sync(_zip_longest(fillvalue=fill, *[iter(sync.iterable)] * n))
        return self

    _ogrouper = grouper

    def reverse(self):
        '''reverse incoming things'''
        with self._sync as sync:
            sync(reversed(list(sync.iterable)))
        return self

    _oreverse = reverse

    def sort(self):
        '''sort incoming things using call for key function'''
        call = self._call
        with self._sync as sync:
            if self._call is None:
                sync(sorted(sync.iterable))
            else:
                sync(sorted(sync.iterable, key=call))
        return self

    _osort = sort


class OrderingMixin(OrderMixin, RandomMixin):

    '''ordering mixin'''
