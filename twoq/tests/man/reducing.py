# -*- coding: utf-8 -*-
'''reduce test mixins'''

from inspect import ismodule

from twoq.support import port


class MMathQMixin(object):

    def test_max(self):
        self._false_true_false(
            self.qclass(1, 2, 4).max(), self.assertEqual, 4,
        )
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60),
        ]
        manq = self.qclass(*stooges).tap(lambda x: x.age).max()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(stuf(manq.end()), stuf(name='curly', age=60))
        self.assertTrue(manq.balanced)

    def test_min(self):
        self._false_true_false(
            self.qclass(10, 5, 100, 2, 1000).min(),
            self.assertEqual,
            2,
        )
        self._false_true_false(
            self.qclass(10, 5, 100, 2, 1000).tap(lambda x: x).min(),
            self.assertEqual,
            2,
        )

    def test_minmax(self):
        self._false_true_false(
            self.qclass(1, 2, 4).minmax(), self.assertEqual, [1, 4],
        )
        self._false_true_false(
            self.qclass(10, 5, 100, 2, 1000).minmax(),
            self.assertEqual,
            [2, 1000],
        )

    def test_sum(self):
        self._false_true_false(
            self.qclass(1, 2, 3).sum(), self.assertEqual, 6,
        )
        self._false_true_false(
            self.qclass(1, 2, 3).sum(1), self.assertEqual, 7,
        )

    def test_mode(self):
        self._false_true_false(
            self.qclass(11, 3, 5, 11, 7, 3, 11).mode(),
            self.assertEqual,
            11,
        )

    def test_median(self):
        self._false_true_false(
            self.qclass(4, 5, 7, 2, 1).median(), self.assertEqual, 4,
        )
        self._false_true_false(
            self.qclass(4, 5, 7, 2, 1, 8).median(), self.assertEqual, 4.5,
        )

    def test_fsum(self):
        self._false_true_false(
            self.qclass(.1, .1, .1, .1, .1, .1, .1, .1, .1, .1).fsum(),
            self.assertEqual,
            1.0,
        )

    def test_average(self):
        self._false_true_false(
            self.qclass(10, 40, 45).average(),
            self.assertEqual,
            31.666666666666668,
        )

    def test_uncommon(self):
        self._false_true_false(
            self.qclass(11, 3, 5, 11, 7, 3, 11).uncommon(),
            self.assertEqual,
            7,
        )

    def test_frequency(self):
        self._false_true_false(
            self.qclass(11, 3, 5, 11, 7, 3, 11).frequency(),
            self.assertEqual,
            [(11, 3), (3, 2), (5, 1), (7, 1)],
        )

    def test_statrange(self):
        self._false_true_false(
            self.qclass(3, 5, 7, 3, 11).statrange(),
            self.assertEqual,
            8,
        )


class MTruthQMixin(object):

    def test_all(self):
        self._false_true_false(
            self.qclass(True, 1, None, 'yes').tap(bool).all(),
            self.assertFalse,
        )

    def test_any(self):
        self._false_true_false(
            self.qclass(None, 0, 'yes', False).tap(bool).any(),
            self.assertTrue,
        )

    def test_include(self):
        self._false_true_false(
            self.qclass(1, 2, 3).contains(3), self.assertTrue,
        )

    def test_quantify(self):
        self._false_true_false(
            self.qclass(True, 1, None, 'yes').tap(bool).quantify(),
            self.assertEqual,
            3,
        )
        self._false_true_false(
            self.qclass(None, 0, 'yes', False).tap(bool).quantify(),
            self.assertEqual,
            1,
        )


class MReduceQMixin(MMathQMixin, MTruthQMixin):

    def test_smash(self):
        self._false_true_false(
            self.qclass([[1, [2], [3, [[4]]]]]).smash(),
            self.assertEqual,
            [1, 2, 3, 4],
        )

    def test_merge(self):
        self._false_true_false(
            self.qclass([4, 5, 6], [1, 2, 3]).merge(),
            self.assertEqual,
            [1, 2, 3, 4, 5, 6],
        )

    def test_pairwise(self):
        self._false_true_false(
            self.qclass(
                'moe', 30, True, 'larry', 40, False, 'curly', 50, 1, 1,
            ).pairwise(),
            self.assertEqual,
            [('moe', 30), (30, True), (True, 'larry'), ('larry', 40),
            (40, False), (False, 'curly'), ('curly', 50), (50, 1), (1, 1)]
        )

    def test_reduce(self):
        self._false_true_false(
            self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce(),
            self.assertEqual,
            6,
        )
        self._false_true_false(
            self.qclass(1, 2, 3).tap(lambda x, y: x + y).reduce(1),
            self.assertEqual,
            7,
        )

    def test_reduce_right(self):
        self._false_true_false(
            self.qclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce_right(),
            self.assertEqual,
             [4, 5, 2, 3, 0, 1],
        )
        self._false_true_false(
            self.qclass([0, 1], [2, 3], [4, 5]).tap(
                lambda x, y: x + y
            ).reduce_right([0, 0]),
            self.assertEqual,
            [4, 5, 2, 3, 0, 1, 0, 0],
        )

    def test_roundrobin(self):
        self._false_true_false(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]
            ).roundrobin(),
            self.assertEqual,
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )

    def test_zip(self):
        self._true_true_false(
            self.qclass(
                ['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False],
            ).zip(),
            self.assertEqual,
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
