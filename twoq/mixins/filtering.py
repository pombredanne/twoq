# -*- coding: utf-8 -*-
'''twoq filtering mixins'''

from inspect import getmro
from threading import local
from itertools import tee, chain, islice
from functools import partial, reduce as ireduce
from operator import attrgetter, itemgetter, truth

from stuf.utils import getcls

from twoq import support as ct

__all__ = ('FilterMixin', 'CollectMixin', 'SetMixin', 'SliceMixin')
chain_iter = chain.from_iterable
_filter = ct.filter
_filterfalse = ct.filterfalse
_map = ct.map
_PY3 = ct.port.PY3

###############################################################################
## filtering subroutines ######################################################
###############################################################################


def find(call, iterable):
    '''
    find the first `True` thing in iterator

    @param call: "Truth" filter
    @param iterable: an iterable
    '''
    for thing in _filter(call, iterable):
        yield thing
        break


def members(iterable):
    '''
    collect members of things

    @param thing: an iterable
    '''
    _getattr = getattr
    for key in dir(iterable):
        try:
            thing = _getattr(iterable, key)
        except AttributeError:
            pass
        else:
            yield key, thing


def mfilter(call, iterable):
    '''
    filter members of things

    @param call: "Truth" filter
    @param iterable: an iterable
    '''
    _members = members
    for i in ct.filter(call, _members(iterable)):
        yield i


def pick(names, iterable):
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


def pluck(keys, iterable):
    '''
    collect values of things in iterable

    @param keys: sequence of keys
    @param iterable: an iterable
    '''
    itemfind = itemgetter(*keys)
    for thing in iterable:
        try:
            yield itemfind(thing)
        except (IndexError, KeyError, TypeError):
            pass


def unique(iterable, key=None):
    '''
    unique things in in iterable

    @param iterable: an iterable
    @param key: determine uniqueness filter
    '''
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in _filterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


###############################################################################
## filter mixins ##############################################################
###############################################################################


class CollectMixin(local):

    '''collecting mixin'''

    def deepmembers(self):
        '''collect object members from incoming things and their bases'''
        _mz = partial(mfilter, self._call)
        with self._sync as sync:
            if _PY3:
                def _memfilters(thing, mz=_mz, gc=getcls, ci=chain_iter):
                    t = lambda x: not x[0].startswith('mro')
                    return _filter(
                        t, ci(_map(mz, ci([getmro((gc(thing))), [thing]])))
                    )
            else:
                def _memfilters(thing, mz=_mz, gc=getcls, ci=chain_iter):
                    return ci(_map(mz, ci([getmro((gc(thing))), [thing]])))
            sync(chain_iter(_map(_memfilters, sync.iterable)))
        return self

    _odeepmembers = deepmembers

    def members(self):
        '''collect object members from incoming things'''
        call = self._call
        _mz = partial(mfilter, call)
        with self._sync as sync:
            sync(chain_iter(_map(_mz, sync.iterable)))
        return self

    _omembers = members

    def pick(self, *names):
        '''collect object attributes from incoming things by their `*names`'''
        with self._sync as sync:
            sync(pick(names, sync.iterable))
        return self

    _opick = pick

    def pluck(self, *keys):
        '''collect object items from incoming things by item `*keys`'''
        with self._sync as sync:
            sync(pluck(keys, sync.iterable))
        return self

    _opluck = pluck


class SetMixin(local):

    '''set and uniqueness mixin'''

    def difference(self):
        '''difference between incoming things'''
        with self._sync as sync:
            sync(ireduce(lambda x, y: set(x).difference(y), sync.iterable))
        return self

    _odifference = difference

    def symmetric_difference(self):
        '''symmetric difference between incoming things'''
        with self._sync as sync:
            sync(ireduce(
                lambda x, y: set(x).symmetric_difference(y), sync.iterable,
            ))
        return self

    _osymmetric_difference = symmetric_difference

    def disjointed(self):
        '''disjoint between incoming things'''
        with self._sync as sync:
            sync.append(ireduce(
                lambda x, y: set(x).isdisjoint(y), sync.iterable,
            ))
        return self

    _disjointed = disjointed

    def intersection(self):
        '''intersection between incoming things'''
        with self._sync as sync:
            sync(ireduce(lambda x, y: set(x).intersection(y), sync.iterable))
        return self

    _ointersection = intersection

    def subset(self):
        '''incoming things are subsets of incoming things'''
        with self._sync as sync:
            sync.append(ireduce(
                lambda x, y: set(x).issubset(y), sync.iterable,
            ))
        return self
    
    _subset = subset

    def superset(self):
        '''incoming things are supersets of incoming things'''
        with self._sync as sync:
            sync.append(ireduce(
                lambda x, y: set(x).issubset(y), sync.iterable
            ))
        return self

    _superset = superset
    
    def union(self):
        '''union between incoming things'''
        with self._sync as sync:
            sync(ireduce(lambda x, y: set(x).union(y), sync.iterable))
        return self

    _ounion = union

    def unique(self):
        '''
        list unique incoming things, preserving order and remember all incoming
        things ever seen
        '''
        with self._sync as sync:
            sync.iter(unique(sync.iterable, self._call))
        return self

    _ounique = unique


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

    _onth = nth

    def initial(self):
        '''all incoming things except the last thing'''
        with self._sync as sync:
            iterable1, iterable2 = tee(sync.iterable)
            sync(islice(iterable1, len(list(iterable2)) - 1))
        return self

    _oinitial = initial

    def rest(self):
        '''all incoming things except the first thing'''
        with self._sync as sync:
            sync(islice(sync.iterable, 1, None))
        return self

    _orest = rest

    def snatch(self, n):
        '''
        last `n` things of incoming things

        @param n: number of things
        '''
        with self._sync as sync:
            iterable1, iterable2 = tee(sync.iterable)
            sync(islice(iterable1, len(list(iterable2)) - n, None))
        return self

    _osnatch = snatch

    def take(self, n):
        '''
        first `n` things of incoming things

        @param n: number of things
        '''
        with self._sync as sync:
            sync(islice(sync.iterable, n))
        return self

    _otake = take


class FilterMixin(CollectMixin, SetMixin, SliceMixin):

    '''filters mixin'''

    def compact(self):
        '''strip "untrue" things from incoming things'''
        with self._sync as sync:
            sync.iter(_filter(truth, sync.iterable))
        return self

    _ocompact = compact

    def filter(self):
        '''incoming things for which call is `True`'''
        call = self._call
        with self._sync as sync:
            sync(_filter(call, sync.iterable))
        return self

    _ofilter = filter

    def find(self):
        '''first incoming thing for which call is `True`'''
        call = self._call
        with self._sync as sync:
            sync(find(call, sync.iterable))
        return self

    _ofind = find

    def partition(self):
        '''
        split incoming things into `True` and `False` things based on results
        of call
        '''
        call = self._call
        with self._sync as sync:
            falsy, truey = tee(sync.iterable)
            sync(iter(
                [list(_filterfalse(call, falsy)), list(_filter(call, truey))]
            ))
        return self

    _opartition = partition

    def reject(self):
        '''incoming things for which call is `False`'''
        call = self._call
        with self._sync as sync:
            sync(_filterfalse(call, sync.iterable))
        return self

    _oreject = reject

    def without(self, *things):
        '''strip things from incoming things'''
        with self._sync as sync:
            sync(_filterfalse(lambda x: x in things, sync.iterable))
        return self

    _owithout = without
