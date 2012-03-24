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
        return self._append(choice(list(self._iterable)))

    def sample(self, n):
        '''
        random sampling drawn from `n` incoming things

        @param n: number of incoming things
        '''
        return self._extend(sample(list(self._iterable), n))

    def shuffle(self):
        '''randomly order incoming things'''
        iterable = list(self._iterable)
        shuffle(iterable)
        return self._extend(iterable)


class OrderMixin(local):

    '''order mixin'''

    def group(self):
        '''group incoming things using call for key function'''
        call_, filt_ = self._call, lambda x: [x[0], list(x[1])]
        if call_ is None:
            return self._extend(imap(filt_, groupby(self._iterable)))
        return self._extend(imap(filt_, groupby(self._iterable, call_)))

    def grouper(self, n, fill=None):
        '''
        split incoming things into sequences of length `n`, using `fill` thing
        to pad incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)
        '''
        return self._extend(
            zip_longest(fillvalue=fill, *[iter(self._iterable)] * n)
        )

    def reverse(self):
        '''reverse incoming things'''
        return self._extend(reversed(list(self._iterable)))

    def sort(self):
        '''sort incoming things using call for key function'''
        call_ = self._call
        if call_ is None:
            self._extend(sorted(self._iterable))
        else:
            self._extend(sorted(self._iterable, key=call_))
        return self


class OrderingMixin(OrderMixin, RandomMixin):

    '''ordering mixin'''
