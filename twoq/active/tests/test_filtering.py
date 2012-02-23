# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestAutoFilteringQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.filtering import filteringq
        self.qclass = filteringq

    ##########################################################################
    ## filter ################################################################
    ##########################################################################

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

    ##########################################################################
    ## single slice ##########################################################
    ##########################################################################

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

    ##########################################################################
    ## large slice ###########################################################
    ##########################################################################

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

    ##########################################################################
    ## collection ############################################################
    ##########################################################################

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
        test = lambda x: not x.startswith('__')
        self.assertEqual(
            self.qclass(
                stooges, stoog2, stoog3
            ).tap(test).members().detap().value(),
            [('age', 40), ('name', 'moe'), ('age', 50), ('name', 'larry'),
            ('age', 60), ('name', 'curly')],
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

    ##########################################################################
    ## strip #################################################################
    ##########################################################################

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

    ##########################################################################
    ## unique slice ##########################################################
    ##########################################################################

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


class TestAutoFilterQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.filtering import filterq
        self.qclass = filterq

    ##########################################################################
    ## filter ################################################################
    ##########################################################################

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
        
    ##########################################################################
    ## strip #################################################################
    ##########################################################################

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


class TestAutoSliceQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.filtering import sliceq
        self.qclass = sliceq

    ##########################################################################
    ## single slice ##########################################################
    ##########################################################################

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

    ##########################################################################
    ## large slice ###########################################################
    ##########################################################################

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


class TestAutoCollectQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.filtering import collectq
        self.qclass = collectq

    ##########################################################################
    ## collection ############################################################
    ##########################################################################

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
        test = lambda x: not x.startswith('__')
        self.assertEqual(
            self.qclass(
                stooges, stoog2, stoog3
            ).tap(test).members().detap().value(),
            [('age', 40), ('name', 'moe'), ('age', 50), ('name', 'larry'),
            ('age', 60), ('name', 'curly')],
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


class TestAutoSetQ(unittest.TestCase):

    '''test automatically synchronized filtering'''

    def setUp(self):
        from twoq.active.filtering import setq
        self.qclass = setq

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


class TestManualFilteringQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.filtering import manfilteringq
        self.qclass = manfilteringq

    ##########################################################################
    ## filter ################################################################
    ##########################################################################

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

    ##########################################################################
    ## single slice ##########################################################
    ##########################################################################

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

    ##########################################################################
    ## large slice ###########################################################
    ##########################################################################

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

    ##########################################################################
    ## collection ############################################################
    ##########################################################################

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
        test = lambda x: not x.startswith('__')
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

    ##########################################################################
    ## strip #################################################################
    ##########################################################################

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

    ##########################################################################
    ## unique slice ##########################################################
    ##########################################################################

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


class TestManualFilterQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.filtering import manfilterq
        self.qclass = manfilterq

    ##########################################################################
    ## filter ################################################################
    ##########################################################################

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

    ##########################################################################
    ## strip #################################################################
    ##########################################################################

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


class TestManSliceQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.filtering import mansliceq
        self.qclass = mansliceq

    ##########################################################################
    ## single slice ##########################################################
    ##########################################################################

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

    ##########################################################################
    ## large slice ###########################################################
    ##########################################################################

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


class TestManCollectQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.filtering import mancollectq
        self.qclass = mancollectq

    ##########################################################################
    ## collection ############################################################
    ##########################################################################

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
        test = lambda x: not x.startswith('__')
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


class TestManSetQ(unittest.TestCase):

    def setUp(self):
        from twoq.active.filtering import mansetq
        self.qclass = mansetq

    ##########################################################################
    ## unique slice ##########################################################
    ##########################################################################

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

if __name__ == '__main__':
    import cProfile
    cProfile.run('unittest.main()')
