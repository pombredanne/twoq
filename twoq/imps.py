# -*- coding: utf-8 -*-
'''twoq lookup mixins'''

import time
import operator
import itertools
import functools
from math import fsum
from threading import local
from random import choice, shuffle, sample

from twoq import support
from collections import deque
from operator import methodcaller
from stuf.utils import lazy, clsname, lazy_class


class lazier(lazy_class):

    def __init__(self, method):
        super(lazier, self).__init__(lambda x: method)


class LookupsMixin(local):

    '''lookup mixins'''

    _choice = lazier(choice)
    _clsname = lazier(clsname)
    _contains = lazier(operator.contains)
    _counter = lazier(support.Counter)
    _deek = lazier(deque)
    _filterfalse = lazier(support.filterfalse)
    _fsum = lazier(fsum)
    _groupby = lazier(itertools.groupby)
    _ichain = lazier(itertools.chain.from_iterable)
    _ifilter = lazier(support.ifilter)
    _imap = lazier(support.imap)
    _ireduce = lazier(functools.reduce)
    _islice = lazier(itertools.islice)
    _items = lazier(support.items)
    _join = lazier(itertools.chain)
    _methodcaller = lazier(methodcaller)
    _partial = lazier(functools.partial)
    _range = lazier(support.range)
    _repeat = lazier(itertools.repeat)
    _reversed = lazier(reversed)
    _sample = lazier(sample)
    _shuffle = lazier(shuffle)
    _sleep = lazier(time.sleep)
    _split = lazier(itertools.tee)
    _starmap = lazier(itertools.starmap)
    _truediv = lazier(operator.truediv)
    _zip = lazier(zip)

    @lazy
    def _getr(self):
        '''local getter'''
        return self._partial(local.__getattribute__, self)

    @lazy
    def _setr(self):
        '''local setter'''
        return self._partial(local.__setattr__, self)

    @lazy
    def _delr(self):
        '''local deleter'''
        return self._partial(local.__delattr__, self)
