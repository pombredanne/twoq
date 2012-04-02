# -*- coding: utf-8 -*-
'''filtering test mixins'''

from inspect import ismodule

from twoq.support import port


class MSliceQMixin(object):

    def test_first(self):
        manq = self.qclass(5, 4, 3, 2, 1).first()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), 5)
        self.assertFalse(manq.balanced)

    def test_nth(self):
        self._false_true_false(
            self.qclass(5, 4, 3, 2, 1).nth(2), self.assertEqual, 3,
        )
        self._false_true_false(
            self.qclass(5, 4, 3, 2, 1).nth(10, 11), self.assertEqual, 11,
        )

    def test_last(self):
        manq = self.qclass(5, 4, 3, 2, 1).last()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), 1)
        self.assertFalse(manq.balanced)

    def test_initial(self):
        self._false_true_false(
            self.qclass(5, 4, 3, 2, 1).initial(),
            self.assertEqual,
            [5, 4, 3, 2],
        )

    def test_rest(self):
        self._false_true_false(
            self.qclass(5, 4, 3, 2, 1).rest(), self.assertEqual, [4, 3, 2, 1],
        )

    def test_take(self):
        self._false_true_false(
            self.qclass(5, 4, 3, 2, 1).take(2), self.assertEqual, [5, 4],
        )

    def test_takeback(self):
        self._false_true_false(
            self.qclass(5, 4, 3, 2, 1).snatch(2), self.assertEqual, [2, 1],
        )


class MCollectQMixin(object):

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
        self._true_true_false(
            self.qclass(
                stooges, stoog2, stoog3
            ).tap(
                lambda x: not x[0].startswith('__')
            ).members().detap().sync(),
            self.assertEqual,
            [('age', 40), ('name', 'moe'), ('age', 50), ('name', 'larry'),
            ('age', 60), ('name', 'curly')],
        )

    def test_deepmembers(self):
        class stooges:
            name = 'moe'
            age = 40
            def boo(self):#@IgnorePep8
                return 'boo'
            def foo(self):#@IgnorePep8
                return 'foo'
        class stoog2: #@IgnorePep8
            name = 'larry'
            age = 50
            def boo(self):#@IgnorePep8
                return 'boo'
            def foo(self):#@IgnorePep8
                return 'foo'
        class stoog3: #@IgnorePep8
            name = 'curly'
            age = 60
            def boo(self):#@IgnorePep8
                return 'boo'
            def foo(self):#@IgnorePep8
                return 'foo'
        test = lambda x: not x[0].startswith('__')
        self._false_true_false(
            self.qclass(stooges, stoog2, stoog3).tap(test).deepmembers(),
            self.assertEqual,
                [('age', 40), ('boo', stooges.boo), ('foo', stooges.foo),
                ('name', 'moe'), ('age', 50), ('boo', stoog2.boo),
                ('foo', stoog2.foo), ('name', 'larry'), ('age', 60),
                ('boo', stoog3.boo), ('foo', stoog3.foo), ('name', 'curly')],
            )
        from stuf.six import callable
        test = lambda x: not x[0].startswith('_') and callable(x[1])
        self._false_true_false(
            self.qclass(stooges, stoog2, stoog3).tap(test).deepmembers(),
            self.assertEqual,
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
        self._true_true_false(
            self.qclass(*stooges).pick('name'),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.qclass(*stooges).pick('name', 'age'),
            self.assertEqual,
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self._false_true_true(
            self.qclass(*stooges).pick('place'),
            self.assertEqual,
            [],
        )

    def test_pluck(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self._true_true_false(
            self.qclass(*stooges).pluck('name'),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.qclass(*stooges).pluck('name', 'age'),
            self.assertEqual,
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        self._true_true_false(
            self.qclass(*stooges).pluck(0),
            self.assertEqual,
            ['moe', 'larry', 'curly'],
        )
        self._true_true_false(
            self.qclass(*stooges).pluck(1),
            self.assertEqual,
            [40, 50, 60],
        )
        self._false_true_true(
            self.qclass(*stooges).pluck('place'),
            self.assertEqual,
            [],
        )


class MSetQMixin(object):

    def test_difference(self):
        self._false_true_false(
            self.qclass([1, 2, 3, 4, 5], [5, 2, 10]).difference(),
            self.assertEqual,
            [1, 3, 4]
        )

    def test_symmetric_difference(self):
        self._false_true_false(
            self.qclass([1, 2, 3, 4, 5], [5, 2, 10]).symmetric_difference(),
            self.assertEqual,
            [1, 3, 4, 10]
        )

    def test_disjointed(self):
        self._false_true_false(
            self.qclass([1, 2, 3], [5, 4, 10]).disjointed(), self.assertTrue,
        )
        self._false_true_false(
            self.qclass([1, 2, 3], [5, 2, 10]).disjointed(), self.assertFalse,
        )

    def test_intersection(self):
        self._false_true_false(
            self.qclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).intersection(),
            self.assertEqual,
            [1, 2],
        )

    def test_union(self):
        self._false_true_false(
            self.qclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).union(),
            self.assertEqual,
            [1, 10, 3, 2, 101],
        )

    def test_subset(self):
        self._false_true_false(
            self.qclass([1, 2, 3], [101, 2, 1, 3]).subset(),
            self.assertTrue,
        )

    def test_superset(self):
        self._false_true_false(
            self.qclass([1, 2, 3], [101, 2, 1, 3, 6, 34]).superset(),
            self.assertTrue,
        )

    def test_unique(self):
        self._false_true_false(
            self.qclass(1, 2, 1, 3, 1, 4).unique(),
            self.assertEqual,
            [1, 2, 3, 4],
        )
        self._false_true_false(
            self.qclass(1, 2, 1, 3, 1, 4).tap(round).unique(),
            self.assertEqual,
            [1, 2, 3, 4],
        )


class MFilterQMixin(MCollectQMixin, MSetQMixin, MSliceQMixin):

    def test_filter(self):
        self._false_true_false(
            self.qclass(1, 2, 3, 4, 5, 6).tap(lambda x: x % 2 == 0).filter(),
            self.assertEqual,
            [2, 4, 6],
        )

    def test_find(self):
        self._false_true_false(
            self.qclass(1, 2, 3, 4, 5, 6).tap(lambda x: x % 2 == 0).find(),
            self.assertEqual,
            2,
        )

    def test_reject(self):
        self._false_true_false(
            self.qclass(1, 2, 3, 4, 5, 6).tap(lambda x: x % 2 == 0).reject(),
            self.assertEqual,
            [1, 3, 5],
        )

    def test_partition(self):
        self._false_true_false(
            self.qclass(
                1, 2, 3, 4, 5, 6
            ).tap(lambda x: x % 2 == 0).partition(),
            self.assertEqual,
            [[1, 3, 5], [2, 4, 6]],
        )

    def test_compact(self):
        self._false_true_false(
            self.qclass(0, 1, False, 2, '', 3).compact(),
            self.assertEqual,
            [1, 2, 3],
        )

    def test_without(self):
        self._false_true_false(
            self.qclass(1, 2, 1, 0, 3, 1, 4).without(0, 1),
            self.assertEqual,
            [2, 3, 4],
        )


__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
