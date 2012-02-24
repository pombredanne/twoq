# -*- coding: utf-8 -*-
'''reduce test mixins'''

from inspect import ismodule

from twoq.support import port


class MReducingQMixin(object):

    def test_flatten(self):
        manq = self.qclass([[1], [2], [3, [[4]]]]).flatten()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [[1], [2], [3, [[4]]]])
        self.assertFalse(manq.balanced)

    def test_smash(self):
        manq = self.qclass([[1, [2], [3, [[4]]]]]).smash()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [1, 2, 3, 4])
        self.assertFalse(manq.balanced)

    def test_merge(self):
        manq = self.qclass([4, 5, 6], [1, 2, 3]).merge()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [1, 2, 3, 4, 5, 6])
        self.assertFalse(manq.balanced)

    def test_pairwise(self):
        manq = self.qclass(
            'moe', 30, True, 'larry', 40, False, 'curly', 50, 1, 1,
        ).pairwise()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(
            manq.value(),
            [('moe', 30), (30, True), (True, 'larry'), ('larry', 40),
            (40, False), (False, 'curly'), ('curly', 50), (50, 1), (1, 1)]
        )
        self.assertFalse(manq.balanced)

    def test_reduce(self):
        manq = self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), 6)
        self.assertFalse(manq.balanced)
        manq = self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce(1)
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), 7)
        self.assertFalse(manq.balanced)

    def test_reduce_right(self):
        manq = self.qclass([0, 1], [2, 3], [4, 5]).tap(
            lambda x, y: x + y
        ).reduce_right()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertListEqual(
            manq.value(), [4, 5, 2, 3, 0, 1],
        )
        self.assertFalse(manq.balanced)
        manq = self.qclass([0, 1], [2, 3], [4, 5]).tap(
            lambda x, y: x + y
        ).reduce_right([0, 0])
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertListEqual(manq.value(), [4, 5, 2, 3, 0, 1, 0, 0])
        self.assertFalse(manq.balanced)

    def test_roundrobin(self):
        manq = self.qclass(
            ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
        ).roundrobin()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(
            manq.value(),
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )
        self.assertFalse(manq.balanced)

    def test_zip(self):
        manq = self.qclass(
            ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
        ).zip()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(
            manq.value(),
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )
        self.assertFalse(manq.balanced)


class MMathQMixin(object):

    def test_max(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        manq = self.qclass(*stooges).tap(lambda x: x.age).max()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(
            stuf(manq.value()), stuf(name='curly', age=60),
        )
        self.assertFalse(manq.balanced)
        manq = self.qclass(1, 2, 4).max()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), 4)
        self.assertFalse(manq.balanced)

    def test_min(self):
        manq = self.qclass(10, 5, 100, 2, 1000).min()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), 2)
        self.assertFalse(manq.balanced)
        manq = self.qclass(10, 5, 100, 2, 1000).tap(lambda x: x).min()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), 2)
        self.assertFalse(manq.balanced)
        
    def test_minmax(self):
        manq = self.qclass(1, 2, 4).minmax()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [1, 4])
        self.assertFalse(manq.balanced)
        manq = self.qclass(10, 5, 100, 2, 1000).minmax()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [2, 1000])
        self.assertFalse(manq.balanced)

    def test_sum(self):
        manq = self.qclass(1, 2, 3).sum()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), 6)
        self.assertFalse(manq.balanced)
        manq = self.qclass(1, 2, 3).sum(1)
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), 7)
        self.assertFalse(manq.balanced)
        
    def test_mode(self):
        manq = self.qclass(11, 3, 5, 11, 7, 3, 11).mode()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertEquals(manq.value(), 11)
        self.assertFalse(manq.balanced)

    def test_median(self):
        manq = self.qclass(4, 5, 7, 2, 1).median()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertEquals(manq.value(), 4)
        self.assertFalse(manq.balanced)
        manq = self.qclass(4, 5, 7, 2, 1, 8).median()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), 4.5)
        self.assertFalse(manq.balanced)

    def test_fsum(self):
        manq = self.qclass(.1, .1, .1, .1, .1, .1, .1, .1, .1, .1).fsum()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), 1.0)
        self.assertFalse(manq.balanced)

    def test_average(self):
        manq = self.qclass(10, 40, 45).average()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), 31.666666666666668)
        self.assertFalse(manq.balanced)
        
    def test_uncommon(self):
        manq = self.qclass(11, 3, 5, 11, 7, 3, 11).uncommon()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), 7)
        self.assertFalse(manq.balanced)
        
    def test_frequency(self):
        manq = self.qclass(11, 3, 5, 11, 7, 3, 11).frequency()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [(11, 3), (3, 2), (5, 1), (7, 1)])
        self.assertFalse(manq.balanced)

    def test_statrange(self):
        manq = self.qclass(3, 5, 7, 3, 11).statrange()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), 8)
        self.assertFalse(manq.balanced)


class MTruthQMixin(object):

    def test_all(self):
        manq = self.qclass(True, 1, None, 'yes').tap(bool).all()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertFalse(manq.value())
        self.assertFalse(manq.balanced)

    def test_any(self):
        manq = self.qclass(None, 0, 'yes', False).tap(bool).any()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertTrue(manq.value())
        self.assertFalse(manq.balanced)

    def test_include(self):
        manq = self.qclass(1, 2, 3).contains(3)
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertTrue(manq.value())
        self.assertFalse(manq.balanced)

    def test_quantify(self):
        manq = self.qclass(True, 1, None, 'yes').tap(bool).quantify()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), 3)
        self.assertFalse(manq.balanced)
        manq = self.qclass(None, 0, 'yes', False).tap(bool).quantify()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), 1)
        self.assertFalse(manq.balanced)


class MReduceQMixin(MMathQMixin, MReducingQMixin, MTruthQMixin):
    
    '''combination mixin'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
