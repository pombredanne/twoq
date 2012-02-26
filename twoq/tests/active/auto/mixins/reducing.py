# -*- coding: utf-8 -*-
'''auto reduce test mixins'''

from inspect import ismodule

from twoq.support import port


class AReducingQMixin(object):

    def test_smash(self):
        self.assertEquals(
            self.qclass([[1, [2], [3, [[4]]]]]).smash().value(), [1, 2, 3, 4],
        )

    def test_merge(self):
        self.assertEquals(
            self.qclass([4, 5, 6], [1, 2, 3]).merge().value(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_pairwise(self):
        self.assertEquals(
            self.qclass(
                'moe', 30, True, 'larry', 40, False, 'curly', 50, 1, 1,
            ).pairwise().value(),
            [('moe', 30), (30, True), (True, 'larry'), ('larry', 40),
            (40, False), (False, 'curly'), ('curly', 50), (50, 1), (1, 1)]
        )

    def test_reduce(self):
        self.assertEquals(
            self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce().value(), 6,
        )
        self.assertEquals(
            self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce(1).value(),
            7,
        )

    def test_reduce_right(self):
        self.assertEquals(
            self.qclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce_right().value(), [4, 5, 2, 3, 0, 1],
        )
        self.assertEquals(
            self.qclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce_right([0, 0]).value(), [4, 5, 2, 3, 0, 1, 0, 0],
        )

    def test_roundrobin(self):
        self.assertEquals(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).roundrobin().value(),
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )

    def test_zip(self):
        self.assertEquals(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).zip().value(),
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )


class AMathQMixin(object):

    def test_max(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self.assertEquals(
            stuf(self.qclass(*stooges).tap(lambda x: x.age).max().value()),
            stuf(name='curly', age=60),
        )
        self.assertEquals(self.qclass(1, 2, 4).max().value(), 4)

    def test_min(self):
        self.assertEquals(self.qclass(10, 5, 100, 2, 1000).min().value(), 2)
        self.assertEquals(
            self.qclass(10, 5, 100, 2, 1000).tap(lambda x: x).min().value(),
            2,
        )

    def test_minmax(self):
        self.assertEquals(self.qclass(1, 2, 4).minmax().value(), [1, 4])
        self.assertEquals(
            self.qclass(10, 5, 100, 2, 1000).minmax().value(), [2, 1000],
        )

    def test_median(self):
        self.assertEquals(self.qclass(4, 5, 7, 2, 1).median().value(), 4)
        self.assertEquals(self.qclass(4, 5, 7, 2, 1, 8).median().value(), 4.5)

    def test_mode(self):
        self.assertEquals(
            self.qclass(11, 3, 5, 11, 7, 3, 11).mode().value(), 11,
        )

    def test_uncommon(self):
        self.assertEquals(
            self.qclass(11, 3, 5, 11, 7, 3, 11).uncommon().value(), 7,
        )

    def test_frequency(self):
        self.assertEquals(
            self.qclass(11, 3, 5, 11, 7, 3, 11).frequency().value(),
            [(11, 3), (3, 2), (5, 1), (7, 1)]
        )

    def test_statrange(self):
        self.assertEquals(
            self.qclass(3, 5, 7, 3, 11).statrange().value(), 8,
        )

    def test_sum(self):
        self.assertEquals(self.qclass(1, 2, 3).sum().value(), 6)
        self.assertEquals(self.qclass(1, 2, 3).sum(1).value(), 7)

    def test_fsum(self):
        self.assertEquals(
            self.qclass(.1, .1, .1, .1, .1, .1, .1, .1, .1, .1).fsum().value(),
            1.0,
        )

    def test_average(self):
        self.assertEquals(
            self.qclass(10, 40, 45).average().value(), 31.666666666666668,
        )


class ATruthQMixin(object):

    def test_all(self):
        self.assertFalse(
            self.qclass(True, 1, None, 'yes').tap(bool).all().value()
        )

    def test_any(self):
        self.assertTrue(
            self.qclass(None, 0, 'yes', False).tap(bool).any().value()
        )

    def test_include(self):
        self.assertTrue(
            self.qclass(1, 2, 3).contains(3).value()
        )

    def test_quantify(self):
        self.assertEqual(
            self.qclass(True, 1, None, 'yes').tap(bool).quantify().value(),
            3,
        )
        self.assertEqual(
            self.qclass(None, 0, 'yes', False).tap(bool).quantify().value(),
            1
        )


class AReduceQMixin(AMathQMixin, AReducingQMixin, ATruthQMixin):

    '''combination mixin'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
