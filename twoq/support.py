# -*- coding: utf-8 -*-
'''twoq support'''

from stuf import six
# pylint: disable-msg=f0401,w0611
from stuf.six.moves import (
    map, filterfalse, filter, zip, zip_longest, xrange)  # @UnresolvedImport @UnusedImport @IgnorePep8
# pylint: enable-msg=f0401

__all__ = ['port', 'iterexcerpt']


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
