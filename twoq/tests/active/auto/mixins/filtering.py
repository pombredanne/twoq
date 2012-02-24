# -*- coding: utf-8 -*-
'''auto filtering test mixins'''

from inspect import ismodule

from twoq.support import port


class AFilteringQMixin(object):

    def test_filter(self):
        self.assertEquals(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).filter().value(), [2, 4, 6]
        )

    def test_find(self):
        self.assertEquals(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).find().value(), 2,
        )

    def test_reject(self):
        self.assertEquals(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).reject().value(), [1, 3, 5]
        )

    def test_partition(self):
        self.assertEquals(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: x % 2 == 0
            ).partition().value(), [[1, 3, 5], [2, 4, 6]]
        )

    def test_compact(self):
        self.assertEqual(
            self.qclass(0, 1, False, 2, '', 3).compact().value(),
            [1, 2, 3],
        )

    def test_without(self):
        self.assertEqual(
            self.qclass(1, 2, 1, 0, 3, 1, 4).without(0, 1).value(),
            [2, 3, 4],
        )


class ASliceQMixin(object):

    def test_first(self):
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).first().value(), 5,
        )

    def test_nth(self):
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).nth(2).value(), 3,
        )
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).nth(10, 11).value(), 11,
        )

    def test_last(self):
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).last().value(), 1,
        )

    def test_initial(self):
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).initial().value(), [5, 4, 3, 2]
        )

    def test_rest(self):
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).rest().value(), [4, 3, 2, 1]
        )

    def test_take(self):
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).take(2).value(), [5, 4]
        )

    def test_takeback(self):
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).snatch(2).value(), [2, 1]
        )


class ACollectQMixin(object):

    def test_members(self):
        class stooges:
            name = 'moe'
            age = 40
        class stoog2: #@IgnorePep8
            name = 'larry'
            age = 50
        class stoog3: #@IgnorePep8
            name = 'curly'
            age = 60
        test = lambda x: not x[0].startswith('__')
        self.assertEqual(
            self.qclass(
                stooges, stoog2, stoog3
            ).tap(test).members().detap().value(),
            [('age', 40), ('name', 'moe'), ('age', 50), ('name', 'larry'),
            ('age', 60), ('name', 'curly')],
        )

    def test_deepmembers(self):
        class stooges:
            name = 'moe'
            age = 40
            def boo(self):
                return 'boo'
            def foo(self):
                return 'foo'
        class stoog2: #@IgnorePep8
            name = 'larry'
            age = 50
            def boo(self):
                return 'boo'
            def foo(self):
                return 'foo'
        class stoog3: #@IgnorePep8
            name = 'curly'
            age = 60
            def boo(self):
                return 'boo'
            def foo(self):
                return 'foo'
        test = lambda x: not x[0].startswith('__')
        self.assertSequenceEqual(
            self.qclass(
                stooges, stoog2, stoog3
            ).tap(test).deepmembers().sync().value(),
            [('age', 40), ('boo', stooges.boo), ('foo', stooges.foo),
            ('name', 'moe'), ('age', 50), ('boo', stoog2.boo),
            ('foo', stoog2.foo), ('name', 'larry'), ('age', 60), 
            ('boo', stoog3.boo), ('foo', stoog3.foo), ('name', 'curly')],
        )
        import inspect
        test = lambda x: not x[0].startswith('__') and inspect.ismethod(x[1])
        self.assertSequenceEqual(
            self.qclass(
                stooges, stoog2, stoog3
            ).tap(test).deepmembers().sync().value(),
            [('boo', stooges.boo), ('foo', stooges.foo), ('boo', stoog2.boo),
            ('foo', stoog2.foo), ('boo', stoog3.boo), ('foo', stoog3.foo)],
        )

    def test_pick(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self.assertEqual(
            self.qclass(*stooges).pick('name').value(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.qclass(*stooges).pick('name', 'age').value(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self.assertEqual(
            self.qclass(*stooges).pick('place').value(), [],
        )

    def test_pluck(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self.assertEqual(
            self.qclass(*stooges).pluck('name').value(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.qclass(*stooges).pluck('name', 'age').value(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        self.assertEqual(
            self.qclass(*stooges).pluck(0).value(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.qclass(*stooges).pluck(1).value(),
            [40, 50, 60],
        )
        self.assertEqual(
            self.qclass(*stooges).pluck('place').value(), [],
        )


class ASetQMixin(object):

    def test_difference(self):
        self.assertEqual(
            self.qclass([1, 2, 3, 4, 5], [5, 2, 10]).difference().value(),
            [1, 3, 4],
        )

    def test_intersection(self):
        self.assertEqual(
            self.qclass(
                [1, 2, 3], [101, 2, 1, 10], [2, 1]
            ).intersection().value(), [1, 2],
        )

    def test_union(self):
        self.assertEqual(
            self.qclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).union().value(),
            [1, 2, 3, 101, 10],
        )

    def test_unique(self):
        self.assertEqual(
            self.qclass(1, 2, 1, 3, 1, 4).unique().value(),
            [1, 2, 3, 4],
        )
        self.assertEqual(
            self.qclass(1, 2, 1, 3, 1, 4).tap(round).unique().value(),
            [1, 2, 3, 4],
        )


class AFilterQMixin(AFilteringQMixin, ACollectQMixin, ASetQMixin, ASliceQMixin):
    
    '''combination mixin'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
del port
