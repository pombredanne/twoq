# -*- coding: utf-8 -*-
'''twoq ordering mixins'''

from threading import local
from itertools import product

from twoq.support import zip_longest


class RandomMixin(local):

    '''random mixin'''

    def choice(self):
        '''random choice of/from incoming things'''
        with self._context():
            return self._append(self._choice(self._list(self._iterable)))

    def sample(self, n):
        '''
        random sampling drawn from `n` incoming things

        @param n: number of incoming things
        '''
        with self._context():
            return self._xtend(self._sample(self._list(self._iterable), n))

    def shuffle(self):
        '''randomly order incoming things'''
        with self._context():
            iterable = self._list(self._iterable)
            self._shuffle(iterable)
            return self._xtend(iterable)


class OrderMixin(local):

    '''order mixin'''

    def group(self):
        '''
        group incoming things, optionally using current call for key function
        '''
        call_, list_ = self._call, self._list
        with self._context():
            if call_ is None:
                return self._xtend(self._imap(
                    lambda x: [x[0], list_(x[1])],
                    self._groupby(self._iterable),
                ))
            return self._xtend(self._imap(
                lambda x: [x[0], list_(x[1])],
                self._groupby(self._iterable, call_)
            ))

    def grouper(self, n, fill=None):
        '''
        split incoming things into sequences of length `n`, using `fill` thing
        to pad incomplete sequences

        @param n: number of things
        @param fill: fill thing (default: None)
        '''
        with self._context():
            return self._xtend(
                zip_longest(fillvalue=fill, *[self._iterz(self._iterable)] * n)
            )

    def reverse(self):
        '''reverse order of incoming things'''
        with self._context():
            return self._xtend(self._reversed(self._list(self._iterable)))

    def sort(self):
        '''
        sort incoming things, optionally using current call as key function
        '''
        call_ = self._call
        with self._context():
            if call_ is None:
                return self._xtend(self._sorted(self._iterable))
            return self._xtend(self._sorted(self._iterable, key=call_))


class CombineMixin(local):

    '''combination mixin'''

    def product(self, n=1):
        '''
        nested for each loops repeated `n` times

        @param n: number of repetitions (default: 1)
        '''
        with self._context():
            return self._xtend(product(*self._iterable, repeat=n))


class OrderingMixin(OrderMixin, RandomMixin, CombineMixin):

    '''ordering mixin'''
