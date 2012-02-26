# -*- coding: utf-8 -*-
'''twoq ordering mixins'''

import random as rm
import itertools as it
from threading import local

from twoq import support as ct

__all__ = ('OrderingMixin', 'OrderMixin', 'RandomMixin')


class OrderingMixin(local):

    '''order mixin'''

    def group(self, _map=ct.map, _groupby=it.groupby):
        '''group incoming things using _call for key function'''
        with self._sync as sync:
            if self._call is None:
                sync(_map(
                    lambda x: [x[0], list(x[1])], _groupby(sync.iterable)
                ))
            else:
                sync(_map(
                    lambda x: [x[0], list(x[1])],
                    _groupby(sync.iterable, self._call),
                ))
        return self

    _ogroup = group

    def grouper(self, n, fill=None, _zipl=ct.zip_longest, _iter=iter):
        '''
        split incoming things into sequences of length `n`, using fill thing to
        pad out incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)

        grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
        '''
        with self._sync as sync:
            sync(_zipl(fillvalue=fill, *[_iter(sync.iterable)] * n))
        return self

    _ogrouper = grouper

    def reverse(self, _reversed=reversed):
        '''reverse incoming things'''
        with self._sync as sync:
            sync(_reversed(sync.iterable))
        return self

    _oreverse = reverse

    def sort(self, _sorted=sorted):
        '''sort incoming things using call for key function'''
        with self._sync as sync:
            if self._call is None:
                sync(_sorted(sync.iterable))
            else:
                sync(_sorted(sync.iterable, key=self._call))
        return self

    _osort = sort


class RandomMixin(local):

    '''random mixin'''

    def choice(self, _choice=rm.choice):
        '''random choice from incoming things'''
        with self._sync as sync:
            sync.append(_choice(sync.iterable))
        return self

    _ochoice = choice

    def sample(self, n, _sample=rm.sample, _list=list):
        '''
        random sampling drawn from `n` incoming things

        @param n: number of things
        '''
        with self._sync as sync:
            sync(_sample(_list(sync.iterable), n))
        return self

    _osample = sample

    def shuffle(self, _shuffle=rm.shuffle):
        '''shuffle incoming things'''
        with self._sync as sync:
            iterable = sync.iterable
            _shuffle(iterable)
            sync(iterable)
        return self

    _oshuffle = shuffle


class OrderMixin(OrderingMixin, RandomMixin):

    '''ordering mixin'''
