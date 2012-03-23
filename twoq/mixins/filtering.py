# -*- coding: utf-8 -*-
'''twoq filtering mixins'''

from inspect import getmro
from threading import local
from itertools import tee, islice
from functools import partial, reduce as ireduce
from operator import attrgetter, itemgetter, truth

from stuf.six import PY3
from stuf.utils import getcls, ifilter, imap
from twoq.support import chain_iter, filterfalse

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
        members_ = cls._members
        for i in ifilter(call_, members_(iterable)):
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
        with self._sync as sync:
            if PY3:
                def _memfilters(thing, mz=_mz, gc=getcls, ci=chain_iter):
                    t = lambda x: not x[0].startswith('mro')
                    return ifilter(
                        t, ci(imap(mz, ci([getmro((gc(thing))), [thing]])))
                    )
            else:
                def _memfilters(thing, mz=_mz, gc=getcls, ci=chain_iter):
                    return ci(imap(mz, ci([getmro((gc(thing))), [thing]])))
            sync(chain_iter(imap(_memfilters, sync.iterable)))
        return self

    def members(self):
        '''collect object members from incoming things'''
        call_ = self._call
        mz_, chain_iter_ = partial(self._mfilter, call_), chain_iter
        with self._sync as sync:
            sync(chain_iter_(imap(mz_, sync.iterable)))
        return self

    def pick(self, *names):
        '''collect object attributes from incoming things by their `*names`'''
        pick_ = self._pick
        with self._sync as sync:
            sync(pick_(names, sync.iterable))
        return self

    def pluck(self, *keys):
        '''collect object items from incoming things by item `*keys`'''
        pluck_ = self._pluck
        with self._sync as sync:
            sync(pluck_(keys, sync.iterable))
        return self


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
        filt_ = lambda x, y: set(x).difference(y)
        with self._sync as sync:
            sync(ireduce(filt_, sync.iterable))
        return self

    def symmetric_difference(self):
        '''symmetric difference between incoming things'''
        filt_ = lambda x, y: set(x).symmetric_difference(y)
        with self._sync as sync:
            sync(ireduce(filt_, sync.iterable))
        return self

    def disjointed(self):
        '''disjoint between incoming things'''
        filt_ = lambda x, y: set(x).isdisjoint(y)
        with self._sync as sync:
            sync.append(ireduce(filt_, sync.iterable))
        return self

    def intersection(self):
        '''intersection between incoming things'''
        filt_ = lambda x, y: set(x).intersection(y)
        with self._sync as sync:
            sync(ireduce(filt_, sync.iterable))
        return self

    def subset(self):
        '''incoming things are subsets of incoming things'''
        filt_ = lambda x, y: set(x).issubset(y)
        with self._sync as sync:
            sync.append(ireduce(filt_, sync.iterable))
        return self

    def superset(self):
        '''incoming things are supersets of incoming things'''
        filt_ = lambda x, y: set(x).issubset(y)
        with self._sync as sync:
            sync.append(ireduce(filt_, sync.iterable))
        return self

    def union(self):
        '''union between incoming things'''
        filt_ = lambda x, y: set(x).union(y)
        with self._sync as sync:
            sync(ireduce(filt_, sync.iterable))
        return self

    def unique(self):
        '''
        list unique incoming things, preserving order and remember all incoming
        things ever seen
        '''
        call_, unique_ = self._call, self._unique
        with self._sync as sync:
            sync.iter(unique_(sync.iterable, call_))
        return self


class SliceMixin(local):

    '''slicing mixin'''

    def nth(self, n, default=None):
        '''
        `nth` incoming thing or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        with self._sync as sync:
            sync.append(next(islice(sync.iterable, n, None), default))
        return self

    def initial(self):
        '''all incoming things except the last thing'''
        with self._sync as sync:
            iterable1, iterable2 = tee(sync.iterable)
            sync(islice(iterable1, len(list(iterable2)) - 1))
        return self

    def rest(self):
        '''all incoming things except the first thing'''
        with self._sync as sync:
            sync(islice(sync.iterable, 1, None))
        return self

    def snatch(self, n):
        '''
        last `n` things of incoming things

        @param n: number of things
        '''
        with self._sync as sync:
            iterable1, iterable2 = tee(sync.iterable)
            sync(islice(iterable1, len(list(iterable2)) - n, None))
        return self

    def take(self, n):
        '''
        first `n` things of incoming things

        @param n: number of things
        '''
        with self._sync as sync:
            sync(islice(sync.iterable, n))
        return self


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
        with self._sync as sync:
            sync.iter(ifilter(truth, sync.iterable))
        return self

    def filter(self):
        '''incoming things for which call is `True`'''
        call_ = self._call
        with self._sync as sync:
            sync(ifilter(call_, sync.iterable))
        return self

    def find(self):
        '''first incoming thing for which call is `True`'''
        call_ = self._call
        find_ = self._find
        with self._sync as sync:
            sync(find_(call_, sync.iterable))
        return self

    def partition(self):
        '''
        split incoming things into `True` and `False` things based on results
        of call
        '''
        call_, list_ = self._call, list
        with self._sync as sync:
            falsy, truey = tee(sync.iterable)
            sync(iter([
                list_(filterfalse(call_, falsy)), list_(ifilter(call_, truey)),
            ]))
        return self

    def reject(self):
        '''incoming things for which call is `False`'''
        call_ = self._call
        with self._sync as sync:
            sync(filterfalse(call_, sync.iterable))
        return self

    def without(self, *things):
        '''strip things from incoming things'''
        filt_ = lambda x: x in things
        with self._sync as sync:
            sync(filterfalse(filt_, sync.iterable))
        return self


class FilteringMixin(CollectMixin, SetMixin, SliceMixin, FilterMixin):

    '''filtering mixin'''
