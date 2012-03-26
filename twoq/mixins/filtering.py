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
        return self._pre()._xtend(self._ichain(self._inmap(_memfilters)))

    def members(self):
        '''collect object members from incoming things'''
        return self._pre()._xtend(self._ichain(self._inmap(
            self._partial(self._mfilter, self._call),
        )))

    def pick(self, *names):
        '''collect object attributes from incoming things by their `*names`'''
        pick_ = self._pick
        return self._inxtend(lambda x: pick_(names, x))

    def pluck(self, *keys):
        '''collect object items from incoming things by item `*keys`'''
        pluck_ = self._pluck
        return self._inxtend(lambda x: pluck_(keys, x))


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
        return self._xreduce(lambda x, y: set(x).difference(y))

    def symmetric_difference(self):
        '''symmetric difference between incoming things'''
        return self._xreduce(lambda x, y: set(x).symmetric_difference(y))

    def disjointed(self):
        '''disjoint between incoming things'''
        return self._areduce(lambda x, y: set(x).isdisjoint(y))

    def intersection(self):
        '''intersection between incoming things'''
        return self._xreduce(lambda x, y: set(x).intersection(y))

    def subset(self):
        '''incoming things that are subsets of incoming things'''
        return self._areduce(lambda x, y: set(x).issubset(y))

    def superset(self):
        '''incoming things that are supersets of incoming things'''
        return self._areduce(lambda x, y: set(x).issubset(y))

    def union(self):
        '''union between incoming things'''
        return self._xreduce(lambda x, y: set(x).union(y))

    def unique(self):
        '''
        list unique incoming things, preserving order and remember all incoming
        things ever seen
        '''
        return self._pre()._iter(self._unique(self._iterable, self._call))


class SliceMixin(local):

    '''slicing mixin'''

    def nth(self, n, default=None):
        '''
        `nth` incoming thing or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        return self._inappend(
            lambda x: self._next(self._islice(x, n, None), default)
        )

    def initial(self):
        '''all incoming things except the last thing'''
        self._pre()
        iterable1, iterable2 = self._split(self._iterable)
        return self._xtend(self._islice(iterable1, len(list(iterable2)) - 1))

    def rest(self):
        '''all incoming things except the first thing'''
        return self._inxtend(lambda x: self._islice(x, 1, None))

    def snatch(self, n):
        '''
        last `n` things of incoming things

        @param n: number of things
        '''
        self._pre()
        iterable1, iterable2 = self._split(self._iterable)
        return self._xtend(
            self._islice(iterable1, self._len(self._list(iterable2)) - n, None)
        )

    def take(self, n):
        '''
        first `n` things of incoming things

        @param n: number of things
        '''
        return self._inxtend(lambda x: self._islice(x, n))


class FilterMixin(local):

    '''filters mixin'''

    def compact(self):
        '''strip "untrue" things from incoming things'''
        return self._pre()._iter(self._ifilter(truth, self._iterable))

    def filter(self):
        '''incoming things for which call is `True`'''
        return self._inxtend(lambda x: self._ifilter(self._call, x))

    def find(self):
        '''first incoming thing for which call is `True`'''
        return self._inappend(
            lambda x: self._next(self._ifilter(self._call, x)),
        )

    def partition(self):
        '''
        split incoming things into `True` and `False` things based on results
        of call
        '''
        self._pre()
        falsy, truey = self._split(self._iterable)
        return self._xtend(iter([
            list(self._filterfalse(self._call, falsy)),
            list(self._ifilter(self._call, truey)),
        ]))

    def reject(self):
        '''incoming things for which call is `False`'''
        ff_, call_ = self._filterfalse, self._call
        return self._inxtend(lambda x: ff_(call_, x))

    def without(self, *things):
        '''strip things from incoming things'''
        ff_ = self._filterfalse
        return self._inxtend(lambda x: ff_(lambda y: y in things, x))


class FilteringMixin(CollectMixin, SetMixin, SliceMixin, FilterMixin):

    '''filtering mixin'''
