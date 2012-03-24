# -*- coding: utf-8 -*-
'''twoq filtering mixins'''

from inspect import getmro
from threading import local
from itertools import islice
from functools import partial
from operator import attrgetter, itemgetter, truth

from stuf.six import PY3
from stuf.utils import getcls, ifilter, imap

from twoq.support import ichain, filterfalse

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
    def _mfilter(cls, call_, iterable):
        '''
        filter members of things

        @param call: "Truth" filter
        @param iterable: an iterable
        '''
        for i in ifilter(call_, cls._members(iterable)):
            yield i

    @staticmethod
    def _pluck(keys, iterable):
        '''
        collect values of things in iterable

        @param keys: sequence of keys
        @param iterable: an iterable
        '''
        itemfind = itemgetter(*keys)
        IndexError_, KeyError_, TypeError_ = IndexError, KeyError, TypeError
        for thing in iterable:
            try:
                yield itemfind(thing)
            except (IndexError_, KeyError_, TypeError_):
                pass

    def deepmembers(self):
        '''collect object members from incoming things and their bases'''
        _mz = partial(self._mfilter, self._call)
        if PY3:
            def _memfilters(thing, mz=_mz, gc=getcls, ci=ichain):
                t = lambda x: not x[0].startswith('mro')
                return ifilter(
                    t, ci(imap(mz, ci([getmro((gc(thing))), [thing]])))
                )
        else:
            def _memfilters(thing, mz=_mz, gc=getcls, ci=ichain):
                return ci(imap(mz, ci([getmro((gc(thing))), [thing]])))
        return self._pre()._extend(ichain(imap(_memfilters, self._iterable)))

    def members(self):
        '''collect object members from incoming things'''
        return self._pre()._extend(ichain(imap(
            partial(self._mfilter, self._call), self._iterable,
        )))

    def pick(self, *names):
        '''collect object attributes from incoming things by their `*names`'''
        return self._pre()._extend(self._pick(names, self._iterable))

    def pluck(self, *keys):
        '''collect object items from incoming things by item `*keys`'''
        return self._pre()._extend(self._pluck(keys, self._iterable))


class SetMixin(local):

    '''set and uniqueness mixin'''

    @staticmethod
    def _unique(iterable, key=None):
        '''
        unique things in in iterable

        @param iterable: an iterable
        @param key: determine uniqueness filter
        '''
        seen = set()
        seen_add_, seen_contains_ = seen.add, seen.__contains__
        if key is None:
            for element in filterfalse(seen_contains_, iterable):
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
        return self._pre()._append(
            next(islice(self._iterable, n, None), default)
        )

    def initial(self):
        '''all incoming things except the last thing'''
        self._pre()
        iterable1, iterable2 = self._split(self._iterable)
        return self._extend(islice(iterable1, len(list(iterable2)) - 1))

    def rest(self):
        '''all incoming things except the first thing'''
        return self._pre()._extend(islice(self._iterable, 1, None))

    def snatch(self, n):
        '''
        last `n` things of incoming things

        @param n: number of things
        '''
        self._pre()
        iterable1, iterable2 = self._split(self._iterable)
        return self._extend(
            islice(iterable1, len(list(iterable2)) - n, None)
        )

    def take(self, n):
        '''
        first `n` things of incoming things

        @param n: number of things
        '''
        return self._pre()._extend(islice(self._iterable, n))


class FilterMixin(local):

    '''filters mixin'''

    @staticmethod
    def _find(call, iterable):
        '''
        find the first `True` thing in iterator

        @param call: "Truth" filter
        @param iterable: an iterable
        '''
        for thing in ifilter(call, iterable):
            yield thing
            break

    def compact(self):
        '''strip "untrue" things from incoming things'''
        return self._pre()._iter(ifilter(truth, self._iterable))

    def filter(self):
        '''incoming things for which call is `True`'''
        return self._pre()._extend(ifilter(self._call, self._iterable))

    def find(self):
        '''first incoming thing for which call is `True`'''
        return self._pre()._extend(self._find(self._call, self._iterable))

    def partition(self):
        '''
        split incoming things into `True` and `False` things based on results
        of call
        '''
        self._pre()
        falsy, truey = self._split(self._iterable)
        return self._extend(iter([
            list(filterfalse(self._call, falsy)),
            list(ifilter(self._call, truey)),
        ]))

    def reject(self):
        '''incoming things for which call is `False`'''
        return self._pre()._extend(filterfalse(self._call, self._iterable))

    def without(self, *things):
        '''strip things from incoming things'''
        return self._pre()._extend(
            filterfalse(lambda x: x in things, self._iterable)
        )


class FilteringMixin(CollectMixin, SetMixin, SliceMixin, FilterMixin):

    '''filtering mixin'''
