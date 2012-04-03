# -*- coding: utf-8 -*-
'''twoq mapping mixins'''

from copy import deepcopy
from threading import local


class DelayMixin(local):

    '''delayed map mixin'''

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
        with self._context():
            return self._xtend(self._starmap(self._partial(
                self._delay_each, wait=wait, caller=self._call
            ), self._iterable))

    def delay_invoke(self, name, wait):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords after delay `wait` but return incoming thing instead if method
        returns `None`

        @param name: name of method
        @param wait: time in seconds
        '''
        with self._context():
            return self._xtend(self._imap(self._partial(
                self._delay_invoke,
                wait=wait,
                caller=self._methodcaller(name, *self._args, **self._kw),
            ), self._iterable))

    def delay_map(self, wait):
        '''
        invoke call on each incoming thing after delay `wait`

        @param wait: time in seconds
        '''
        with self._context():
            return self._xtend(self._imap(self._partial(
                self._delay_map, wait=wait, caller=self._call
            ), self._iterable))


class RepeatMixin(local):

    '''repetition mixin'''

    def copy(self):
        '''copy each incoming thing'''
        with self._context():
            return self._xtend(self._imap(deepcopy, self._iterable))

    def padnone(self):
        '''repeat incoming things and then `None` indefinitely'''
        with self._context():
            return self._iter(
                self._join(self._iterable, self._repeat(None),
            ))

    def range(self, start, stop=0, step=1):
        '''
        put sequence of numbers in incoming things

        @param start: number to start with
        @param stop: number to stop with (default: 0)
        @param step: number of steps to advance per iteration (default: 1)
        '''
        with self._context():
            return self._xtend(
                self._range(start, stop, step) if stop else self._range(start)
            )

    def repeat(self, n):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        with self._context():
            return self._xtend(self._repeat(tuple(self._iterable), n))

    def times(self, n=None):
        '''
        repeat call with incoming things `n` times

        @param n: repeat call n times on incoming things (default: None)
        '''
        with self._context():
            if n is None:
                return self._xtend(self._starmap(
                    self._call, self._repeat(self._list(self._iterable)),
                ))
            return self._xtend(self._starmap(
                self._call, self._repeat(self._list(self._iterable), n),
            ))


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
        with self._context():
            return self._xtend(self._imap(self._call, self._iterable))

    def invoke(self, name):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords but return incoming thing instead if method returns `None`

        @param name: name of method
        '''
        with self._context():
            return self._xtend(self._imap(self._partial(
                self._invoke,
                caller=self._methodcaller(name, *self._args, **self._kw),
            ), self._iterable))

    def each(self):
        '''invoke call with passed arguments, keywords in incoming things'''
        with self._context():
            return self._xtend(self._starmap(
                lambda x, y: self._call(*x, **y), self._iterable,
            ))

    def starmap(self):
        '''invoke call on each sequence of incoming things'''
        with self._context():
            return self._xtend(self._starmap(self._call, self._iterable))

    def items(self):
        '''invoke call on each mapping to get key, value pairs'''
        with self._context():
            return self._xtend(self._starmap(
                self._call,
                self._ichain(self._imap(self._items, self._iterable))
            ))


class MappingMixin(DelayMixin, RepeatMixin, MapMixin):

    '''mapping mixin'''
