# -*- coding: utf-8 -*-
'''twoq mapping mixins'''

import time
from threading import local
from functools import partial
from copy import deepcopy
from operator import methodcaller
from itertools import starmap, chain, repeat

from stuf.six import items
from stuf.utils import imap
from twoq.support import chain_iter, range

__all__ = ('DelayMixin', 'RepeatMixin', 'MapMixin', 'MappingMixin')


class DelayMixin(local):

    '''delayed map mixin'''

    @staticmethod
    def _delay_each(x, y, wait=0, caller=None):
        '''
        invoke `caller` with passed arguments, keywords after a delay

        @param x: positional arguments
        @param y: keywork arguments
        @param wait: time in seconds to delay (default: 0)
        @param caller: a callable (default: None)
        '''
        time.sleep(wait)
        return caller(*x, **y)

    @staticmethod
    def _delay_invoke(x, wait=0, caller=None):
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

    @staticmethod
    def _delay_map(x, wait=None, caller=None):
        '''
        invoke call on thing after a delay

        @param wait: time in seconds to delay (default: 0)
        @param caller: a callable (default: None)
        '''
        time.sleep(wait)
        return caller(x)

    def delay_each(self, wait):
        '''
        invoke call with passed arguments, keywords in incoming things after
        delay `wait`

        @param wait: time in seconds
        '''
        _delay = partial(self._delay_each, wait=wait, caller=self._call)
        return self._extend(starmap(_delay, self._iterable))

    def delay_invoke(self, name, wait):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords after delay `wait` but return incoming thing instead if method
        returns `None`

        @param name: name of method
        @param wait: time in seconds
        '''
        _call = partial(
            self._delay_invoke,
            wait=wait,
            caller=methodcaller(name, *self._args, **self._kw),
        )
        return self._extend(imap(_call, self._iterable))

    def delay_map(self, wait):
        '''
        invoke call on each incoming thing after delay `wait`

        @param wait: time in seconds
        '''
        call_ = partial(self._delay_map, wait=wait, caller=self._call)
        return self._extend(imap(call_, self._iterable))


class RepeatMixin(local):

    '''repetition mixin'''

    def copy(self):
        '''copy each incoming thing'''
        return self._extend(imap(deepcopy, self._iterable))

    def padnone(self):
        '''incoming things and then `None` indefinitely'''
        return self._extend.iter(chain(self._iterable, repeat(None)))

    def range(self, start, stop=0, step=1):
        '''
        put sequence of numbers in incoming things

        @param start: number to start with
        @param stop: number to stop with (default: 0)
        @param step: number of steps to advance per iteration (default: 1)
        '''
        return self._extend(range(start, stop, step) if stop else range(start))

    def repeat(self, n):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        return self._extend(repeat(tuple(self._iterable), n))

    def times(self, n=None):
        '''
        repeat call with incoming things `n` times

        @param n: repeat call n times on incoming things (default: None)
        '''
        if n is None:
            return self._extend(starmap(
                self._call, repeat(list(self._iterable))
            ))
        return self._extend(
            starmap(self._call, repeat(list(self._iterable), n))
        )


class MapMixin(local):

    '''mapping mixin'''

    @staticmethod
    def _invoke(thing, caller=None):
        '''
        invoke method on object but return object instead of call result if the
        call returns None

        @param thing: some thing
        @param caller: a callable (default: None)
        '''
        results = caller(thing)
        return thing if results is None else results

    def each(self):
        '''invoke call with passed arguments, keywords in incoming things'''
        filt_ = lambda x, y: self._call(*x, **y)
        return self._extend(starmap(filt_, self._iterable))

    def invoke(self, name):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords but return incoming thing instead if method returns `None`

        @param name: name of method
        '''
        call_ = partial(
            self._invoke, caller=methodcaller(name, *self._args, **self._kw),
        )
        return self._extend(imap(call_, self._iterable))

    def items(self):
        '''invoke call on each mapping to get key, value pairs'''
        return self._extend(starmap(
            self._call, chain_iter(imap(items, self._iterable))
        ))

    def map(self):
        '''invoke call on each incoming thing'''
        return self._extend(imap(self._call, self._iterable))

    def starmap(self):
        '''invoke call on each sequence of incoming things'''
        return self._extend(starmap(self._call, self._iterable))


class MappingMixin(DelayMixin, RepeatMixin, MapMixin):

    '''mapping mixin'''
