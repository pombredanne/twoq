# -*- coding: utf-8 -*-
'''python compatibility layer'''

from stuf import six
# pylint: disable-msg=f0401,w0611
from stuf.six.moves import map, filterfalse, filter, zip, zip_longest  # @UnresolvedImport @UnusedImport @IgnorePep8
# pylint: enable-msg=f0401

__all__ = ['port']


class port(object):

    '''python 2/3 helper'''

    # is python 3?
    PY3 = six.PY3
    # types
    BINARY = six.binary_type
    CLASS = six.class_types
    INTEGER = six.integer_types
    MAXSIZE = six.MAXSIZE
    STRING = six.string_types
    UNICODE = six.text_type
    # classes
    BytesIO = six.BytesIO
    StringIO = six.StringIO
    # character data
    b = staticmethod(six.b)
    int2byte = staticmethod(six.int2byte)
    u = staticmethod(six.u)
    # dictionary
    items = staticmethod(six.iteritems)
    keys = staticmethod(six.iterkeys)
    values = staticmethod(six.itervalues)
    # iterables
    iterator = staticmethod(six.advance_iterator)
    # classes
    metaclass = staticmethod(six.with_metaclass)
    # methods
    code = staticmethod(six.get_function_code)
    defaults = staticmethod(six.get_function_defaults)
    method_function = staticmethod(six.get_method_function)
    method_self = staticmethod(six.get_method_self)
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
    def printit(*args, **kw):
        '''print output'''
        return six.print_(*args, **kw)
