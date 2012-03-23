# -*- coding: utf-8 -*-
'''twoq ordering mixins'''

from threading import local
from itertools import groupby
from random import choice, shuffle, sample

from stuf.utils import imap
from twoq.support import zip_longest

__all__ = ('OrderMixin', 'RandomMixin', 'OrderingMixin')


class RandomMixin(local):

    '''random mixin'''

    def choice(self):
        '''random choice of/from incoming things'''
        with self._sync as sync:
            sync.append(choice(list(sync.iterable)))
        return self

    def sample(self, n):
        '''
        random sampling drawn from `n` incoming things

        @param n: number of incoming things
        '''
        with self._sync as sync:
            sync(sample(list(sync.iterable), n))
        return self

    def shuffle(self):
        '''randomly order incoming things'''
        with self._sync as sync:
            iterable = list(sync.iterable)
            shuffle(iterable)
            sync(iterable)
        return self


class OrderMixin(local):

    '''order mixin'''

    def group(self):
        '''group incoming things using call for key function'''
        call_ = self._call
        filt_ = lambda x: [x[0], list(x[1])]
        with self._sync as sync:
            if call_ is None:
                sync(imap(filt_, groupby(sync.iterable)))
            else:
                sync(imap(filt_, groupby(sync.iterable, call_)))
        return self

    def grouper(self, n, fill=None):
        '''
        split incoming things into sequences of length `n`, using `fill` thing
        to pad incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)
        '''
        with self._sync as sync:
            sync(zip_longest(fillvalue=fill, *[iter(sync.iterable)] * n))
        return self

    def reverse(self):
        '''reverse incoming things'''
        with self._sync as sync:
            sync(reversed(list(sync.iterable)))
        return self

    def sort(self):
        '''sort incoming things using call for key function'''
        call_ = self._call
        with self._sync as sync:
            if call_ is None:
                sync(sorted(sync.iterable))
            else:
                sync(sorted(sync.iterable, key=call_))
        return self


class OrderingMixin(OrderMixin, RandomMixin):

    '''ordering mixin'''
