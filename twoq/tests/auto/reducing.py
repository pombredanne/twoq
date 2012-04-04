# -*- coding: utf-8 -*-
'''auto reduce test mixins'''

from inspect import ismodule

from twoq.support import port


class AMathQMixin(object):

    def test_max(self):
        self.assertEqual(self.qclass(1, 2, 4).max().end(), 4)
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60),
        ]
        self.assertEqual(
            stuf(self.qclass(*stooges).tap(lambda x: x.age).max().end()),
            stuf(name='curly', age=60),
        )

    def test_min(self):
        self.assertEqual(self.qclass(10, 5, 100, 2, 1000).min().end(), 2)
        self.assertEqual(
            self.qclass(10, 5, 100, 2, 1000).tap(lambda x: x).min().end(), 2,
        )

    def test_minmax(self):
        self.assertEqual(self.qclass(1, 2, 4).minmax().end(), [1, 4])
        self.assertEqual(
            self.qclass(10, 5, 100, 2, 1000).minmax().end(), [2, 1000],
        )

    def test_median(self):
        self.assertEqual(self.qclass(4, 5, 7, 2, 1).median().end(), 4)
        self.assertEqual(self.qclass(4, 5, 7, 2, 1, 8).median().end(), 4.5)

    def test_mode(self):
        self.assertEqual(
            self.qclass(11, 3, 5, 11, 7, 3, 11).mode().end(), 11,
        )

    def test_statrange(self):
        self.assertEqual(self.qclass(3, 5, 7, 3, 11).statrange().end(), 8)

    def test_sum(self):
        self.assertEqual(self.qclass(1, 2, 3).sum().end(), 6)
        self.assertEqual(self.qclass(1, 2, 3).sum(1).end(), 7)

    def test_fsum(self):
        self.assertEqual(
            self.qclass(.1, .1, .1, .1, .1, .1, .1, .1, .1, .1).fsum().end(),
            1.0,
        )

    def test_average(self):
        self.assertEqual(
            self.qclass(10, 40, 45).average().end(), 31.666666666666668,
        )


class ATruthQMixin(object):

    def test_all(self):
        self.assertFalse(
            self.qclass(True, 1, None, 'yes').tap(bool).all().end()
        )

    def test_any(self):
        self.assertTrue(
            self.qclass(None, 0, 'yes', False).tap(bool).any().end()
        )

    def test_include(self):
        self.assertTrue(self.qclass(1, 2, 3).contains(3).end())

    def test_quantify(self):
        self.assertEqual(
            self.qclass(True, 1, None, 'yes').tap(bool).quantify().end(), 3,
        )
        self.assertEqual(
            self.qclass(None, 0, 'yes', False).tap(bool).quantify().end(), 1,
        )

    def test_uncommon(self):
        self.assertEqual(
            self.qclass(11, 3, 5, 11, 7, 3, 11).uncommon().end(), 7,
        )

    def test_frequency(self):
        self.assertEqual(
            self.qclass(11, 3, 5, 11, 7, 3, 11).frequency().end(),
            [(11, 3), (3, 2), (5, 1), (7, 1)]
        )


class AReduceQMixin(AMathQMixin, ATruthQMixin):

    def test_smash(self):
        self.assertEqual(
            self.qclass([[1, [2], [3, [[4]]]]]).smash().end(), [1, 2, 3, 4],
        )

    def test_merge(self):
        self.assertEqual(
            self.qclass([4, 5, 6], [1, 2, 3]).merge().end(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_pairwise(self):
        self.assertEqual(
            self.qclass(
                'moe', 30, True, 'larry', 40, False, 'curly', 50, 1, 1,
            ).pairwise().end(),
            [('moe', 30), (30, True), (True, 'larry'), ('larry', 40),
            (40, False), (False, 'curly'), ('curly', 50), (50, 1), (1, 1)]
        )

    def test_reduce(self):
        self.assertEqual(
            self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce().end(), 6,
        )
        self.assertEqual(
            self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce(1).end(), 7,
        )

    def test_reduce_right(self):
        self.assertEqual(
            self.qclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce_right().end(), [4, 5, 2, 3, 0, 1],
        )
        self.assertEqual(
            self.qclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce_right([0, 0]).end(), [4, 5, 2, 3, 0, 1, 0, 0],
        )

    def test_roundrobin(self):
        self.assertEqual(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).roundrobin().end(),
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )

    def test_zip(self):
        self.assertEqual(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).zip().end(),
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )


__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
