# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestAutoOrderingQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.ordering import orderingq
        self.qclass = orderingq

    ##########################################################################
    ## order #################################################################
    ##########################################################################

    def test_group(self,):
        from math import floor
        self.assertEquals(
        self.qclass(1.3, 2.1, 2.4).tap(lambda x: floor(x)).group().value(),
            [[1.0, [1.3]], [2.0, [2.1, 2.4]]]
        )
        self.assertEquals(
            self.qclass(1.3, 2.1, 2.4).group().value(),
            [[1.3, [1.3]], [2.1, [2.1]], [2.4, [2.4]]],
        )

    def test_grouper(self):
        self.assertEquals(
            self.qclass(
                'moe', 'larry', 'curly', 30, 40, 50, True
            ).grouper(2, 'x').value(),
             [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]
        )

    def test_reversed(self):
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).reverse().value(), [1, 2, 3, 4, 5],
        )

    def test_sort(self):
        from math import sin
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: sin(x)
            ).sort().value(),
            [5, 4, 6, 3, 1, 2],
        )

    ##########################################################################
    ## random ################################################################
    ##########################################################################

    def test_choice(self):
        self.assertEqual(
            len(self.qclass(1, 2, 3, 4, 5, 6).choice()), 1,
        )

    def test_sample(self):
        self.assertEqual(
            len(self.qclass(1, 2, 3, 4, 5, 6).sample(3).value()), 3,
        )

    def test_shuffle(self):
        self.assertEqual(
            len(self.qclass(1, 2, 3, 4, 5, 6).shuffle()),
            len([5, 4, 6, 3, 1, 2]),
        )


class TestAutoOrderQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.ordering import orderq
        self.qclass = orderq

    ##########################################################################
    ## order #################################################################
    ##########################################################################

    def test_group(self,):
        from math import floor
        self.assertEquals(
        self.qclass(1.3, 2.1, 2.4).tap(lambda x: floor(x)).group().value(),
            [[1.0, [1.3]], [2.0, [2.1, 2.4]]]
        )
        self.assertEquals(
            self.qclass(1.3, 2.1, 2.4).group().value(),
            [[1.3, [1.3]], [2.1, [2.1]], [2.4, [2.4]]],
        )

    def test_grouper(self):
        self.assertEquals(
            self.qclass(
                'moe', 'larry', 'curly', 30, 40, 50, True
            ).grouper(2, 'x').value(),
             [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]
        )

    def test_reversed(self):
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).reverse().value(), [1, 2, 3, 4, 5],
        )

    def test_sort(self):
        from math import sin
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: sin(x)
            ).sort().value(),
            [5, 4, 6, 3, 1, 2],
        )


class TestAutoRandomQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.ordering import randomq
        self.qclass = randomq

    ##########################################################################
    ## random ################################################################
    ##########################################################################

    def test_choice(self):
        self.assertEqual(
            len(self.qclass(1, 2, 3, 4, 5, 6).choice()), 1,
        )

    def test_sample(self):
        self.assertEqual(
            len(self.qclass(1, 2, 3, 4, 5, 6).sample(3).value()), 3,
        )

    def test_shuffle(self):
        self.assertEqual(
            len(self.qclass(1, 2, 3, 4, 5, 6).shuffle()),
            len([5, 4, 6, 3, 1, 2]),
        )


class TestManOrderingQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.ordering import manorderingq
        self.qclass = manorderingq

    ##########################################################################
    ## order #################################################################
    ##########################################################################

    def test_group(self,):
        from math import floor
        manq = self.qclass(1.3, 2.1, 2.4).tap(lambda x: floor(x)).group()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(
            manq.value(), [[1.0, [1.3]], [2.0, [2.1, 2.4]]]
        )
        self.assertFalse(manq.balanced)
        manq = self.qclass(1.3, 2.1, 2.4).group()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(
            manq.value(), [[1.3, [1.3]], [2.1, [2.1]], [2.4, [2.4]]],
        )
        self.assertFalse(manq.balanced)

    def test_grouper(self):
        manq = self.qclass(
            'moe', 'larry', 'curly', 30, 40, 50, True
        ).grouper(2, 'x')
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(
            manq.value(),
            [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]
        )
        self.assertFalse(manq.balanced)

    def test_reversed(self):
        manq = self.qclass(5, 4, 3, 2, 1).reverse()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [1, 2, 3, 4, 5])
        self.assertFalse(manq.balanced)

    def test_sort(self):
        from math import sin
        manq = self.qclass(1, 2, 3, 4, 5, 6).tap(lambda x: sin(x)).sort()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [5, 4, 6, 3, 1, 2])
        self.assertFalse(manq.balanced)

    ##########################################################################
    ## random ################################################################
    ##########################################################################

    def test_choice(self):
        manq = self.qclass(1, 2, 3, 4, 5, 6).choice()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        manq.value()
        self.assertFalse(manq.balanced)

    def test_sample(self):
        manq = self.qclass(1, 2, 3, 4, 5, 6).sample(3)
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        manq.value()
        self.assertFalse(manq.balanced)

    def test_shuffle(self):
        manq = self.qclass(1, 2, 3, 4, 5, 6).shuffle()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        manq.value()
        self.assertFalse(manq.balanced)


class TestManOrderQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.ordering import manorderq
        self.qclass = manorderq

    ##########################################################################
    ## order #################################################################
    ##########################################################################

    def test_group(self,):
        from math import floor
        manq = self.qclass(1.3, 2.1, 2.4).tap(lambda x: floor(x)).group()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(
            manq.value(), [[1.0, [1.3]], [2.0, [2.1, 2.4]]]
        )
        self.assertFalse(manq.balanced)
        manq = self.qclass(1.3, 2.1, 2.4).group()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(
            manq.value(), [[1.3, [1.3]], [2.1, [2.1]], [2.4, [2.4]]],
        )
        self.assertFalse(manq.balanced)

    def test_grouper(self):
        manq = self.qclass(
            'moe', 'larry', 'curly', 30, 40, 50, True
        ).grouper(2, 'x')
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(
            manq.value(),
            [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]
        )
        self.assertFalse(manq.balanced)

    def test_reversed(self):
        manq = self.qclass(5, 4, 3, 2, 1).reverse()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [1, 2, 3, 4, 5])
        self.assertFalse(manq.balanced)

    def test_sort(self):
        from math import sin
        manq = self.qclass(1, 2, 3, 4, 5, 6).tap(lambda x: sin(x)).sort()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [5, 4, 6, 3, 1, 2])
        self.assertFalse(manq.balanced)


class TestManRandomQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.ordering import manrandomq
        self.qclass = manrandomq

    ##########################################################################
    ## random ################################################################
    ##########################################################################

    def test_choice(self):
        manq = self.qclass(1, 2, 3, 4, 5, 6).choice()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        manq.value()
        self.assertFalse(manq.balanced)

    def test_sample(self):
        manq = self.qclass(1, 2, 3, 4, 5, 6).sample(3)
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        manq.value()
        self.assertFalse(manq.balanced)

    def test_shuffle(self):
        manq = self.qclass(1, 2, 3, 4, 5, 6).shuffle()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        manq.value()
        self.assertFalse(manq.balanced)

if __name__ == '__main__':
    import cProfile
    cProfile.run('unittest.main()')
