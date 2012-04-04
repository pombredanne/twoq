# -*- coding: utf-8 -*-
'''twoq mapping mixins'''

from time import sleep
from copy import deepcopy
from threading import local
from operator import methodcaller
from itertools import starmap, tee, repeat

from twoq.support import imap, ichain, items, xrange


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
        sleep(wait)
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
        sleep(wait)
        results = caller(x)
        return x if results is None else results

    @staticmethod
    def _delay_map(x, wait=None, caller=None):
        '''
        invoke call on thing after a delay

        @param wait: time in seconds to delay (default: 0)
        @param caller: a callable (default: None)
        '''
        sleep(wait)
        return caller(x)

    def delay_each(self, wait):
        '''
        invoke call with passed arguments, keywords in incoming things after
        delay `wait`

        @param wait: time in seconds
        '''
        with self._context():
            de, call = self._delay_each, self._call
            return self._xtend(starmap(
                lambda x, y: de(x, y, wait, call), self._iterable,
            ))

    def delay_invoke(self, name, wait):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords after delay `wait` but return incoming thing instead if method
        returns `None`

        @param name: name of method
        @param wait: time in seconds
        '''
        with self._context():
            di, mc = self._delay_invoke, methodcaller
            args, kw = self._args, self._kw
            return self._xtend(imap(
                lambda x: di(x, wait, mc(name, *args, **kw)), self._iterable,
            ))

    def delay_map(self, wait):
        '''
        invoke call on each incoming thing after delay `wait`

        @param wait: time in seconds
        '''
        with self._context():
            dm, call = self._delay_map, self._call
            return self._xtend(imap(
                lambda x: dm(x, wait, call), self._iterable,
            ))


class RepeatMixin(local):

    '''repetition mixin'''

    def copy(self):
        '''copy each incoming thing'''
        with self._context():
            return self._xtend(imap(deepcopy, self._iterable))

    def padnone(self):
        '''repeat incoming things and then `None` indefinitely'''
        with self._context():
            return self._iter(tee(self._iterable, repeat(None)))

    def range(self, start, stop=0, step=1):
        '''
        put sequence of numbers in incoming things

        @param start: number to start with
        @param stop: number to stop with (default: 0)
        @param step: number of steps to advance per iteration (default: 1)
        '''
        with self._context():
            return self._xtend(
                xrange(start, stop, step) if stop else xrange(start)
            )

    def repeat(self, n):
        '''
        repeat incoming things `n` times

        @param n: number of times to repeat
        '''
        with self._context():
            return self._xtend(repeat(tuple(self._iterable), n))

    def times(self, n=None):
        '''
        repeat call with incoming things `n` times

        @param n: repeat call n times on incoming things (default: None)
        '''
        with self._context():
            if n is None:
                return self._xtend(starmap(
                    self._call, repeat(list(self._iterable)),
                ))
            return self._xtend(starmap(
                self._call, repeat(list(self._iterable), n),
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
            return self._xtend(imap(self._call, self._iterable))

    def invoke(self, name):
        '''
        invoke method `name` on each incoming thing with passed arguments,
        keywords but return incoming thing instead if method returns `None`

        @param name: name of method
        '''
        with self._context():
            invoke = self._invoke
            return self._xtend(imap(
                lambda x: invoke(
                    x, caller=methodcaller(name, *self._args, **self._kw)
                ),
                self._iterable
            ))

    def each(self):
        '''invoke call with passed arguments, keywords in incoming things'''
        with self._context():
            return self._xtend(starmap(
                lambda x, y: self._call(*x, **y), self._iterable,
            ))

    def starmap(self):
        '''invoke call on each sequence of incoming things'''
        with self._context():
            return self._xtend(starmap(self._call, self._iterable))

    def items(self):
        '''invoke call on each mapping to get key, value pairs'''
        with self._context():
            return self._xtend(starmap(
                self._call, ichain(imap(items, self._iterable))
            ))


class MappingMixin(DelayMixin, RepeatMixin, MapMixin):

    '''mapping mixin'''
