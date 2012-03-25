# -*- coding: utf-8 -*-
'''twoq ordering mixins'''

from threading import local
from itertools import groupby
from random import choice, shuffle, sample

from twoq.support import zip_longest

__all__ = ('OrderMixin', 'RandomMixin', 'OrderingMixin')


class RandomMixin(local):

    '''random mixin'''

    def choice(self):
        '''random choice of/from incoming things'''
        return self._pre()._append(choice(self._list(self._iterable)))

    def sample(self, n):
        '''
        random sampling drawn from `n` incoming things

        @param n: number of incoming things
        '''
        return self._pre()._extend(sample(self._list(self._iterable), n))

    def shuffle(self):
        '''randomly order incoming things'''
        self._pre()
        iterable = self._list(self._iterable)
        shuffle(iterable)
        return self._extend(iterable)


class OrderMixin(local):

    '''order mixin'''

    def group(self):
        '''group incoming things using call for key function'''
        call_ = self._call
        if call_ is None:
            return self._pre()._extend(self._imap(
                lambda x: [x[0], self._list(x[1])], groupby(self._iterable),
            ))
        return self._pre()._extend(self._imap(
            lambda x: [x[0], self._list(x[1])], groupby(self._iterable, call_)
        ))

    def grouper(self, n, fill=None):
        '''
        split incoming things into sequences of length `n`, using `fill` thing
        to pad incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)
        '''
        return self._pre()._extend(
            zip_longest(fillvalue=fill, *[self._iter(self._iterable)] * n)
        )

    def reverse(self):
        '''reverse incoming things'''
        return self._pre()._extend(self._reversed(self._list(self._iterable)))

    def sort(self):
        '''sort incoming things using call for key function'''
        call_ = self._call
        if call_ is None:
            self._pre()._extend(self._sorted(self._iterable))
        else:
            self._pre()._extend(self._sorted(self._iterable, key=call_))
        return self


class OrderingMixin(OrderMixin, RandomMixin):

    '''ordering mixin'''
