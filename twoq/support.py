# -*- coding: utf-8 -*-
'''twoq utils'''

__all__ = ['iterexcept']

from functools import partial
from collections import Iterable
from itertools import islice, cycle
from operator import itemgetter, attrgetter

from twoq.compat import port, filter as ifilter, filterfalse


def find(call, incoming, _filter=ifilter):
    for thing in _filter(call, incoming):
        yield thing
        break


def iterexcept(func, exception):
    '''
    call a function repeatedly until an exception is raised

    Converts a call-until-exception interface to an iterator interface. Like
    `__builtin__.iter(func, sentinel)` but uses an exception instead of a
    sentinel to end the loop.
    '''
    try:
        while 1:
            yield func()
    except exception:
        pass


def members(this, call=None, _filter=ifilter, _get=getattr):
    '''collect members of incoming things'''
    for key in _filter(call, dir(this)):
        try:
            thing = _get(this, key)
        except AttributeError:
            pass
        else:
            yield key, thing


def pick(names, iterable, _attrgetter=attrgetter):
    attrfind = _attrgetter(*names)
    for thing in iterable:
        try:
            yield attrfind(thing)
        except AttributeError:
            pass


def pluck(keys, iterable, _itemgetter=itemgetter):
    itemfind = _itemgetter(*keys)
    for thing in iterable:
        try:
            yield itemfind(thing)
        except (IndexError, KeyError, TypeError):
            pass


def roundrobin(iterable, _s=islice, _c=cycle, _p=partial, _i=iter, _n=next):
    pending = len(iterable)
    nexts = _c(_p(_n, _i(i)) for i in iterable)
    while pending:
        try:
            for n in nexts:
                yield n()
        except StopIteration:
            pending -= 1
            nexts = _c(_s(nexts, pending))


def smash(iterable, _isstring=port.isstring, _Iterable=Iterable):
    for i in iterable:
        if isinstance(i, _Iterable) and not _isstring(i):
            for j in smash(i):
                yield j
        else:
            yield i


def unique(iterable, key=None, _ff=filterfalse, _set=set):
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
