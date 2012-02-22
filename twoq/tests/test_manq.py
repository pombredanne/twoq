# -*- coding: utf-8 -*-
'''test manq'''

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestManQ(unittest.TestCase):

    '''test manq'''

    def setUp(self):
        from twoq import manq
        self.qclass = manq

    ###########################################################################
    ## queue manipulation #####################################################
    ###########################################################################

    def test_wrap(self):
        from stuf import stuf
        self.assertDictEqual(
            self.qclass(
                [('a', 1), ('b', 2), ('c', 3)]
            ).reup().wrap(stuf).map().sync().value(),
            stuf(a=1, b=2, c=3),
        )

    def test_delitem(self):
        q = self.qclass([1, 2, 3, 4, 5, 6])
        del q[2]
        self.assertEquals(q.swap().value(), [1, 2, 4, 5, 6])

    def test_remove(self):
        self.assertEquals(
            self.qclass([1, 2, 3, 4, 5, 6]).remove(5).swap().value(),
            [1, 2, 3, 4, 6],
        )

    def test_insert(self):
        q = self.qclass([1, 2, 3, 4, 5, 6])
        q.insert(2, 10)
        self.assertEquals(q.swap().value(), [1, 2, 10, 4, 5, 6])

    def test_extend(self):
        self.assertEquals(
            self.qclass().extend([1, 2, 3, 4, 5, 6]).swap().value(),
            [1, 2, 3, 4, 5, 6],
        )

    def test_extendleft(self):
        self.assertEquals(
            self.qclass().extendleft([1, 2, 3, 4, 5, 6]).swap().value(),
            [6, 5, 4, 3, 2, 1]
        )

    def test_append(self):
        self.assertEquals(
            self.qclass().append('foo').swap().value(), 'foo'
        )

    def test_appendleft(self):
        self.assertEquals(
            self.qclass().appendleft('foo').swap().value(), 'foo'
        )

    def test_inclear(self):
        self.assertEqual(len(self.qclass([1, 2, 5, 6]).inclear()), 0)

    def test_outclear(self):
        self.assertEqual(len(self.qclass([1, 2, 5, 6]).outclear().outgoing), 0)

    ###########################################################################
    ## queue balancing ########################################################
    ###########################################################################

    def test_insync(self):
        q = self.qclass([1, 2, 3, 4, 5, 6]).outshift().inclear().shift()
        self.assertSequenceEqual(q.incoming, q.outgoing)

    def test_inshift(self):
        q = self.qclass([1, 2, 3, 4, 5, 6]).outshift().sync()
        self.assertSequenceEqual(q.incoming, q.outgoing)

    def test_outsync(self):
        q = self.qclass([1, 2, 3, 4, 5, 6]).outshift()
        self.assertSequenceEqual(q.incoming, q.outgoing)

    def test_outshift(self):
        q = self.qclass([1, 2, 3, 4, 5, 6]).outsync()
        self.assertSequenceEqual(q.incoming, q.outgoing)

    ###########################################################################
    ## queue information ######################################################
    ###########################################################################

    def test_index(self):
        self.assertEquals(self.qclass([1, 2, 3, 4, 5, 6]).index(3), 2)

    def test_results(self):
        self.assertEquals(
            list(self.qclass([1, 2, 3, 4, 5, 6]).outsync().results()),
            [1, 2, 3, 4, 5, 6]
        )

    def test_contains(self):
        self.assertTrue(5 in self.qclass([1, 2, 3, 4, 5, 6]))

    ##########################################################################
    ## filter ################################################################
    ##########################################################################

    def test_filter(self):
        manq = self.qclass(
            [1, 2, 3, 4, 5, 6]
        ).tap(lambda x: x % 2 == 0).filter()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), [2, 4, 6])
        self.assertTrue(manq.balanced)

    def test_find(self):
        manq = self.qclass([1, 2, 3, 4, 5, 6]).tap(lambda x: x % 2 == 0).find()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), 2)
        self.assertTrue(manq.balanced)

    def test_reject(self):
        manq = self.qclass(
            [1, 2, 3, 4, 5, 6]
        ).tap(lambda x: x % 2 == 0).reject()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), [1, 3, 5])
        self.assertTrue(manq.balanced)

    def test_partition(self):
        manq = self.qclass(
            [1, 2, 3, 4, 5, 6]
        ).tap(lambda x: x % 2 == 0).partition()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), [[1, 3, 5], [2, 4, 6]])
        self.assertTrue(manq.balanced)

    ##########################################################################
    ## execution #############################################################
    ##########################################################################

    def test_each(self):
        def test(*args, **kw):
            return sum(args) * kw['a']
        manq = self.qclass(
            [((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})]
        ).tap(test).each()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), [6, 10, 14])
        self.assertTrue(manq.balanced)

    def test_map(self):
        manq = self.qclass([1, 2, 3]).tap(lambda x: x * 3).map()
        self.assertFalse(manq.balanced)
        self.assertEquals(list(manq.sync()), [3, 6, 9])
        self.assertTrue(manq.balanced)

    def test_invoke(self):
        manq = self.qclass([5, 1, 7], [3, 2, 1]).args(1).invoke('index')
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), [1, 2])
        self.assertTrue(manq.balanced)
        manq = self.qclass([5, 1, 7], [3, 2, 1]).invoke('sort')
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), [[1, 5, 7], [1, 2, 3]])
        self.assertTrue(manq.balanced)

    ##########################################################################
    ## delayed execution #####################################################
    ##########################################################################

    def test_delay_each(self):
        def test(*args, **kw):
            return sum(args) * kw['a']
        manq = self.qclass(
            [((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})]
        ).tap(test).delay_each(1)
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), [6, 10, 14])
        self.assertTrue(manq.balanced)

    def test_delay_map(self):
        manq = self.qclass([1, 2, 3]).tap(lambda x: x * 3).delay_map(1)
        self.assertFalse(manq.balanced)
        self.assertEquals(list(manq.sync()), [3, 6, 9])
        self.assertTrue(manq.balanced)

    def test_delay_invoke(self):
        manq = self.qclass(
            [5, 1, 7], [3, 2, 1]
        ).args(1).delay_invoke('index', 1)
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), [1, 2])
        self.assertTrue(manq.balanced)
        manq = self.qclass([5, 1, 7], [3, 2, 1]).invoke('sort')
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), [[1, 5, 7], [1, 2, 3]])
        self.assertTrue(manq.balanced)

    ##########################################################################
    ## reduction #############################################################
    ##########################################################################

    def test_flatten(self):
        manq = self.qclass([[1], [2], [3, [[4]]]]).flatten()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), [1, 2, 3, [[4]]])
        self.assertTrue(manq.balanced)

    def test_smash(self):
        manq = self.qclass([[1, [2], [3, [[4]]]]]).smash()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), [1, 2, 3, 4])
        self.assertTrue(manq.balanced)

    def test_merge(self):
        manq = self.qclass([4, 5, 6], [1, 2, 3]).merge()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), [1, 2, 3, 4, 5, 6])
        self.assertTrue(manq.balanced)

    def test_pairwise(self):
        manq = self.qclass(
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, 1, 1],
        ).pairwise()
        self.assertFalse(manq.balanced)
        self.assertEquals(
            manq.sync().value(),
            [('moe', 30), (30, True), (True, 'larry'), ('larry', 40),
            (40, False), (False, 'curly'), ('curly', 50), (50, 1), (1, 1)]
        )
        self.assertTrue(manq.balanced)

    def test_reduce(self):
        manq = self.qclass([1, 2, 3]).tap(lambda x, y: x + y).reduce()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), 6)
        self.assertTrue(manq.balanced)
        manq = self.qclass([1, 2, 3]).tap(lambda x, y: x + y).reduce(1)
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), 7)
        self.assertTrue(manq.balanced)

    def test_reduce_right(self):
        manq = self.qclass([[0, 1], [2, 3], [4, 5]]).tap(
            lambda x, y: x + y
        ).reduce_right()
        self.assertFalse(manq.balanced)
        self.assertEquals(
            manq.sync().value(), [4, 5, 2, 3, 0, 1],
        )
        self.assertTrue(manq.balanced)
        manq = self.qclass([[0, 1], [2, 3], [4, 5]]).tap(
            lambda x, y: x + y
        ).reduce_right([0, 0])
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), [4, 5, 2, 3, 0, 1, 0, 0])
        self.assertTrue(manq.balanced)

    def test_roundrobin(self):
        manq = self.qclass(
            [['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]]
        ).roundrobin()
        self.assertFalse(manq.balanced)
        self.assertEquals(
            manq.sync().value(),
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )
        self.assertTrue(manq.balanced)

    def test_zip(self):
        manq = self.qclass(
            [['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]]
        ).zip()
        self.assertFalse(manq.balanced)
        self.assertEquals(
            manq.sync().value(),
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )
        self.assertTrue(manq.balanced)

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
        manq = self.qclass(stooges).tap(lambda x: x.age).max()
        self.assertFalse(manq.balanced)
        self.assertEquals(
            stuf(manq.sync().value()), stuf(name='curly', age=60),
        )
        self.assertTrue(manq.balanced)
        manq = self.qclass([1, 2, 4]).max()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), 4)
        self.assertTrue(manq.balanced)

    def test_min(self):
        manq = self.qclass([10, 5, 100, 2, 1000]).min()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), 2)
        self.assertTrue(manq.balanced)
        manq = self.qclass([10, 5, 100, 2, 1000]).tap(lambda x: x).min()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), 2)
        self.assertTrue(manq.balanced)

    def test_sum(self):
        manq = self.qclass([1, 2, 3]).sum()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), 6)
        self.assertTrue(manq.balanced)
        manq = self.qclass([1, 2, 3]).sum(1)
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), 7)
        self.assertTrue(manq.balanced)

    def test_fsum(self):
        manq = self.qclass([.1, .1, .1, .1, .1, .1, .1, .1, .1, .1]).fsum()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), 1.0)
        self.assertTrue(manq.balanced)

    def test_average(self):
        manq = self.qclass([10, 40, 45]).average()
        self.assertFalse(manq.balanced)
        self.assertEquals(manq.sync().value(), 31.666666666666668)
        self.assertTrue(manq.balanced)

    ##########################################################################
    ## order #################################################################
    ##########################################################################

    def test_group(self,):
        from math import floor
        manq = self.qclass([1.3, 2.1, 2.4]).tap(lambda x: floor(x)).group()
        self.assertFalse(manq.balanced)
        self.assertEquals(
            manq.sync().value(), [[1.0, [1.3]], [2.0, [2.1, 2.4]]]
        )
        self.assertTrue(manq.balanced)
        manq = self.qclass([1.3, 2.1, 2.4]).group()
        self.assertFalse(manq.balanced)
        self.assertEquals(
            manq.sync().value(), [[1.3, [1.3]], [2.1, [2.1]], [2.4, [2.4]]],
        )
        self.assertTrue(manq.balanced)

    def test_grouper(self):
        manq = self.qclass(
            ['moe', 'larry', 'curly', 30, 40, 50, True]
        ).grouper(2, 'x')
        self.assertFalse(manq.balanced)
        self.assertEquals(
            manq.sync().value(),
            [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]
        )
        self.assertTrue(manq.balanced)

    def test_reversed(self):
        manq = self.qclass([5, 4, 3, 2, 1]).reverse()
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [1, 2, 3, 4, 5])
        self.assertTrue(manq.balanced)

    def test_sort(self):
        from math import sin
        manq = self.qclass([1, 2, 3, 4, 5, 6]).tap(lambda x: sin(x)).sort()
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [5, 4, 6, 3, 1, 2])
        self.assertTrue(manq.balanced)

    ##########################################################################
    ## random ################################################################
    ##########################################################################

    def test_choice(self):
        manq = self.qclass([1, 2, 3, 4, 5, 6]).choice()
        self.assertFalse(manq.balanced)
        self.assertEqual(len(manq.sync()), 1)
        self.assertTrue(manq.balanced)

    def test_sample(self):
        manq = self.qclass([1, 2, 3, 4, 5, 6]).sample(3)
        self.assertFalse(manq.balanced)
        self.assertEqual(len(manq.sync().value()), 3)
        self.assertTrue(manq.balanced)

    def test_shuffle(self):
        from collections import deque
        manq = self.qclass([1, 2, 3, 4, 5, 6]).shuffle()
        self.assertNotEqual(manq.outgoing, manq.incoming)
        self.assertEqual(len(manq.sync()), len([5, 4, 6, 3, 1, 2]))
        self.assertSequenceEqual(manq.outgoing, manq.incoming, deque)

    ##########################################################################
    ## single slice ##########################################################
    ##########################################################################

    def test_first(self):
        manq = self.qclass([5, 4, 3, 2, 1]).first()
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), 5)
        self.assertTrue(manq.balanced)

    def test_nth(self):
        manq = self.qclass([5, 4, 3, 2, 1]).nth(2)
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), 3)
        self.assertTrue(manq.balanced)
        manq = self.qclass([5, 4, 3, 2, 1]).nth(10, 11)
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), 11)
        self.assertTrue(manq.balanced)

    def test_last(self):
        manq = self.qclass([5, 4, 3, 2, 1]).last()
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), 1)
        self.assertTrue(manq.balanced)

    ##########################################################################
    ## large slice ###########################################################
    ##########################################################################

    def test_initial(self):
        manq = self.qclass([5, 4, 3, 2, 1]).initial()
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [5, 4, 3, 2])
        self.assertTrue(manq.balanced)

    def test_rest(self):
        manq = self.qclass([5, 4, 3, 2, 1]).rest()
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [4, 3, 2, 1])
        self.assertTrue(manq.balanced)

    def test_take(self):
        manq = self.qclass([5, 4, 3, 2, 1]).take(2)
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [5, 4])
        self.assertTrue(manq.balanced)

    def test_takeback(self):
        manq = self.qclass([5, 4, 3, 2, 1]).snatch(2)
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [2, 1])
        self.assertTrue(manq.balanced)

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
            [stooges, stoog2, stoog3]
        ).tap(test).members().detap().sort()
        self.assertFalse(manq.balanced)
        self.assertEqual(
            manq.sync().value(),
            [('age', 40), ('age', 50), ('age', 60),
            ('name', 'curly'), ('name', 'larry'), ('name', 'moe')],
        )
        self.assertTrue(manq.balanced)

    def test_pick(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        manq = self.qclass(stooges).pick('name')
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), ['moe', 'larry', 'curly'])
        self.assertTrue(manq.balanced)
        manq = self.qclass(stooges).pick('name', 'age')
        self.assertFalse(manq.balanced)
        self.assertEqual(
            manq.sync().value(), [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self.assertTrue(manq.balanced)
        manq = self.qclass(stooges).pick('place')
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [])
        self.assertTrue(manq.balanced)

    def test_pluck(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        manq = self.qclass(stooges).pluck('name')
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), ['moe', 'larry', 'curly'])
        self.assertTrue(manq.balanced)
        manq = self.qclass(stooges).pluck('name', 'age')
        self.assertFalse(manq.balanced)
        self.assertEqual(
            manq.sync().value(), [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self.assertTrue(manq.balanced)
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        manq = self.qclass(stooges).pluck(0)
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), ['moe', 'larry', 'curly'])
        self.assertTrue(manq.balanced)
        manq = self.qclass(stooges).pluck(1)
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [40, 50, 60])
        self.assertTrue(manq.balanced)
        manq = self.qclass(stooges).pluck('place')
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [])
        self.assertTrue(manq.balanced)

    ##########################################################################
    ## repetition ############################################################
    ##########################################################################

    def test_range(self):
        manq = self.qclass().range(3)
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [0, 1, 2])
        self.assertTrue(manq.balanced)
        manq = self.qclass().range(1, 3)
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [1, 2])
        self.assertTrue(manq.balanced)
        manq = self.qclass().range(1, 3, 2)
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), 1)
        self.assertTrue(manq.balanced)

    def test_repeat(self):
        manq = self.qclass([40, 50, 60]).repeat(3)
        self.assertFalse(manq.balanced)
        self.assertEqual(
            manq.sync().value(), [(40, 50, 60), (40, 50, 60), (40, 50, 60)],
        )
        self.assertTrue(manq.balanced)

    def test_times(self):
        def test(*args):
            return list(args)
        manq = self.qclass(40, 50, 60).tap(test).times(3)
        self.assertFalse(manq.balanced)
        self.assertEqual(
            manq.sync().value(), [[40, 50, 60], [40, 50, 60], [40, 50, 60]],
        )
        self.assertTrue(manq.balanced)

    ##########################################################################
    ## truth #################################################################
    ##########################################################################

    def test_all(self):
        manq = self.qclass([True, 1, None, 'yes']).tap(bool).all()
        self.assertFalse(manq.balanced)
        self.assertFalse(manq.sync().value())
        self.assertTrue(manq.balanced)

    def test_any(self):
        manq = self.qclass([None, 0, 'yes', False]).tap(bool).any()
        self.assertFalse(manq.balanced)
        self.assertTrue(manq.sync().value())
        self.assertTrue(manq.balanced)

    def test_include(self):
        manq = self.qclass([1, 2, 3]).contains(3)
        self.assertFalse(manq.balanced)
        self.assertTrue(manq.sync().value())
        self.assertTrue(manq.balanced)

    def test_quantify(self):
        manq = self.qclass([True, 1, None, 'yes']).tap(bool).quantify()
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), 3)
        self.assertTrue(manq.balanced)
        manq = self.qclass([None, 0, 'yes', False]).tap(bool).quantify()
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), 1)
        self.assertTrue(manq.balanced)

    ##########################################################################
    ## strip #################################################################
    ##########################################################################

    def test_compact(self):
        manq = self.qclass([0, 1, False, 2, '', 3]).compact()
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [1, 2, 3])
        self.assertTrue(manq.balanced)

    def test_without(self):
        manq = self.qclass([1, 2, 1, 0, 3, 1, 4]).without(0, 1)
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [2, 3, 4])
        self.assertTrue(manq.balanced)

    ##########################################################################
    ## unique slice ##########################################################
    ##########################################################################

    def test_difference(self):
        manq = self.qclass([[1, 2, 3, 4, 5], [5, 2, 10]]).difference()
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [1, 3, 4])
        self.assertTrue(manq.balanced)

    def test_intersection(self):
        manq = self.qclass([[1, 2, 3], [101, 2, 1, 10], [2, 1]]).intersection()
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [1, 2])
        self.assertTrue(manq.balanced)

    def test_union(self):
        manq = self.qclass([[1, 2, 3], [101, 2, 1, 10], [2, 1]]).union()
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [1, 2, 3, 101, 10])
        self.assertTrue(manq.balanced)

    def test_unique(self):
        manq = self.qclass([1, 2, 1, 3, 1, 4]).unique()
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [1, 2, 3, 4])
        self.assertTrue(manq.balanced)
        manq = self.qclass([1, 2, 1, 3, 1, 4]).tap(round).unique()
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.sync().value(), [1, 2, 3, 4])
        self.assertTrue(manq.balanced)


if __name__ == '__main__':
    import cProfile
    cProfile.run('unittest.main()')
