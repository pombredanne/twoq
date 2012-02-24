# -*- coding: utf-8 -*-
'''twoq filtering mixins'''

import operator as op
import itertools as it
import functools as ft
from threading import local
from functools import partial

from twoq import support as ct

__all__ = (
    'FilteringMixin', 'FilterMixin', 'CollectMixin', 'SetMixin', 'SliceMixin'
)

###############################################################################
## filtering subroutines ######################################################
###############################################################################


def find(call, incoming, _filter=ct.filter):
    for thing in _filter(call, incoming):
        yield thing
        break


def members(this, call=None, _filter=ct.filter, _get=getattr):
    '''collect members of incoming things'''
    for key in _filter(call, dir(this)):
        try:
            thing = _get(this, key)
        except AttributeError:
            pass
        else:
            yield key, thing


def pick(names, iterable, _attrgetter=op.attrgetter):
    attrfind = _attrgetter(*names)
    for thing in iterable:
        try:
            yield attrfind(thing)
        except AttributeError:
            pass


def pluck(keys, iterable, _itemgetter=op.itemgetter):
    itemfind = _itemgetter(*keys)
    for thing in iterable:
        try:
            yield itemfind(thing)
        except (IndexError, KeyError, TypeError):
            pass


def unique(iterable, key=None, _ff=ct.filterfalse, _set=set):
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

    def filter(self, _filter=ct.filter):
        '''incoming things for which call is `True`'''
        with self._sync as sync:
            sync(_filter(self._call, sync.iterable))
        return self

    def find(self, _find=find):
        '''first incoming thing for which call is `True`'''
        with self._sync as sync:
            sync(_find(self._call, self.incoming))
        return self

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

    def reject(self, _filterfalse=ct.filterfalse):
        '''incoming things for which call is `False`'''
        with self._sync as sync:
            sync(_filterfalse(self._call, sync.iterable))
        return self

    def without(self, *things):
        '''strip things from incoming things'''
        with self._sync as sync:
            sync(ct.filterfalse(lambda x: x in things, sync.iterable))
        return self


class CollectMixin(local):

    '''gathering mixin'''

    def members(self, _mz=members, _map=ct.map, _ci=it.chain.from_iterable):
        '''collect members of incoming things'''
        _members = partial(_mz, call=self._call)
        with self._sync as sync:
            sync(_ci(_map(_members, sync.iterable)))
        return self

    def pick(self, *names):
        '''attributes of incoming things by attribute `*names`'''
        with self._sync as sync:
            sync(pick(names, sync.iterable))
        return self

    def pluck(self, *keys):
        '''items of incoming things by item `*keys`'''
        with self._sync as sync:
            sync(pluck(keys, sync.iterable))
        return self


class SetMixin(local):

    '''set and uniqueness mixin'''

    def difference(self, _reduce=ft.reduce, _set=set):
        '''difference between incoming things'''
        with self._sync as sync:
            sync(_reduce(
                lambda x, y: _set(x).difference(_set(y)), sync.iterable,
            ))
        return self

    def intersection(self, _reduce=ft.reduce, _set=set):
        '''intersection between incoming things'''
        with self._sync as sync:
            sync(_reduce(
                lambda x, y: _set(x).intersection(_set(y)), sync.iterable,
            ))
        return self

    def union(self, _reduce=ft.reduce, _set=set):
        '''union between incoming things'''
        with self._sync as sync:
            sync(_reduce(
                lambda x, y: _set(x).union(_set(y)), sync.iterable,
            ))
        return self

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

    def initial(self, _islice=it.islice, _len=len):
        '''all incoming things except the last thing'''
        with self._sync as sync:
            iterable = sync.iterable
            sync(_islice(iterable, _len(iterable) - 1))
        return self

    def rest(self, _islice=it.islice):
        '''all incoming things except the first thing'''
        with self._sync as sync:
            sync(_islice(sync.iterable, 1, None))
        return self

    def snatch(self, n, _islice=it.islice, _len=len):
        '''
        last `n` things of incoming things

        @param n: number of things
        '''
        with self._sync as sync:
            iterable = sync.iterable
            sync(_islice(iterable, _len(iterable) - n, None))
        return self

    def take(self, n, _islice=it.islice):
        '''
        first `n` things of incoming things

        @param n: number of things
        '''
        with self._sync as sync:
            sync(_islice(sync.iterable, n))
        return self


class FilterMixin(FilteringMixin, CollectMixin, SetMixin, SliceMixin):

    '''filters mixin'''
