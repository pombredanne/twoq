# -*- coding: utf-8 -*-
'''twoq filtering mixins'''

from inspect import getmro
from threading import local
from operator import attrgetter, itemgetter, truth

from stuf.six import PY3
from stuf.utils import getcls

__all__ = (
    'FilterMixin', 'CollectMixin', 'SetMixin', 'SliceMixin', 'FilteringMixin',
)


class CollectMixin(local):

    '''collecting mixin'''

    @staticmethod
    def _pick(names, iterable):
        '''
        collect attributes of things in iterable

        @param names: sequence of names
        @param iterable: an iterable
        '''
        attrfind = attrgetter(*names)
        for thing in iterable:
            try:
                yield attrfind(thing)
            except AttributeError:
                pass

    @staticmethod
    def _members(iterable):
        '''
        collect members of things

        @param thing: an iterable
        '''
        getattr_, AttributeError_ = getattr, AttributeError
        for key in dir(iterable):
            try:
                thing = getattr_(iterable, key)
            except AttributeError_:
                pass
            else:
                yield key, thing

    @classmethod
    def _mfilter(cls, call, iterable):
        '''
        filter members of things

        @param call: "Truth" filter
        @param iterable: an iterable
        '''
        for i in cls._ifilter(call, cls._members(iterable)):
            yield i

    @staticmethod
    def _pluck(keys, iterable, _itemgetter=itemgetter):
        '''
        collect values of things in iterable

        @param keys: sequence of keys
        @param iterable: an iterable
        '''
        itemfind = _itemgetter(*keys)
        IndexError_, KeyError_, TypeError_ = IndexError, KeyError, TypeError
        for thing in iterable:
            try:
                yield itemfind(thing)
            except (IndexError_, KeyError_, TypeError_):
                pass

    def deepmembers(self):
        '''collect object members from incoming things and their bases'''
        _mz = self._partial(self._mfilter, self._call)
        if PY3:
            def _memfilters(thing, mz=_mz, gc=getcls, ci=self._ichain):
                t = lambda x: not x[0].startswith('mro')
                return self._ifilter(
                    t, ci(self._imap(mz, ci([getmro((gc(thing))), [thing]])))
                )
        else:
            def _memfilters(thing, mz=_mz, gc=getcls, ci=self._ichain):
                return ci(self._imap(mz, ci([getmro((gc(thing))), [thing]])))
        with self._context():
            return self._xtend(
                self._ichain(self._imap(_memfilters, self._iterable))
            )

    def members(self):
        '''collect object members from incoming things'''
        with self._context():
            return self._xtend(self._ichain(self._imap(
                self._partial(self._mfilter, self._call), self._iterable,
            )))

    def pick(self, *names):
        '''collect object attributes from incoming things by their `*names`'''
        with self._context():
            return self._xtend(self._pick(names, self._iterable))

    def pluck(self, *keys):
        '''collect object items from incoming things by item `*keys`'''
        with self._context():
            return self._xtend(self._pluck(keys, self._iterable))


class SetMixin(local):

    '''set and uniqueness mixin'''

    @classmethod
    def _unique(cls, iterable, key=None):
        '''
        unique things in in iterable

        @param iterable: an iterable
        @param key: determine uniqueness filter
        '''
        seen = set()
        seen_add_, seen_contains_ = seen.add, seen.__contains__
        if key is None:
            for element in cls._filterfalse(seen_contains_, iterable):
                seen_add_(element)
                yield element
        else:
            for element in iterable:
                k = key(element)
                if k not in seen:
                    seen_add_(k)
                    yield element

    def difference(self):
        '''difference between incoming things'''
        with self._context():
            return self._xreduce(lambda x, y: set(x).difference(y))

    def symmetric_difference(self):
        '''symmetric difference between incoming things'''
        with self._context():
            return self._xreduce(lambda x, y: set(x).symmetric_difference(y))

    def disjointed(self):
        '''disjoint between incoming things'''
        with self._context():
            return self._areduce(lambda x, y: set(x).isdisjoint(y))

    def intersection(self):
        '''intersection between incoming things'''
        with self._context():
            return self._xreduce(lambda x, y: set(x).intersection(y))

    def subset(self):
        '''incoming things that are subsets of incoming things'''
        with self._context():
            return self._areduce(lambda x, y: set(x).issubset(y))

    def superset(self):
        '''incoming things that are supersets of incoming things'''
        with self._context():
            return self._areduce(lambda x, y: set(x).issubset(y))

    def union(self):
        '''union between incoming things'''
        with self._context():
            return self._xreduce(lambda x, y: set(x).union(y))

    def unique(self):
        '''
        list unique incoming things, preserving order and remember all incoming
        things ever seen
        '''
        with self._context():
            return self._iter(self._unique(self._iterable, self._call))


class SliceMixin(local):

    '''slicing mixin'''

    def nth(self, n, default=None):
        '''
        `nth` incoming thing or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        with self._context():
            return self._append(
                self._next(self._islice(self._iterable, n, None), default)
            )

    def initial(self):
        '''all incoming things except the last thing'''
        with self._context():
            i1, i2 = self._split(self._iterable)
            return self._xtend(self._islice(i1, len(list(i2)) - 1))

    def rest(self):
        '''all incoming things except the first thing'''
        with self._context():
            return self._xtend(self._islice(self._iterable, 1, None))

    def snatch(self, n):
        '''
        last `n` things of incoming things

        @param n: number of things
        '''
        with self._context():
            i1, i2 = self._split(self._iterable)
            return self._xtend(self._islice(
                i1, self._len(self._list(i2)) - n, None
            ))

    def take(self, n):
        '''
        first `n` things of incoming things

        @param n: number of things
        '''
        with self._context():
            return self._xtend(self._islice(self._iterable, n))


class FilterMixin(local):

    '''filters mixin'''

    def compact(self):
        '''strip "untrue" things from incoming things'''
        with self._context():
            return self._iter(self._ifilter(truth, self._iterable))

    def filter(self):
        '''incoming things for which call is `True`'''
        with self._context():
            return self._xtend(self._ifilter(self._call, self._iterable))

    def find(self):
        '''first incoming thing for which call is `True`'''
        with self._context():
            return self._append(
                self._next(self._ifilter(self._call, self._iterable)),
            )

    def partition(self):
        '''
        split incoming things into `True` and `False` things based on results
        of call
        '''
        with self._context():
            list_, call_ = self._list, self._call
            falsy, truey = self._split(self._iterable)
            return self._xtend(self._iter([
                list_(self._filterfalse(call_, falsy)),
                list_(self._ifilter(call_, truey)),
            ]))

    def reject(self):
        '''incoming things for which call is `False`'''
        with self._context():
            return self._xtend(self._filterfalse(self._call, self._iterable))

    def without(self, *things):
        '''strip things from incoming things'''
        with self._context():
            return self._xtend(
                self._filterfalse(lambda y: y in things, self._iterable)
            )


class FilteringMixin(CollectMixin, SetMixin, SliceMixin, FilterMixin):

    '''filtering mixin'''
