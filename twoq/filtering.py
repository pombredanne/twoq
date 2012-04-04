# -*- coding: utf-8 -*-
'''twoq filtering mixins'''

from itertools import tee, islice
from inspect import getmro
from threading import local
from functools import reduce

from operator import attrgetter, itemgetter, truth

from stuf.six import PY3
from stuf.utils import getcls

from twoq.support import ifilter, ichain, imap, filterfalse


class CollectMixin(local):

    '''collecting mixin'''

    @classmethod
    def _extract(cls, truth, subcall, transform, iterable):
        '''
        collect members of things

        @param call: "Truth" filter
        @param truth: second "Truth" filter
        @param iterable: an iterable
        '''
        def members(
            f, s, t, i, d_=dir, w_=cls._extract, g=getattr, e=AttributeError,
        ): #@IgnorePep8
            for k in d_(i):
                try:
                    v = g(i, k)
                except e:
                    pass
                else:
                    if s(v):
                        yield k, t(w_(f, s, t, v))
                    else:
                        yield k, v
        for member in ifilter(
            truth, members(truth, subcall, transform, iterable),
        ):
            yield member

    @classmethod
    def _mfilter(cls, call, iterable):
        '''
        filter members of things

        @param call: "Truth" filter
        @param iterable: an iterable
        '''
        def members(iterable):
            getattr_, AttributeError_ = getattr, AttributeError
            for key in dir(iterable):
                try:
                    thing = getattr_(iterable, key)
                except AttributeError_:
                    pass
                else:
                    yield key, thing
        for i in ifilter(call, members(iterable)):
            yield i

    @staticmethod
    def _pick(names, iterable):
        '''
        collect attributes of things in iterable

        @param names: sequence of names
        @param iterable: an iterable
        '''
        attrfind = attrgetter(*names)
        for thing in iterable:
            try:
                yield attrfind(thing)
            except AttributeError:
                pass

    @staticmethod
    def _pluck(keys, iterable, _itemgetter=itemgetter):
        '''
        collect values of things in iterable

        @param keys: sequence of keys
        @param iterable: an iterable
        '''
        itemfind = _itemgetter(*keys)
        IndexError_, KeyError_, TypeError_ = IndexError, KeyError, TypeError
        for thing in iterable:
            try:
                yield itemfind(thing)
            except (IndexError_, KeyError_, TypeError_):
                pass

    def deepmembers(self):
        '''collect object members from incoming things and their bases'''
        _mf = self._mfilter
        _mz = lambda x: _mf(self._call, x)
        if PY3:
            def _memfilters(thing, mz=_mz, gc=getcls, ci=ichain):
                t = lambda x: not x[0].startswith('mro')
                return self._ifilter(
                    t, ci(imap(mz, ci([getmro((gc(thing))), [thing]])))
                )
        else:
            def _memfilters(thing, mz=_mz, gc=getcls, ci=ichain):
                return ci(imap(mz, ci([getmro((gc(thing))), [thing]])))
        with self._context():
            return self._xtend(
                ichain(imap(_memfilters, self._iterable))
            )
            
    def extract(self):
        '''extract object members from incoming things'''
        with self._context():
            walk_ = self._extract
            call_, alt_, wrap_ = self._call, self._alt, self._wrapper
            return self._xtend(ichain(imap(
                lambda x: walk_(call_, alt_, wrap_, x), self._iterable,
            )))

    def members(self):
        '''collect object members from incoming things'''
        with self._context():
            mfilter = self._mfilter
            return self._xtend(ichain(imap(
                lambda x: mfilter(self._call, x), self._iterable,
            )))

    def pick(self, *names):
        '''collect object attributes from incoming things by their `*names`'''
        with self._context():
            return self._xtend(self._pick(names, self._iterable))

    def pluck(self, *keys):
        '''collect object items from incoming things by item `*keys`'''
        with self._context():
            return self._xtend(self._pluck(keys, self._iterable))


class SetMixin(local):

    '''set and uniqueness mixin'''

    @classmethod
    def _unique(cls, iterable, key=None):
        '''
        unique things in in iterable

        @param iterable: an iterable
        @param key: determine uniqueness filter
        '''
        seen = set()
        seen_add_, seen_contains_ = seen.add, seen.__contains__
        if key is None:
            for element in filterfalse(seen_contains_, iterable):
                seen_add_(element)
                yield element
        else:
            for element in iterable:
                k = key(element)
                if k not in seen:
                    seen_add_(k)
                    yield element

    def difference(self):
        '''difference between incoming things'''
        with self._context():
            return self._xtend(reduce(
                lambda x, y: set(x).difference(y), self._iterable,
            ))

    def symmetric_difference(self):
        '''symmetric difference between incoming things'''
        with self._context():
            return self._xtend(reduce(
                lambda x, y: set(x).symmetric_difference(y), self._iterable,
            ))

    def disjointed(self):
        '''disjoint between incoming things'''
        with self._context():
            return self._append(reduce(
                lambda x, y: set(x).isdisjoint(y), self._iterable,
            ))

    def intersection(self):
        '''intersection between incoming things'''
        with self._context():
            return self._xtend(reduce(
                lambda x, y: set(x).intersection(y), self._iterable,
            ))

    def subset(self):
        '''incoming things that are subsets of incoming things'''
        with self._context():
            return self._append(reduce(
                lambda x, y: set(x).issubset(y), self._iterable,
            ))

    def superset(self):
        '''incoming things that are supersets of incoming things'''
        with self._context():
            return self._append(reduce(
                lambda x, y: set(x).issubset(y), self._iterable
            ))

    def union(self):
        '''union between incoming things'''
        with self._context():
            return self._xtend(
                reduce(lambda x, y: set(x).union(y), self._iterable)
            )

    def unique(self):
        '''
        list unique incoming things, preserving order and remember all incoming
        things ever seen
        '''
        with self._context():
            return self._iter(self._unique(self._iterable, self._call))


class SliceMixin(local):

    '''slicing mixin'''

    def nth(self, n, default=None):
        '''
        `nth` incoming thing or default thing

        @param n: number of things
        @param default: default thing (default: None)
        '''
        with self._context():
            return self._append(
                next(islice(self._iterable, n, None), default)
            )

    def initial(self):
        '''all incoming things except the last thing'''
        with self._context():
            i1, i2 = tee(self._iterable)
            return self._xtend(islice(i1, len(list(i2)) - 1))

    def rest(self):
        '''all incoming things except the first thing'''
        with self._context():
            return self._xtend(islice(self._iterable, 1, None))

    def snatch(self, n):
        '''
        last `n` things of incoming things

        @param n: number of things
        '''
        with self._context():
            i1, i2 = tee(self._iterable)
            return self._xtend(islice(i1, len(list(i2)) - n, None))

    def take(self, n):
        '''
        first `n` things of incoming things

        @param n: number of things
        '''
        with self._context():
            return self._xtend(islice(self._iterable, n))


class FilterMixin(local):

    '''filters mixin'''

    def compact(self):
        '''strip "untrue" things from incoming things'''
        with self._context():
            return self._iter(ifilter(truth, self._iterable))

    def filter(self):
        '''incoming things for which call is `True`'''
        with self._context():
            return self._xtend(ifilter(self._call, self._iterable))

    def find(self):
        '''first incoming thing for which call is `True`'''
        with self._context():
            return self._append(
                next(ifilter(self._call, self._iterable))
            )

    def partition(self):
        '''
        split incoming things into `True` and `False` things based on results
        of call
        '''
        list_, call_ = list, self._call
        with self._context():
            falsy, truey = tee(self._iterable)
            return self._xtend(iter([
                list_(filterfalse(call_, falsy)), list_(ifilter(call_, truey)),
            ]))

    def reject(self):
        '''incoming things for which call is `False`'''
        with self._context():
            return self._xtend(filterfalse(self._call, self._iterable))

    def without(self, *things):
        '''strip things from incoming things'''
        with self._context():
            return self._xtend(
                filterfalse(lambda y: y in things, self._iterable)
            )


class FilteringMixin(CollectMixin, SetMixin, SliceMixin, FilterMixin):

    '''filtering mixin'''
