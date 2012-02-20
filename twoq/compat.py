# -*- coding: utf-8 -*-
'''base compatibility layer'''

from stuf import six

__all__ = ['Port']


class Port(object):

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
    b = six.b
    int2byte = six.int2byte
    u = six.u
    # dictionary
    items = six.iteritems
    keys = six.iterkeys
    values = six.itervalues
    # iterables
    iterator = six.advance_iterator
    # classes
    metaclass = six.with_metaclass
    # methods
    code = six.get_function_code
    defaults = six.get_function_defaults
    method_function = six.get_method_function
    method_self = six.get_method_self
    unbound = six.get_unbound_function
    # exception
    reraise = six.reraise

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
