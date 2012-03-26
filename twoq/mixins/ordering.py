# -*- coding: utf-8 -*-
'''twoq ordering mixins'''

from threading import local
from itertools import groupby
from random import choice, shuffle, sample

from twoq.support import zip_longest, lazier

__all__ = ('OrderMixin', 'RandomMixin', 'OrderingMixin')


class RandomMixin(local):

    '''random mixin'''

    _choice = lazier(choice)
    _sample = lazier(sample)
    _shuffle = lazier(shuffle)

    @classmethod
    def _shuffleit(cls, iterable):
        '''
        shuffle iterable

        @param iterable: an iterable
        '''
        iterable = cls._list(iterable)
        cls._shuffle(iterable)
        return iterable

    def choice(self):
        '''random choice of/from incoming things'''
        return self._inappend(lambda x: self._choice(self._list(x)))

    def sample(self, n):
        '''
        random sampling drawn from `n` incoming things

        @param n: number of incoming things
        '''
        sample_, list_ = self._sample, self._list
        return self._inxtend(lambda x: sample_(list_(x), n))

    def shuffle(self):
        '''randomly order incoming things'''
        return self._inxtend(self._shuffleit)


class OrderMixin(local):

    '''order mixin'''

    _groupby = lazier(groupby)

    def group(self):
        '''
        group incoming things, optionally using current call for key function
        '''
        call_, list_ = self._call, self._list
        if call_ is None:
            return self._x2map(
                lambda x: [x[0], list_(x[1])], self._groupby,
            )
        return self._x2map(
            lambda x: [x[0], list_(x[1])], lambda x: self._groupby(x, call_)
        )

    def grouper(self, n, fill=None):
        '''
        split incoming things into sequences of length `n`, using `fill` thing
        to pad incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)
        '''
        iter_ = self._iter
        return self._inxtend(
            lambda x: zip_longest(fillvalue=fill, *[iter_(x)] * n)
        )

    def reverse(self):
        '''reverse incoming things'''
        list_, reversed_ = self._list, self._reversed
        return self._inxtend(lambda x: reversed_(list_(x)))

    def sort(self):
        '''
        sort incoming things, optionally using current call as key function
        '''
        call_, sorted_ = self._call, self._sorted
        if call_ is None:
            return self._inxtend(sorted_)
        return self._inxtend(lambda x: sorted_(x, key=call_))


class OrderingMixin(OrderMixin, RandomMixin):

    '''ordering mixin'''
