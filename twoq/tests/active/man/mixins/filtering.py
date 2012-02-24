# -*- coding: utf-8 -*-
'''filtering test mixins'''

from inspect import ismodule

from twoq.support import port


class MFilteringQMixin(object):

    def test_filter(self):
        manq = self.qclass(1, 2, 3, 4, 5, 6).tap(lambda x: x % 2 == 0).filter()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [2, 4, 6])
        self.assertFalse(manq.balanced)

    def test_find(self):
        manq = self.qclass(1, 2, 3, 4, 5, 6).tap(lambda x: x % 2 == 0).find()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), 2)
        self.assertFalse(manq.balanced)

    def test_reject(self):
        manq = self.qclass(1, 2, 3, 4, 5, 6).tap(lambda x: x % 2 == 0).reject()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [1, 3, 5])
        self.assertFalse(manq.balanced)

    def test_partition(self):
        manq = self.qclass(
            1, 2, 3, 4, 5, 6
        ).tap(lambda x: x % 2 == 0).partition()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [[1, 3, 5], [2, 4, 6]])
        self.assertFalse(manq.balanced)

    def test_compact(self):
        manq = self.qclass(0, 1, False, 2, '', 3).compact()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [1, 2, 3])
        self.assertFalse(manq.balanced)

    def test_without(self):
        manq = self.qclass(1, 2, 1, 0, 3, 1, 4).without(0, 1)
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [2, 3, 4])
        self.assertFalse(manq.balanced)


class MSliceQMixin(object):

    def test_first(self):
        manq = self.qclass(5, 4, 3, 2, 1).first()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), 5)
        self.assertFalse(manq.balanced)

    def test_nth(self):
        manq = self.qclass(5, 4, 3, 2, 1).nth(2)
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), 3)
        self.assertFalse(manq.balanced)
        manq = self.qclass(5, 4, 3, 2, 1).nth(10, 11)
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), 11)
        self.assertFalse(manq.balanced)

    def test_last(self):
        manq = self.qclass(5, 4, 3, 2, 1).last()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), 1)
        self.assertFalse(manq.balanced)

    def test_initial(self):
        manq = self.qclass(5, 4, 3, 2, 1).initial()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [5, 4, 3, 2])
        self.assertFalse(manq.balanced)

    def test_rest(self):
        manq = self.qclass(5, 4, 3, 2, 1).rest()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [4, 3, 2, 1])
        self.assertFalse(manq.balanced)

    def test_take(self):
        manq = self.qclass(5, 4, 3, 2, 1).take(2)
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [5, 4])
        self.assertFalse(manq.balanced)

    def test_takeback(self):
        manq = self.qclass(5, 4, 3, 2, 1).snatch(2)
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [2, 1])
        self.assertFalse(manq.balanced)


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
        test = lambda x: not x[0].startswith('__')
        manq = self.qclass(
            stooges, stoog2, stoog3
        ).tap(test).members().detap().sync()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(
            manq.value(),
            [('age', 40), ('name', 'moe'), ('age', 50), ('name', 'larry'),
            ('age', 60), ('name', 'curly')],
        )
        self.assertFalse(manq.balanced)
        
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
        manq = self.qclass(stooges, stoog2, stoog3).tap(test).deepmembers()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(
            manq.value(),
            [('age', 40), ('boo', stooges.boo), ('foo', stooges.foo),
            ('name', 'moe'), ('age', 50), ('boo', stoog2.boo),
            ('foo', stoog2.foo), ('name', 'larry'), ('age', 60), 
            ('boo', stoog3.boo), ('foo', stoog3.foo), ('name', 'curly')],
        )
        self.assertFalse(manq.balanced)
        import inspect
        test = lambda x: not x[0].startswith('__') and inspect.ismethod(x[1])
        manq = self.qclass(stooges, stoog2, stoog3).tap(test).deepmembers()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(
            manq.value(),
            [('boo', stooges.boo), ('foo', stooges.foo), ('boo', stoog2.boo),
            ('foo', stoog2.foo), ('boo', stoog3.boo), ('foo', stoog3.foo)],
        )
        self.assertFalse(manq.balanced)

    def test_pick(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        manq = self.qclass(*stooges).pick('name')
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), ['moe', 'larry', 'curly'])
        self.assertFalse(manq.balanced)
        manq = self.qclass(*stooges).pick('name', 'age')
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(
            manq.value(), [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self.assertFalse(manq.balanced)
        manq = self.qclass(*stooges).pick('place')
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [])
        self.assertTrue(manq.balanced)

    def test_pluck(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        manq = self.qclass(*stooges).pluck('name')
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), ['moe', 'larry', 'curly'])
        self.assertFalse(manq.balanced)
        manq = self.qclass(*stooges).pluck('name', 'age')
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(
            manq.value(), [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self.assertFalse(manq.balanced)
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        manq = self.qclass(*stooges).pluck(0)
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), ['moe', 'larry', 'curly'])
        self.assertFalse(manq.balanced)
        manq = self.qclass(*stooges).pluck(1)
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [40, 50, 60])
        self.assertFalse(manq.balanced)
        manq = self.qclass(*stooges).pluck('place')
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [])
        self.assertTrue(manq.balanced)


class MSetQMixin(object):

    def test_difference(self):
        manq = self.qclass([1, 2, 3, 4, 5], [5, 2, 10]).difference()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [1, 3, 4])
        self.assertFalse(manq.balanced)

    def test_intersection(self):
        manq = self.qclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).intersection()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [1, 2])
        self.assertFalse(manq.balanced)

    def test_union(self):
        manq = self.qclass([1, 2, 3], [101, 2, 1, 10], [2, 1]).union()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [1, 2, 3, 101, 10])
        self.assertFalse(manq.balanced)

    def test_unique(self):
        manq = self.qclass(1, 2, 1, 3, 1, 4).unique()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [1, 2, 3, 4])
        self.assertFalse(manq.balanced)
        manq = self.qclass(1, 2, 1, 3, 1, 4).tap(round).unique()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [1, 2, 3, 4])
        self.assertFalse(manq.balanced)
        
        
class MFilterQMixin(MFilteringQMixin, MCollectQMixin, MSetQMixin, MSliceQMixin):
    
    '''combination mixin'''


__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
