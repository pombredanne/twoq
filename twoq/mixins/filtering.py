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

###############################################################################
## filtering subroutines ######################################################
###############################################################################


def find(call, iterable):
    '''
    find the first `True` thing in iterator

    @param call: "Truth" filter
    @param iterable: an iterable
    '''
    for thing in ct.filter(call, iterable):
        yield thing
        break


def members(iterable):
    '''
    collect members of things

    @param thing: an iterable
    '''
    for key in dir(iterable):
        try:
            thing = getattr(iterable, key)
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
    for i in ct.filter(call, members(iterable)):
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
        for element in ct.filterfalse(seen.__contains__, iterable):
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

    '''gathering mixin'''

    def deepmembers(self):
        '''collect members of incoming things and their bases'''
        _mz = partial(mfilter, self._call)
        with self._sync as sync:
            if ct.port.PY3:
                def _memfilters(thing, mz=_mz, gc=getcls, ci=chain_iter):
                    t = lambda x: not x[0].startswith('mro')
                    return ct.filter(
                        t, ci(ct.map(mz, ci([getmro((gc(thing))), [thing]])))
                    )
            else:
                def _memfilters(thing, mz=_mz, gc=getcls, ci=chain_iter):
                    return ci(ct.map(mz, ci([getmro((gc(thing))), [thing]])))
            sync(chain_iter(ct.map(_memfilters, sync.iterable)))
        return self

    _odeepmembers = deepmembers

    def members(self):
        '''collect members of incoming things'''
        _mz = partial(mfilter, self._call)
        with self._sync as sync:
            sync(chain_iter(ct.map(_mz, sync.iterable)))
        return self

    _omembers = members

    def pick(self, *names):
        '''attributes of incoming things by attribute `*names`'''
        with self._sync as sync:
            sync(pick(names, sync.iterable))
        return self

    _opick = pick

    def pluck(self, *keys):
        '''items of incoming things by item `*keys`'''
        with self._sync as sync:
            sync(pluck(keys, sync.iterable))
        return self

    _opluck = pluck


class SetMixin(local):

    '''set and uniqueness mixin'''

    def difference(self):
        '''difference between incoming things'''
        with self._sync as sync:
            sync(ireduce(
                lambda x, y: set(x).difference(set(y)), sync.iterable,
            ))
        return self

    _odifference = difference

    def intersection(self):
        '''intersection between incoming things'''
        with self._sync as sync:
            sync(ireduce(
                lambda x, y: set(x).intersection(set(y)), sync.iterable,
            ))
        return self

    _ointersection = intersection

    def union(self):
        '''union between incoming things'''
        with self._sync as sync:
            sync(ireduce(lambda x, y: set(x).union(set(y)), sync.iterable))
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
        nth incoming thing or default thing

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
            sync.iter(ct.filter(truth, sync.iterable))
        return self

    _ocompact = compact

    def filter(self):
        '''incoming things for which call is `True`'''
        with self._sync as sync:
            sync(ct.filter(self._call, sync.iterable))
        return self

    _ofilter = filter

    def find(self):
        '''first incoming thing for which call is `True`'''
        with self._sync as sync:
            sync(find(self._call, self.incoming))
        return self

    _ofind = find

    def partition(self):
        '''
        split incoming things into `True` and `False` things based on results
        of callable

        @param test: a test
        '''
        with self._sync as sync:
            call = self._call
            falsy, truey = tee(sync.iterable)
            sync(iter(
                [list(ct.filterfalse(call, falsy)),
                list(ct.filter(call, truey))]),
            )
        return self

    _opartition = partition

    def reject(self):
        '''incoming things for which call is `False`'''
        with self._sync as sync:
            sync(ct.filterfalse(self._call, sync.iterable))
        return self

    _oreject = reject

    def without(self, *things):
        '''strip things from incoming things'''
        with self._sync as sync:
            sync(ct.filterfalse(lambda x: x in things, sync.iterable))
        return self

    _owithout = without