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
        with self._sync as sync:
            sync(starmap(_delay, sync.iterable))
        return self

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
        with self._sync as sync:
            sync(imap(_call, sync.iterable))
        return self

    def delay_map(self, wait):
        '''
        invoke call on each incoming thing after delay `wait`

        @param wait: time in seconds
        '''
        call_ = partial(self._delay_map, wait=wait, caller=self._call)
        with self._sync as sync:
            sync(imap(call_, sync.iterable))
        return self


class RepeatMixin(local):

    '''repetition mixin'''

    def copy(self):
        '''copy each incoming thing'''
        with self._sync as sync:
            sync(imap(deepcopy, sync.iterable))
        return self

    def padnone(self):
        '''incoming things and then `None` indefinitely'''
        with self._sync as sync:
            sync.iter(chain(sync.iterable, repeat(None)))
        return self

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

    def repeat(self, n):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        with self._sync as sync:
            sync(repeat(tuple(sync.iterable), n))
        return self

    def times(self, n=None):
        '''
        repeat call with incoming things `n` times

        @param n: repeat call n times on incoming things (default: None)
        '''
        call_ = self._call
        with self._sync as sync:
            if n is None:
                sync(starmap(call_, repeat(list(sync.iterable))))
            else:
                sync(starmap(call_, repeat(list(sync.iterable), n)))
        return self


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
        call_ = self._call
        filt_ = lambda x, y: call_(*x, **y)
        with self._sync as sync:
            sync(starmap(filt_, sync.iterable))
        return self

    def invoke(self, name):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords but return incoming thing instead if method returns `None`

        @param name: name of method
        '''
        call_ = partial(
            self._invoke, caller=methodcaller(name, *self._args, **self._kw),
        )
        with self._sync as sync:
            sync(imap(call_, sync.iterable))
        return self

    def items(self):
        '''invoke call on each mapping to get key, value pairs'''
        call_ = self._call
        with self._sync as sync:
            sync(starmap(call_, chain_iter(imap(items, sync.iterable))))
        return self

    def map(self):
        '''invoke call on each incoming thing'''
        call_ = self._call
        with self._sync as sync:
            sync(imap(call_, sync.iterable))
        return self

    def starmap(self):
        '''invoke call on each sequence of incoming things'''
        call_ = self._call
        with self._sync as sync:
            sync(starmap(call_, sync.iterable))
        return self


class MappingMixin(DelayMixin, RepeatMixin, MapMixin):

    '''mapping mixin'''
