# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestAutoReducingQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.reducing import reducingq
        self.qclass = reducingq

    ##########################################################################
    ## reduction #############################################################
    ##########################################################################

    def test_flatten(self):
        self.assertEquals(
            self.qclass([[1], [2], [3, [[4]]]]).flatten().value(),
            [[1], [2], [3, [[4]]]],
        )

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

    ##########################################################################
    ## math ##################################################################
    ##########################################################################

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
        self.assertEquals(
            self.qclass(10, 5, 100, 2, 1000).min().value(), 2,
        )
        self.assertEquals(
            self.qclass(10, 5, 100, 2, 1000).tap(lambda x: x).min().value(),
            2,
        )
        
    def test_median(self):
        self.assertEquals(self.qclass(4, 5, 7, 2, 1).median().value(), 4)
        self.assertEquals(self.qclass(4, 5, 7, 2, 1, 8).median().value(), 4.5)

    def test_mode(self):
        self.assertEquals(
            self.qclass(11, 3, 5, 11, 7, 3, 11).mode().value(), 11,
        )

    def test_sum(self):
        self.assertEquals(self.qclass(1, 2, 3).sum().value(), 6)
        self.assertEquals(self.qclass(1, 2, 3).sum(1).value(), 7)

    def test_fsum(self):
        self.assertEquals(
            self.qclass(.1, .1, .1, .1, .1, .1, .1, .1, .1, .1).fsum().value(),
            1.0,
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

    def test_average(self):
        self.assertEquals(
            self.qclass(10, 40, 45).average().value(), 31.666666666666668
        )

    ##########################################################################
    ## truth #################################################################
    ##########################################################################

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


class TestAutoReduceQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.reducing import reduceq
        self.qclass = reduceq

    ##########################################################################
    ## reduction #############################################################
    ##########################################################################

    def test_flatten(self):
        self.assertEquals(
            self.qclass([[1], [2], [3, [[4]]]]).flatten().value(),
            [[1], [2], [3, [[4]]]],
        )

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


class TestAutoMathQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.reducing import mathq
        self.qclass = mathq

    ##########################################################################
    ## math ##################################################################
    ##########################################################################

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


class TestAutoTruthQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.reducing import truthq
        self.qclass = truthq

    ##########################################################################
    ## truth #################################################################
    ##########################################################################

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


class TestManReducingQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.reducing import manreducingq
        self.qclass = manreducingq

    ##########################################################################
    ## reduction #############################################################
    ##########################################################################

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

    ##########################################################################
    ## math ##################################################################
    ##########################################################################

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
        
    def test_mode(self):
        manq = self.qclass(11, 3, 5, 11, 7, 3, 11).mode()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertEquals(manq.value(), 11)
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

    ##########################################################################
    ## truth #################################################################
    ##########################################################################

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


class TestManReduceQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.reducing import manreduceq
        self.qclass = manreduceq

    ##########################################################################
    ## reduction #############################################################
    ##########################################################################

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


class TestManMathQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.reducing import manmathq
        self.qclass = manmathq

    ##########################################################################
    ## math ##################################################################
    ##########################################################################

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


class TestManTruthQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.reducing import mantruthq
        self.qclass = mantruthq

    ##########################################################################
    ## truth #################################################################
    ##########################################################################

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


if __name__ == '__main__':
    import cProfile
    cProfile.run('unittest.main()')
