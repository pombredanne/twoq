# -*- coding: utf-8 -*-
'''twoq mapping mixins'''

import time
from copy import deepcopy
from threading import local

from twoq.support import lazier

__all__ = ('DelayMixin', 'RepeatMixin', 'MapMixin', 'MappingMixin')


class DelayMixin(local):

    '''delayed map mixin'''

    _sleep = lazier(time.sleep)

    @classmethod
    def _delay_each(cls, x, y, wait=0, caller=None):
        '''
        invoke `caller` with passed arguments, keywords after a delay

        @param x: positional arguments
        @param y: keywork arguments
        @param wait: time in seconds to delay (default: 0)
        @param caller: a callable (default: None)
        '''
        cls._sleep(wait)
        return caller(*x, **y)

    @classmethod
    def _delay_invoke(cls, x, wait=0, caller=None):
        '''
        invoke method on object after a delay but return object instead of call
        result if the call returns None

        @param x: some thing
        @param wait: time in seconds to delay (default: 0)
        @param caller: a callable (default: None)
        '''
        cls._sleep(wait)
        results = caller(x)
        return x if results is None else results

    @classmethod
    def _delay_map(cls, x, wait=None, caller=None):
        '''
        invoke call on thing after a delay

        @param wait: time in seconds to delay (default: 0)
        @param caller: a callable (default: None)
        '''
        cls._sleep(wait)
        return caller(x)

    def delay_each(self, wait):
        '''
        invoke call with passed arguments, keywords in incoming things after
        delay `wait`

        @param wait: time in seconds
        '''
        return self._xinstarmap(self._partial(
            self._delay_each, wait=wait, caller=self._call
        ))

    def delay_invoke(self, name, wait):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords after delay `wait` but return incoming thing instead if method
        returns `None`

        @param name: name of method
        @param wait: time in seconds
        '''
        return self._xinmap(self._partial(
            self._delay_invoke,
            wait=wait,
            caller=self._methodcaller(name, *self._args, **self._kw),
        ))

    def delay_map(self, wait):
        '''
        invoke call on each incoming thing after delay `wait`

        @param wait: time in seconds
        '''
        return self._xinmap(self._partial(
            self._delay_map, wait=wait, caller=self._call
        ))


class RepeatMixin(local):

    '''repetition mixin'''

    def copy(self):
        '''copy each incoming thing'''
        return self._xinmap(deepcopy)

    def padnone(self):
        '''repeat incoming things and then `None` indefinitely'''
        return self._pre()._iter(
            self._join(self._iterable, self._repeat(None),
        ))

    def range(self, start, stop=0, step=1):
        '''
        put sequence of numbers in incoming things

        @param start: number to start with
        @param stop: number to stop with (default: 0)
        @param step: number of steps to advance per iteration (default: 1)
        '''
        return self._pxtend(
            self._range(start, stop, step) if stop else self._range(start)
        )

    def repeat(self, n):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        return self._inxtend(lambda x: self._repeat(tuple(x), n))

    def times(self, n=None):
        '''
        repeat call with incoming things `n` times

        @param n: repeat call n times on incoming things (default: None)
        '''
        if n is None:
            return self._x2starmap(
                self._call, lambda x: self._repeat(self._list(x)),
            )
        return self._x2starmap(
            self._call, lambda x: self._repeat(self._list(x), n),
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

    def map(self):
        '''invoke call on each incoming thing'''
        return self._xinmap(self._call)

    def invoke(self, name):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords but return incoming thing instead if method returns `None`

        @param name: name of method
        '''
        return self._xinmap(self._partial(
            self._invoke,
            caller=self._methodcaller(name, *self._args, **self._kw),
        ))

    def each(self):
        '''invoke call with passed arguments, keywords in incoming things'''
        return self._xinstarmap(lambda x, y: self._call(*x, **y))

    def starmap(self):
        '''invoke call on each sequence of incoming things'''
        return self._xinstarmap(self._call)

    def items(self):
        '''invoke call on each mapping to get key, value pairs'''
        return self._pre()._xstarmap(
            self._call, self._ichain(self._inmap(self._items)),
        )


class MappingMixin(DelayMixin, RepeatMixin, MapMixin):

    '''mapping mixin'''
