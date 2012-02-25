# -*- coding: utf-8 -*-
'''twoq support'''

from stuf import six
# pylint: disable-msg=f0401,w0611
from stuf.six.moves import (
    map, filterfalse, filter, zip, zip_longest, xrange)  # @UnresolvedImport @UnusedImport @IgnorePep8
# pylint: enable-msg=f0401

__all__ = ['port', 'iterexcerpt']
items = six.items


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


import sys
if not sys.version_info[0] == 2 and sys.version_info[1] < 7:
    from collections import Counter  # @UnresolvedImport
else:
    import heapq
    from collections import Mapping
    from operator import itemgetter
    from itertools import chain, repeat, starmap

    class Counter(dict):

        '''dict subclass for counting hashable items'''

        def __init__(self, iterable=None, **kwds):
            '''
            If given, count elements from an input iterable. Or, initialize
            count from another mapping of elements to their counts.
            '''
            super(Counter, self).__init__()
            self.update(iterable, **kwds)

        def __missing__(self, key):
            '''count of elements not in the Counter is zero'''
            # Needed so that self[missing_item] does not raise KeyError
            return 0

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

        def elements(self):
            '''
            Iterator over elements repeating each as many times as its count
            '''
            return chain.from_iterable(starmap(repeat, self.iteritems()))

        # Override dict methods where necessary

        @classmethod
        def fromkeys(cls, iterable, v=None):
            raise NotImplementedError(
                'Counter.fromkeys() is undefined.'
                'Use Counter(iterable) instead.'
            )

        def update(self, iterable=None, **kwds):
            '''like dict.update() but add counts instead of replacing them'''
            if iterable is not None:
                if isinstance(iterable, Mapping):
                    if self:
                        self_get = self.get
                        for elem, count in items(iterable):
                            self[elem] = self_get(elem, 0) + count
                    else:
                        # fast path when counter is empty
                        super(Counter, self).update(iterable)
                else:
                    self_get = self.get
                    for elem in iterable:
                        self[elem] = self_get(elem, 0) + 1
            if kwds:
                self.update(kwds)

        def subtract(self, iterable=None, **kwds):
            '''
            like dict.update() but subtracts counts instead of replacing them.

            Counts can be reduced below zero. Both the inputs and outputs are
            allowed to contain zero and negative counts.
            '''
            if iterable is not None:
                self_get = self.get
                if isinstance(iterable, Mapping):
                    for elem, count in items(iterable):
                        self[elem] = self_get(elem, 0) - count
                else:
                    for elem in iterable:
                        self[elem] = self_get(elem, 0) - 1
            if kwds:
                self.subtract(kwds)

        def copy(self):
            '''return a shallow copy'''
            return self.__class__(self)

        def __reduce__(self):
            return self.__class__, (dict(self),)

        def __delitem__(self, elem):
            '''
            like dict.__delitem__() but does not raise KeyError for missing
            values
            '''
            if elem in self:
                super(Counter, self).__delitem__(elem)

        def __repr__(self):
            if not self:
                return '%s()' % self.__class__.__name__
            items = ', '.join(map('%r: %r'.__mod__, self.most_common()))
            return '%s({%s})' % (self.__class__.__name__, items)

        def __add__(self, other):
            '''add counts from two counters'''
            if not isinstance(other, Counter):
                return NotImplemented
            result = Counter()
            for elem, count in items(self):
                newcount = count + other[elem]
                if newcount > 0:
                    result[elem] = newcount
            for elem, count in items(other):
                if elem not in self and count > 0:
                    result[elem] = count
            return result

        def __sub__(self, other):
            '''subtract count, but keep only results with positive counts'''
            if not isinstance(other, Counter):
                return NotImplemented
            result = Counter()
            for elem, count in items(self):
                newcount = count - other[elem]
                if newcount > 0:
                    result[elem] = newcount
            for elem, count in items(other):
                if elem not in self and count < 0:
                    result[elem] = 0 - count
            return result

        def __or__(self, other):
            '''union is the maximum of value in either of the input counters'''
            if not isinstance(other, Counter):
                return NotImplemented
            result = Counter()
            for elem, count in items(self):
                other_count = other[elem]
                newcount = other_count if count < other_count else count
                if newcount > 0:
                    result[elem] = newcount
            for elem, count in items(other):
                if elem not in self and count > 0:
                    result[elem] = count
            return result

        def __and__(self, other):
            '''intersection is the minimum of corresponding counts'''
            if not isinstance(other, Counter):
                return NotImplemented
            result = Counter()
            for elem, count in items(self):
                other_count = other[elem]
                newcount = count if count < other_count else other_count
                if newcount > 0:
                    result[elem] = newcount
            return result
