# -*- coding: utf-8 -*-
'''twoq mapping mixins'''

import time
from threading import local
from functools import partial
from copy import copy, deepcopy
from operator import methodcaller
from itertools import starmap, chain, repeat

from stuf.six import items
from stuf.utils import imap
from twoq.support import range
from twoq.support import chain_iter

__all__ = (
    'DelayMixin', 'CopyMixin', 'RepeatMixin', 'MapMixin', 'MappingMixin',
)

###############################################################################
## mapping subroutines ########################################################
###############################################################################


def invoke(thing, caller=None):
    '''
    invoke method on object but return object instead of call result if the
    call returns None

    @param thing: some thing
    @param caller: a callable (default: None)
    '''
    results = caller(thing)
    return thing if results is None else results


def delay_each(x, y, wait=0, caller=None):
    '''
    invoke `caller` with passed arguments, keywords after a delay

    @param x: positional arguments
    @param y: keywork arguments
    @param wait: time in seconds to delay (default: 0)
    @param caller: a callable (default: None)
    '''
    time.sleep(wait)
    return caller(*x, **y)


def delay_invoke(x, wait=0, caller=None):
    '''
    invoke method on object after a delay but return object instead of call
    result if the call returns None

    @param x: some thing
    @param wait: time in seconds to delay (default: 0)
    @param caller: a callable (default: None)
    '''
    time.sleep(wait)
    results = caller(x)
    return x if results is None else results


def delay_map(x, wait=None, caller=None):
    '''
    invoke call on thing after a delay

    @param wait: time in seconds to delay (default: 0)
    @param caller: a callable (default: None)
    '''
    time.sleep(wait)
    return caller(x)


###############################################################################
## map mixins #################################################################
###############################################################################


class DelayMixin(local):

    '''delayed map mixin'''

    def delay_each(self, wait):
        '''
        invoke call with passed arguments, keywords in incoming things after
        delay `wait`

        @param wait: time in seconds
        '''
        _delay = partial(delay_each, wait=wait, caller=self._call)
        with self._sync as sync:
            sync(starmap(_delay, sync.iterable))
        return self

    _odelay_each = delay_each

    def delay_invoke(self, name, wait):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords after delay `wait` but return incoming thing instead if method
        returns `None`

        @param name: name of method
        @param wait: time in seconds
        '''
        _call = partial(
            delay_invoke,
            wait=wait,
            caller=methodcaller(name, *self._args, **self._kw),
        )
        with self._sync as sync:
            sync(imap(_call, sync.iterable))
        return self

    _odelay_invoke = delay_invoke

    def delay_map(self, wait):
        '''
        invoke call on each incoming thing after delay `wait`

        @param wait: time in seconds
        '''
        _call = partial(delay_map, wait=wait, caller=self._call)
        with self._sync as sync:
            sync(imap(_call, sync.iterable))
        return self

    _odelayimap = delay_map


class CopyMixin(local):

    '''copy mixin'''

    def copy(self):
        '''copy each incoming thing'''
        with self._sync as sync:
            sync(imap(copy, sync.iterable))
        return self

    _ocopy = copy

    def deepcopy(self):
        '''copy each incoming thing deeply'''
        with self._sync as sync:
            sync(imap(deepcopy, sync.iterable))
        return self

    _odeepcopy = deepcopy


class RepeatMixin(local):

    '''repetition mixin'''

    def padnone(self):
        '''incoming things and then `None` indefinitely'''
        with self._sync as sync:
            sync.iter(chain(sync.iterable, repeat(None)))
        return self

    _opadnone = padnone

    def range(self, start, stop=0, step=1):
        '''
        put sequence of numbers in incoming things

        @param start: number to start with
        @param stop: number to stop with (default: 0)
        @param step: number of steps to advance per iteration (default: 1)
        '''
        with self._sync as sync:
            if stop:
                sync(range(start, stop, step))
            else:
                sync(range(start))
        return self

    _orange = range

    def repeat(self, n):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        with self._sync as sync:
            sync(repeat(tuple(sync.iterable), n))
        return self

    _orepeat = repeat

    def times(self, n=None):
        '''
        repeat call with incoming things `n` times

        @param n: number of times to repeat calls with incoming things
            (default: None)
        '''
        call = self._call
        with self._sync as sync:
            if n is None:
                sync(starmap(call, repeat(list(sync.iterable))))
            else:
                sync(starmap(call, repeat(list(sync.iterable), n)))
        return self

    _otimes = times


class MapMixin(local):

    '''mapping mixin'''

    def each(self):
        '''invoke call with passed arguments, keywords in incoming things'''
        call = self._call
        with self._sync as sync:
            sync(starmap(lambda x, y: call(*x, **y), sync.iterable))
        return self

    _oeach = each

    def invoke(self, name):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords but return incoming thing instead if method returns `None`

        @param name: name of method
        '''
        _call = partial(
            invoke, caller=methodcaller(name, *self._args, **self._kw),
        )
        with self._sync as sync:
            sync(imap(_call, sync.iterable))
        return self

    _oinvoke = invoke

    def items(self):
        '''invoke call on each mapping to get key, value pairs'''
        call = self._call
        with self._sync as sync:
            sync(starmap(call, chain_iter(imap(items, sync.iterable))))
        return self

    _ostarmap = items

    def map(self):
        '''invoke call on each incoming thing'''
        call = self._call
        with self._sync as sync:
            sync(imap(call, sync.iterable))
        return self

    _omap = map

    def starmap(self):
        '''invoke call on each sequence of incoming things'''
        call = self._call
        with self._sync as sync:
            sync(starmap(call, sync.iterable))
        return self

    _ostarmap = starmap


class MappingMixin(DelayMixin, CopyMixin, RepeatMixin, MapMixin):

    '''mapping mixin'''
