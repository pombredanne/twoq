# -*- coding: utf-8 -*-
'''test AutoQMixin'''

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestAutoMapping(unittest.TestCase):

    '''test AutoQMixin'''

    def setUp(self):
        from twoq.active.mapping import mappingq
        self.qclass = mappingq

    ###########################################################################
    ## queue balancing ########################################################
    ###########################################################################

    def test_copy(self):
        testlist = [[1, 2, 3], [4, 5, 6]]
        newlist = self.qclass(testlist).copy().value()
        self.assertFalse(newlist is testlist)
        self.assertListEqual(newlist, testlist)
        self.assertTrue(newlist[0] is testlist[0])
        self.assertListEqual(newlist[0], testlist[0])
        self.assertTrue(newlist[1] is testlist[1])
        self.assertListEqual(newlist[1], testlist[1])

    def test_deepcopy(self):
        testlist = [[1, [2, 3]], [4, [5, 6]]]
        newlist = self.qclass(testlist).deepcopy().value()
        self.assertFalse(newlist is testlist)
        self.assertListEqual(newlist, testlist)
        self.assertFalse(newlist[0] is testlist[0])
        self.assertListEqual(newlist[0], testlist[0])
        self.assertFalse(newlist[1] is testlist[1])
        self.assertListEqual(newlist[1], testlist[1])

    ##########################################################################
    ## execution #############################################################
    ##########################################################################

    def test_each(self):
        def test(*args, **kw):
            return sum(args) * kw['a']
        self.assertEquals(
            self.qclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).tap(test).each().value(),
            [6, 10, 14],
        )

    def test_map(self):
        self.assertEquals(
            self.qclass(1, 2, 3).tap(lambda x: x * 3).map().value(), [3, 6, 9],
        )

    def test_invoke(self):
        self.assertEquals(
            self.qclass([5, 1, 7], [3, 2, 1]).args(1).invoke('index').value(),
            [1, 2],
        )
        self.assertEquals(
            self.qclass([5, 1, 7], [3, 2, 1]).invoke('sort').value(),
            [[1, 5, 7], [1, 2, 3]],
        )

    ##########################################################################
    ## repetition ############################################################
    ##########################################################################

    def test_range(self):
        self.assertEqual(self.qclass().range(3).value(), [0, 1, 2])
        self.assertEqual(self.qclass().range(1, 3).value(), [1, 2])
        self.assertEqual(self.qclass().range(1, 3, 2).value(), 1)

    def test_repeat(self):
        self.assertEqual(
            self.qclass(40, 50, 60).repeat(3).value(),
            [(40, 50, 60), (40, 50, 60), (40, 50, 60)],
        )

    def test_times(self):
        def test(*args):
            return list(args)
        self.assertEqual(
            self.qclass(40, 50, 60).tap(test).times(3).value(),
            [[40, 50, 60], [40, 50, 60], [40, 50, 60]],
        )

    ##########################################################################
    ## delayed execution #####################################################
    ##########################################################################

    def test_delay_each(self):
        def test(*args, **kw):
            return sum(args) * kw['a']
        self.assertEquals(
            self.qclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            )
            .tap(test)
            .delay_each(0.5)
            .value(),
            [6, 10, 14],
        )

    def test_delay_map(self):
        self.assertEquals(
            self.qclass(1, 2, 3).tap(lambda x: x * 3).delay_map(0.5).value(),
            [3, 6, 9],
        )

    def test_delay_invoke(self):
        self.assertEquals(
            self.qclass([5, 1, 7], [3, 2, 1])
            .args(1)
            .delay_invoke('index', 0.5)
            .value(),
            [1, 2],
        )
        self.assertEquals(
            self.qclass([5, 1, 7], [3, 2, 1])
            .delay_invoke('sort', 0.5).value(),
            [[1, 5, 7], [1, 2, 3]],
        )


class TestManQ(unittest.TestCase):

    '''test manq'''

    def setUp(self):
        from twoq.active.mapping import mappingq
        self.qclass = mappingq

    ##########################################################################
    ## execution #############################################################
    ##########################################################################

    def test_each(self):
        def test(*args, **kw):
            return sum(args) * kw['a']
        manq = self.qclass(
            ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
        ).tap(test).each()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [6, 10, 14])
        self.assertFalse(manq.balanced)

    def test_map(self):
        manq = self.qclass(1, 2, 3).tap(lambda x: x * 3).map()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [3, 6, 9])
        self.assertFalse(manq.balanced)

    def test_invoke(self):
        manq = self.qclass([5, 1, 7], [3, 2, 1]).args(1).invoke('index')
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [1, 2])
        self.assertFalse(manq.balanced)
        manq = self.qclass([5, 1, 7], [3, 2, 1]).invoke('sort')
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [[1, 5, 7], [1, 2, 3]])
        self.assertFalse(manq.balanced)

    ###########################################################################
    ## queue balancing ########################################################
    ###########################################################################

    def test_copy(self):
        testlist = [[1, 2, 3], [4, 5, 6]]
        manq = self.qclass(testlist).copy()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        newlist = manq.value()
        self.assertFalse(newlist is testlist)
        self.assertListEqual(newlist, testlist)
        self.assertTrue(newlist[0] is testlist[0])
        self.assertListEqual(newlist[0], testlist[0])
        self.assertTrue(newlist[1] is testlist[1])
        self.assertListEqual(newlist[1], testlist[1])
        self.assertFalse(manq.balanced)

    def test_deepcopy(self):
        testlist = [[1, [2, 3]], [4, [5, 6]]]
        manq = self.qclass(testlist).deepcopy()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        newlist = manq.value()
        self.assertFalse(newlist is testlist)
        self.assertListEqual(newlist, testlist)
        self.assertFalse(newlist[0] is testlist[0])
        self.assertListEqual(newlist[0], testlist[0])
        self.assertFalse(newlist[1] is testlist[1])
        self.assertListEqual(newlist[1], testlist[1])
        self.assertFalse(manq.balanced)

    ##########################################################################
    ## repetition ############################################################
    ##########################################################################

    def test_range(self):
        manq = self.qclass().range(3)
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [0, 1, 2])
        self.assertFalse(manq.balanced)
        manq = self.qclass().range(1, 3)
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), [1, 2])
        self.assertFalse(manq.balanced)
        manq = self.qclass().range(1, 3, 2)
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(manq.value(), 1)
        self.assertFalse(manq.balanced)

    def test_repeat(self):
        manq = self.qclass(40, 50, 60).repeat(3)
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(
            manq.value(), [(40, 50, 60), (40, 50, 60), (40, 50, 60)],
        )
        self.assertFalse(manq.balanced)

    def test_times(self):
        def test(*args):
            return list(args)
        manq = self.qclass(40, 50, 60).tap(test).times(3)
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(
            manq.value(), [[40, 50, 60], [40, 50, 60], [40, 50, 60]],
        )
        self.assertFalse(manq.balanced)

    ##########################################################################
    ## delayed execution #####################################################
    ##########################################################################

    def test_delay_each(self):
        def test(*args, **kw):
            return sum(args) * kw['a']
        manq = self.qclass(
            ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
        ).tap(test).delay_each(0.5)
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [6, 10, 14])
        self.assertFalse(manq.balanced)

    def test_delay_map(self):
        manq = self.qclass(1, 2, 3).tap(lambda x: x * 3).delay_map(0.5)
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [3, 6, 9])
        self.assertFalse(manq.balanced)

    def test_delay_invoke(self):
        manq = self.qclass(
            [5, 1, 7], [3, 2, 1]
        ).args(1).delay_invoke('index', 0.5)
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [1, 2])
        self.assertFalse(manq.balanced)
        manq = self.qclass([5, 1, 7], [3, 2, 1]).invoke('sort')
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEquals(manq.value(), [[1, 5, 7], [1, 2, 3]])
        self.assertFalse(manq.balanced)


if __name__ == '__main__':
    import cProfile
    cProfile.run('unittest.main()')
