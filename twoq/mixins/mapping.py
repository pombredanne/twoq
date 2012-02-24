# -*- coding: utf-8 -*-
'''twoq mapping mixins'''

import time

import copy as cp
import itertools as it
from threading import local
from functools import partial
from operator import methodcaller as mc

from twoq import support as ct

__all__ = (
    'DelayMixin', 'CopyMixin', 'MappingMixin', 'RepeatMixin', 'MapMixin',
)

###############################################################################
## mapping subroutines ########################################################
###############################################################################


def invoke(thing, caller=None): #@IgnorePep8
    results = caller(thing)
    return thing if results is None else results


def delay_each(x, y, wait=0, caller=None, _sleep=time.sleep):
    _sleep(wait)
    return caller(*x, **y)


def delay_invoke(x, wait=0, caller=None, _sleep=time.sleep): #@IgnorePep8
    _sleep(wait)
    results = caller(x)
    return x if results is None else results


def delay_map(x, wait=None, caller=None, _sleep=time.sleep):
    _sleep(wait)
    return caller(x)


###############################################################################
## map mixins #################################################################
###############################################################################


class DelayMixin(local):

    '''delayed map mixin'''

    def delay_each(self, wait, _map=it.starmap, _delay_each=delay_each):
        '''
        invoke call with passed arguments, keywords in incoming things after a
        delay

        @param wait: time in seconds
        '''
        _delay = partial(_delay_each, wait=wait, caller=self._call)
        with self._sync as sync:
            sync(_map(_delay, sync.iterable))
        return self

    def delay_invoke(self, name, wait, _mc=mc, _di=delay_invoke, _map=ct.map):
        '''
        invoke call on each incoming thing with passed arguments, keywords
        after a delay but return incoming thing instead if call returns None

        @param name: name of method
        @param wait: time in seconds
        '''
        _caller = _mc(name, *self._args, **self._kw)
        _call = partial(_di, wait=wait, caller=_caller)
        with self._sync as sync:
            sync(_map(_call, sync.iterable))
        return self

    def delay_map(self, wait, _delay_map=delay_map, _map=ct.map):
        '''
        invoke call on each incoming thing after a delay

        @param wait: time in seconds
        '''
        _call = partial(_delay_map, wait=wait, caller=self._call)
        with self._sync as sync:
            sync(_map(_call, sync.iterable))
        return self


class CopyMixin(local):

    '''duplication mixin'''

    def copy(self, _map=ct.map, _copy=cp.copy):
        '''copy each incoming thing'''
        with self._sync as sync:
            sync(_map(_copy, sync.iterable))
        return self

    def deepcopy(self, _map=ct.map, _deepcopy=cp.deepcopy):
        '''copy each incoming thing deeply'''
        with self._sync as sync:
            sync(_map(_deepcopy, sync.iterable))
        return self


class MappingMixin(local):

    '''map mixin'''

    def each(self, _map=it.starmap):
        '''invoke call with passed arguments, keywords in incoming things'''
        with self._sync as sync:
            sync(_map(lambda x, y: self._call(*x, **y), sync.iterable))
        return self

    def invoke(self, name, _mc=mc, _invoke=invoke, _map=ct.map):
        '''
        invoke call on each incoming thing with passed arguments, keywords
        but return incoming thing instead if call returns None

        @param name: name of method
        '''
        _caller = _mc(name, *self._args, **self._kw)
        _call = partial(_invoke, caller=_caller)
        with self._sync as sync:
            sync(_map(_call, sync.iterable))
        return self

    def map(self, _map=ct.map):
        '''invoke call on each incoming thing'''
        with self._sync as sync:
            sync(_map(self._call, sync.iterable))
        return self


class RepeatMixin(local):

    '''repetition mixin'''

    def padnone(self, _chain=it.chain, _repeat=it.repeat):
        '''
        incoming things and then `None` indefinitely

        (Useful for emulating the behavior of 2.x classic `builtin` `map`)
        '''
        with self._sync as sync:
            sync.iter(_chain(sync.iterable, _repeat(None)))
        return self

    def range(self, start, stop=0, step=1, _range=ct.xrange):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        with self._sync as sync:
            if stop:
                sync(_range(start, stop, step))
            else:
                sync(_range(start))
        return self

    def repeat(self, n, _repeat=it.repeat, _tuple=tuple):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        with self._sync as sync:
            sync(_repeat(_tuple(sync.iterable), n))
        return self

    def times(self, n=None, _starmap=it.starmap, _repeat=it.repeat):
        '''
        repeat call with passed arguments

        @param n: number of times to repeat calls (default: None)
        '''
        with self._sync as sync:
            if n is None:
                sync(_starmap(self._call, _repeat(sync.iterable)))
            else:
                sync(_starmap(self._call, _repeat(sync.iterable, n)))
        return self


class MapMixin(DelayMixin, CopyMixin, MappingMixin, RepeatMixin):

    '''mapping mixin'''
