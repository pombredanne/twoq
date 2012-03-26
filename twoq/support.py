# -*- coding: utf-8 -*-
'''twoq support'''

from threading import Lock
from itertools import chain
from functools import wraps
from collections import namedtuple

from stuf import six
from stuf.utils import lazy_class
# pylint: disable-msg=f0401,w0611
from stuf.six.moves import (
    map, filterfalse, filter, zip, zip_longest, xrange)  # @UnresolvedImport @UnusedImport @IgnorePep8
# pylint: enable-msg=f0401

__all__ = ['port']
items = six.items
ichain = chain.from_iterable
range = xrange
imap = map
ifilter = filter


class lazier(lazy_class):

    def __init__(self, method):
        super(lazier, self).__init__(lambda x: method)


class port(object):

    '''python 2/3 helper'''

    # is python 3?
    PY3 = six.PY3
    # types
    BINARY = six.binaries
    CLASS = six.classes
    INTEGER = six.integers
    MAXSIZE = six.MAXSIZE
    STRING = six.strings
    UNICODE = six.texts
    # classes
    BytesIO = six.BytesIO
    StringIO = six.StringIO
    # character data
    b = staticmethod(six.b)
    int2byte = staticmethod(six.int2byte)
    u = staticmethod(six.u)
    # dictionary
    items = staticmethod(six.items)
    keys = staticmethod(six.keys)
    values = staticmethod(six.values)
    # iterables
    iterator = staticmethod(six.advance_iterator)
    # classes
    metaclass = staticmethod(six.with_metaclass)
    # methods
    code = staticmethod(six.function_code)
    defaults = staticmethod(six.function_defaults)
    method_function = staticmethod(six.method_function)
    method_self = staticmethod(six.method_self)
    unbound = staticmethod(six.get_unbound_function)
    # exception
    reraise = staticmethod(six.reraise)

    @classmethod
    def isbinary(cls, value):
        '''is binary?'''
        return isinstance(value, cls.BINARY)

    @classmethod
    def isclass(cls, value):
        '''is class?'''
        return isinstance(value, cls.CLASS)

    @classmethod
    def iscall(cls, value):
        '''is callable?'''
        return six.callable(value)

    @classmethod
    def isgtemax(cls, value):
        '''greater than max size?'''
        return value > cls.MAXSIZE

    @classmethod
    def isinteger(cls, value):
        '''is integer?'''
        return isinstance(value, cls.INTEGER)

    @classmethod
    def isltemax(cls, value):
        '''less than max size?'''
        return value < cls.MAXSIZE

    @classmethod
    def isstring(cls, value):
        '''is string'''
        return isinstance(value, cls.STRING)

    @classmethod
    def isunicode(cls, value):
        '''is text?'''
        return isinstance(value, cls.UNICODE)

    @staticmethod
    def printf(*args, **kw):
        '''print output'''
        return six.printf(*args, **kw)


isstring = port.isstring
isunicode = port.isunicode


import sys
if not sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from collections import Counter  # @UnresolvedImport
else:
    import heapq
    from operator import itemgetter

    class Counter(dict):

        '''dict subclass for counting hashable items'''

        def __init__(self, iterable=None, **kw):
            '''
            If given, count elements from an input iterable. Or, initialize
            count from another mapping of elements to their counts.
            '''
            super(Counter, self).__init__()
            self.update(iterable, **kw)

        def most_common(self, n=None):
            '''
            list the n most common elements and their counts from the most
            common to the least

            If n is None, then list all element counts.
            '''
            # Emulate Bag.sortedByCount from Smalltalk
            if n is None:
                return sorted(items(self), key=itemgetter(1), reverse=True)
            return heapq.nlargest(n, self.iteritems(), key=itemgetter(1))

        # Override dict methods where necessary

        def update(self, iterable=None, **kw):
            '''like dict.update() but add counts instead of replacing them'''
            if iterable is not None:
                self_get = self.get
                for elem in iterable:
                    self[elem] = self_get(elem, 0) + 1


_CacheInfo = namedtuple('CacheInfo', ['hits', 'misses', 'maxsize', 'currsize'])


def lru_cache(maxsize=100, typed=False):
    '''
    least-recently-used cache decorator.

    If *maxsize* is set to None, the LRU features are disabled and the cache
    can grow without bound.

    If *typed* is True, arguments of different types will be cached separately.
    For example, f(3.0) and f(3) will be treated as distinct calls with
    distinct results.

    Arguments to the cached function must be hashable.

    View the cache statistics named tuple (hits, misses, maxsize, currsize)
    with f.cache_info().  Clear the cache and statistics with f.cache_clear().
    Access the underlying function with f.__wrapped__.

    See:  http://en.wikipedia.org/wiki/Cache_algorithms#Least_Recently_Used
    '''
    # Users should only access the lru_cache through its public API:
    #       cache_info, cache_clear, and f.__wrapped__
    # The internals of the lru_cache are encapsulated for thread safety and
    # to allow the implementation to change (including a possible C version).

    def decorating_function(user_function):
        cache = dict()
        stats = [0, 0]
        # names for the stats fields
        HITS, MISSES = 0, 1
        # bound method to lookup key or return None
        cache_get = cache.get
        # localize the global len() function
        _len = len
        # separate positional and keyword args
        kwd_mark = (object(),)
        # because linkedlist updates aren't threadsafe
        lock = Lock()
        # root of the circular doubly linked list
        root = []
        # initialize by pointing to self
        root[:] = [root, root, None, None]
        # names for the link fields
        PREV, NEXT, KEY, RESULT = 0, 1, 2, 3

        def make_key(args, kwds, typed, tuple=tuple, sorted=sorted, type=type):
            key = args
            if kwds:
                sorted_items = tuple(sorted(kwds.items()))
                key += kwd_mark + sorted_items
            if typed:
                key += tuple(type(v) for v in args)
                if kwds:
                    key += tuple(type(v) for _, v in sorted_items)
            return key

        if maxsize is None:

            @wraps(user_function)
            def wrapper(*args, **kwds):
                # simple caching without ordering or size limit
                key = make_key(args, kwds, typed) if kwds or typed else args
                # root used here as a unique not-found sentinel
                result = cache_get(key, root)
                if result is not root:
                    stats[HITS] += 1
                    return result
                result = user_function(*args, **kwds)
                cache[key] = result
                stats[MISSES] += 1
                return result
        else:

            @wraps(user_function)
            def wrapper(*args, **kwds):
                # size limited caching that tracks accesses by recency
                key = make_key(args, kwds, typed) if kwds or typed else args
                with lock:
                    link = cache_get(key)
                    if link is not None:
                        # record recent use of the key by moving it to the
                        # front of the list
                        link_prev, link_next, key, result = link
                        link_prev[NEXT] = link_next
                        link_next[PREV] = link_prev
                        last = root[PREV]
                        last[NEXT] = root[PREV] = link
                        link[PREV] = last
                        link[NEXT] = root
                        stats[HITS] += 1
                        return result
                result = user_function(*args, **kwds)
                with lock:
                    last = root[PREV]
                    link = [last, root, key, result]
                    cache[key] = last[NEXT] = root[PREV] = link
                    if _len(cache) > maxsize:
                        # purge least recently used cache entry
                        _, old_next, old_key, _ = root[NEXT]
                        root[NEXT] = old_next
                        old_next[PREV] = root
                        del cache[old_key]
                    stats[MISSES] += 1
                return result

        def cache_info():
            '''Report cache statistics'''
            with lock:
                return _CacheInfo(
                    stats[HITS], stats[MISSES], maxsize, len(cache)
                )

        def cache_clear():
            '''Clear the cache and cache statistics'''
            with lock:
                cache.clear()
                root[:] = [root, root, None, None]
                stats[:] = [0, 0]

        wrapper.__wrapped__ = user_function
        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return wrapper
    return decorating_function
