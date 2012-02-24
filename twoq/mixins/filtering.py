# -*- coding: utf-8 -*-
'''twoq filtering mixins'''

import operator as op
import itertools as it
import functools as ft
from threading import local

from stuf.utils import getcls

from twoq import support as ct

__all__ = (
    'FilteringMixin', 'FilterMixin', 'CollectMixin', 'SetMixin', 'SliceMixin'
)
chain_iter = it.chain.from_iterable

###############################################################################
## filtering subroutines ######################################################
###############################################################################


def find(call, iterable, _filter=ct.filter):
    '''
    find the first `True` thing in iterator

    @param call: "Truth" filter
    @param iterable: an iterable
    '''
    for thing in _filter(call, iterable):
        yield thing
        break


def members(iterable, _get=getattr):
    '''
    collect members of things

    @param thing: an iterable
    '''
    for key in dir(iterable):
        try:
            thing = _get(iterable, key)
        except AttributeError:
            pass
        else:
            yield key, thing


def memberfilter(call, iterable, _members=members, _filter=ct.filter):
    '''
    filter members of things

    @param call: "Truth" filter
    @param iterable: an iterable
    '''
    for i in _filter(call, _members(iterable)):
        yield i


def pick(names, iterable, _attrgetter=op.attrgetter):
    '''
    collect attributes of things in iterable

    @param names: sequence of names
    @param iterable: an iterable
    '''
    attrfind = _attrgetter(*names)
    for thing in iterable:
        try:
            yield attrfind(thing)
        except AttributeError:
            pass


def pluck(keys, iterable, _itemgetter=op.itemgetter):
    '''
    collect values of things in iterable

    @param keys: sequence of keys
    @param iterable: an iterable
    '''
    itemfind = _itemgetter(*keys)
    for thing in iterable:
        try:
            yield itemfind(thing)
        except (IndexError, KeyError, TypeError):
            pass


def unique(iterable, key=None, _ff=ct.filterfalse, _set=set):
    '''
    unique things in in iterable

    @param iterable: an iterable
    @param key: determine uniqueness filter
    '''
    seen = _set()
    seen_add = seen.add
    if key is None:
        for element in _ff(seen.__contains__, iterable):
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


class FilteringMixin(local):

    '''filter mixin'''

    def compact(self, _filter=ct.filter, _truth=op.truth):
        '''strip "untrue" things from incoming things'''
        with self._sync as sync:
            sync.iter(_filter(_truth, sync.iterable))
        return self

    _ocompact = compact

    def filter(self, _filter=ct.filter):
        '''incoming things for which call is `True`'''
        with self._sync as sync:
            sync(_filter(self._call, sync.iterable))
        return self

    _ofilter = filter

    def find(self, _find=find):
        '''first incoming thing for which call is `True`'''
        with self._sync as sync:
            sync(_find(self._call, self.incoming))
        return self

    _ofind = find

    def partition(self, _t=it.tee, _ff=ct.filterfalse, _filter=ct.filter):
        '''
        split incoming things into `True` and `False` things based on results
        of callable

        @param test: a test
        '''
        with self._sync as sync:
            call = self._call
            falsy, truey = _t(sync.iterable)
            sync.append(list(_ff(call, falsy)))
            sync.append(list(_filter(call, truey)))
        return self

    _opartition = partition

    def reject(self, _filterfalse=ct.filterfalse):
        '''incoming things for which call is `False`'''
        with self._sync as sync:
            sync(_filterfalse(self._call, sync.iterable))
        return self

    _oreject = reject

    def without(self, *things):
        '''strip things from incoming things'''
        with self._sync as sync:
            sync(ct.filterfalse(lambda x: x in things, sync.iterable))
        return self
    
    _owithout = without


class CollectMixin(local):

    '''gathering mixin'''
    
    def deepmembers(self, mz=memberfilter, ci=chain_iter, gc=getcls):
        '''collect members of incoming things and their bases'''
        _mz = ft.partial(mz, self._call)
        with self._sync as sync:
            def _memfilters(thing, mz=_mz, gc=gc):
                return ci(ct.map(mz, ci([type.mro(gc(thing)), [thing]])))
            sync(ci(ct.map(_memfilters, sync.iterable)))
        return self

    _odeepmembers = deepmembers

    def members(self, _mz=memberfilter, _ci=it.chain.from_iterable):
        '''collect members of incoming things'''
        _mz = ft.partial(_mz, self._call)
        with self._sync as sync:
            sync(_ci(ct.map(_mz, sync.iterable)))
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

    def difference(self, _reduce=ft.reduce, _set=set):
        '''difference between incoming things'''
        with self._sync as sync:
            sync(_reduce(
                lambda x, y: _set(x).difference(_set(y)), sync.iterable,
            ))
        return self
    
    _odifference = difference

    def intersection(self, _reduce=ft.reduce, _set=set):
        '''intersection between incoming things'''
        with self._sync as sync:
            sync(_reduce(
                lambda x, y: _set(x).intersection(_set(y)), sync.iterable,
            ))
        return self
    
    _ointersection = intersection

    def union(self, _reduce=ft.reduce, _set=set):
        '''union between incoming things'''
        with self._sync as sync:
            sync(_reduce(
                lambda x, y: _set(x).union(_set(y)), sync.iterable,
            ))
        return self
    
    _ounion = union

    def unique(self, _unique=unique):
        '''
        list unique incoming things, preserving order and remember all incoming
        things ever seen

        unique_everseen('AAAABBBCCDAABBB') --> A B C D
        unique_everseen('ABBCcAD', str.lower) --> A B C D
        '''
        with self._sync as sync:
            sync.iter(_unique(sync.iterable, self._call))
        return self
    
    _ounique = unique


class SliceMixin(local):

    '''slicing mixin'''

    def nth(self, n, default=None, _next=next, _islice=it.islice):
        '''
        nth incoming thing or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        with self._sync as sync:
            sync.append(_next(_islice(sync.iterable, n, None), default))
        return self
    
    _onth = nth

    def initial(self, _islice=it.islice, _len=len):
        '''all incoming things except the last thing'''
        with self._sync as sync:
            iterable = sync.iterable
            sync(_islice(iterable, _len(iterable) - 1))
        return self

    _oinitial = initial

    def rest(self, _islice=it.islice):
        '''all incoming things except the first thing'''
        with self._sync as sync:
            sync(_islice(sync.iterable, 1, None))
        return self
    
    _orest = rest

    def snatch(self, n, _islice=it.islice, _len=len):
        '''
        last `n` things of incoming things

        @param n: number of things
        '''
        with self._sync as sync:
            iterable = sync.iterable
            sync(_islice(iterable, _len(iterable) - n, None))
        return self

    _osnatch = snatch

    def take(self, n, _islice=it.islice):
        '''
        first `n` things of incoming things

        @param n: number of things
        '''
        with self._sync as sync:
            sync(_islice(sync.iterable, n))
        return self

    _otake = take


class FilterMixin(FilteringMixin, CollectMixin, SetMixin, SliceMixin):

    '''filters mixin'''
