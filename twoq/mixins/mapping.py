# -*- coding: utf-8 -*-
'''twoq mapping mixins'''

import time

import copy as cp
import itertools as it
from threading import local
from functools import partial
from operator import methodcaller as mc

from twoq import support as ct
from twoq.support import port

__all__ = (
    'DelayMixin', 'CopyMixin', 'MappingMixin', 'RepeatMixin', 'MapMixin',
)
chain_iter = it.chain.from_iterable

###############################################################################
## mapping subroutines ########################################################
###############################################################################


def invoke(thing, caller=None): #@IgnorePep8
    '''
    invoke method on object but return object instead of call result if the
    call returns None

    @param thing: some thing
    @param caller: a callable (default: None)
    '''
    results = caller(thing)
    return thing if results is None else results


def delay_each(x, y, wait=0, caller=None, _sleep=time.sleep):
    '''
    invoke `caller` with passed arguments, keywords after a delay

    @param x: positional arguments
    @param y: keywork arguments
    @param wait: time in seconds to delay (default: 0)
    @param caller: a callable (default: None)
    '''
    _sleep(wait)
    return caller(*x, **y)


def delay_invoke(x, wait=0, caller=None, _sleep=time.sleep): #@IgnorePep8
    '''
    invoke method on object after a delay but return object instead of call
    result if the call returns None

    @param x: some thing
    @param wait: time in seconds to delay (default: 0)
    @param caller: a callable (default: None)
    '''
    _sleep(wait)
    results = caller(x)
    return x if results is None else results


def delay_map(x, wait=None, caller=None, _sleep=time.sleep):
    '''
    invoke call on thing after a delay

    @param wait: time in seconds to delay (default: 0)
    @param caller: a callable (default: None)
    '''
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

    _odelay_each = delay_each

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

    _odelay_invoke = delay_invoke

    def delay_map(self, wait, _delay_map=delay_map, _map=ct.map):
        '''
        invoke call on each incoming thing after a delay

        @param wait: time in seconds
        '''
        _call = partial(_delay_map, wait=wait, caller=self._call)
        with self._sync as sync:
            sync(_map(_call, sync.iterable))
        return self

    _odelay_map = delay_map


class CopyMixin(local):

    '''duplication mixin'''

    def copy(self, _map=ct.map, _copy=cp.copy):
        '''copy each incoming thing'''
        with self._sync as sync:
            sync(_map(_copy, sync.iterable))
        return self

    _ocopy = copy

    def deepcopy(self, _map=ct.map, _deepcopy=cp.deepcopy):
        '''copy each incoming thing deeply'''
        with self._sync as sync:
            sync(_map(_deepcopy, sync.iterable))
        return self

    _odeepcopy = deepcopy


class MappingMixin(local):

    '''map mixin'''

    def each(self, _map=it.starmap):
        '''invoke call with passed arguments, keywords in incoming things'''
        with self._sync as sync:
            sync(_map(lambda x, y: self._call(*x, **y), sync.iterable))
        return self

    _oeach = each

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

    _oinvoke = invoke

    def items(self, _s=it.starmap, _c=chain_iter, _m=ct.map, _i=port.items):
        '''invoke call on each mapping to get key, value pairs'''
        with self._sync as sync:
            sync(_s(self._call, _c(_m(_i, sync.iterable))))
        return self

    _ostarmap = items

    def map(self, _map=ct.map):
        '''invoke call on each incoming thing'''
        with self._sync as sync:
            sync(_map(self._call, sync.iterable))
        return self

    _omap = map

    def starmap(self, _map=it.starmap):
        '''invoke call on each incoming pair of things'''
        with self._sync as sync:
            sync(_map(self._call, sync.iterable))
        return self

    _ostarmap = starmap


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

    _opadnone = padnone

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

    _orange = range

    def repeat(self, n, _repeat=it.repeat, _tuple=tuple):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        with self._sync as sync:
            sync(_repeat(_tuple(sync.iterable), n))
        return self

    _orepeat = repeat

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

    _otimes = times


class MapMixin(DelayMixin, CopyMixin, MappingMixin, RepeatMixin):

    '''mapping mixin'''
