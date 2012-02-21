# -*- coding: utf-8 -*-
'''test twoq'''

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class TestTwoQ(unittest.TestCase):

    '''test twoq'''

    def setUp(self):
        from twoq import twoq
        self.qclass = twoq

    ##########################################################################
    ## queue management & execution ##########################################
    ##########################################################################

    def test_index(self):
        self.assertEquals(self.qclass([1, 2, 3, 4, 5, 6]).index(3), 2)

    def test_remove(self):
        self.assertEquals(
            self.qclass([1, 2, 3, 4, 5, 6]).remove(5).swap().value(),
            [1, 2, 3, 4, 6]
        )

    def test_results(self):
        self.assertEquals(
            list(self.qclass([1, 2, 3, 4, 5, 6]).outshift().results()),
            [1, 2, 3, 4, 5, 6]
        )

    def test_delitem(self):
        q = self.qclass([1, 2, 3, 4, 5, 6])
        del q[2]
        self.assertEquals(q.swap().value(), [1, 2, 4, 5, 6])

    def test_insync(self):
        q = self.qclass([1, 2, 3, 4, 5, 6]).outsync().inclear().insync()
        self.assertSequenceEqual(q.incoming, q.outgoing)

    def test_inshift(self):
        q = self.qclass([1, 2, 3, 4, 5, 6]).outsync().inshift()
        self.assertSequenceEqual(q.incoming, q.outgoing)

    def test_outsync(self):
        q = self.qclass([1, 2, 3, 4, 5, 6]).outsync()
        self.assertSequenceEqual(q.incoming, q.outgoing)

    def test_outshift(self):
        q = self.qclass([1, 2, 3, 4, 5, 6]).outshift()
        self.assertSequenceEqual(q.incoming, q.outgoing)

    def test_contains(self):
        self.assertTrue(5 in self.qclass([1, 2, 3, 4, 5, 6]))

    def test_inclear(self):
        self.assertEqual(len(self.qclass([1, 2, 5, 6]).inclear()), 0)

    def test_outclear(self):
        self.assertEqual(len(self.qclass([1, 2, 5, 6]).outclear().outgoing), 0)

    def test_insert(self):
        q = self.qclass([1, 2, 3, 4, 5, 6])
        q.insert(2, 10)
        self.assertEquals(q.swap().value(), [1, 2, 10, 4, 5, 6])

    def test_extend(self):
        self.assertEquals(
            self.qclass().extend([1, 2, 3, 4, 5, 6]).swap().value(),
            [1, 2, 3, 4, 5, 6]
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

    ##########################################################################
    ## filter ################################################################
    ##########################################################################

    def test_filter(self):
        self.assertEquals(
            self.qclass([1, 2, 3, 4, 5, 6]).tap(
                lambda x: x % 2 == 0
            ).filter().value(), [2, 4, 6]
        )

    def test_find(self):
        self.assertEquals(
            self.qclass([1, 2, 3, 4, 5, 6]).tap(
                lambda x: x % 2 == 0
            ).find().value(), 2,
        )

    def test_reject(self):
        self.assertEquals(
            self.qclass([1, 2, 3, 4, 5, 6]).tap(
                lambda x: x % 2 == 0
            ).reject().value(), [1, 3, 5]
        )

    ##########################################################################
    ## map ###################################################################
    ##########################################################################

    def test_each(self):
        def test(*args, **kw):
            return sum(args) * kw['a']
        self.assertEquals(
            self.qclass(
                [((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})]
            ).tap(test).each().value(),
            [6, 10, 14],
        )

    def test_map(self):
        self.assertEquals(
            list(self.qclass([1, 2, 3]).tap(lambda x: x * 3).map()), [3, 6, 9],
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

    def test_wrap(self):
        from stuf import stuf
        self.assertDictEqual(
            self.qclass(
                [('a', 1), ('b', 2), ('c', 3)]
            ).reup().wrap(stuf).map().value(),
            stuf(a=1, b=2, c=3),
        )

    ##########################################################################
    ## reduction #############################################################
    ##########################################################################

    def test_flatten(self):
        self.assertEquals(
            self.qclass([[1], [2], [3, [[4]]]]).flatten().value(),
            [1, 2, 3, [[4]]],
        )

    def test_max(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self.assertEquals(
            stuf(self.qclass(stooges).tap(lambda x: x.age).max().value()),
            stuf(name='curly', age=60),
        )
        self.assertEquals(
            self.qclass([1, 2, 4]).max().value(), 4,
        )

    def test_merge(self):
        self.assertEquals(
            self.qclass([[1, [2], [3, [[4]]]]]).smash().value(),
            [1, 2, 3, 4],
        )

    def test_min(self):
        self.assertEquals(
            self.qclass([10, 5, 100, 2, 1000]).min().value(), 2,
        )
        self.assertEquals(
            self.qclass([10, 5, 100, 2, 1000]).tap(lambda x: x).min().value(),
            2,
        )

    def test_pairwise(self):
        self.assertEquals(
            self.qclass(
                ['moe', 30, True, 'larry', 40, False, 'curly', 50, 1, 1],
            ).pairwise().value(),
            [('moe', 30), (30, True), (True, 'larry'), ('larry', 40),
            (40, False), (False, 'curly'), ('curly', 50), (50, 1), (1, 1)]
        )

    def test_reduce(self):
        self.assertEquals(
            self.qclass([1, 2, 3]).tap(lambda x, y: x + y).reduce().value(), 6,
        )
        self.assertEquals(
            self.qclass([1, 2, 3]).tap(lambda x, y: x + y).reduce(1).value(),
            7,
        )

    def test_reduce_right(self):
        self.assertEquals(
            self.qclass([[0, 1], [2, 3], [4, 5]]).tap(
                lambda x, y: x + y
            ).reduce_right().value(), [4, 5, 2, 3, 0, 1],
        )
        self.assertEquals(
            self.qclass([[0, 1], [2, 3], [4, 5]]).tap(
                lambda x, y: x + y
            ).reduce_right([0, 0]).value(), [4, 5, 2, 3, 0, 1, 0, 0],
        )

    def test_roundrobin(self):
        self.assertEquals(
            self.qclass(
                [['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]]
            ).roundrobin().value(),
            ['moe', 30, True, 'larry', 40, False, 'curly', 50, False],
        )

    def test_zip(self):
        self.assertEquals(
            self.qclass(
                [['moe', 'larry', 'curly'], [30, 40, 50], [True, False, False]]
            ).zip().value(),
            [('moe', 30, True), ('larry', 40, False), ('curly', 50, False)],
        )

    ##########################################################################
    ## order #################################################################
    ##########################################################################

    def test_group(self,):
        from math import floor
        self.assertEquals(
        self.qclass([1.3, 2.1, 2.4]).tap(lambda x: floor(x)).group().value(),
            [[1.0, [1.3]], [2.0, [2.1, 2.4]]]
        )
        self.assertEquals(
            self.qclass([1.3, 2.1, 2.4]).group().value(),
            [[1.3, [1.3]], [2.1, [2.1]], [2.4, [2.4]]],
        )

    def test_grouper(self):
        self.assertEquals(
            self.qclass(
                ['moe', 'larry', 'curly', 30, 40, 50, True]
            ).grouper(2, 'x').value(),
             [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]
        )

    def test_reversed(self):
        self.assertEqual(
            self.qclass(
                [5, 4, 3, 2, 1]
            ).reverse().value(), [1, 2, 3, 4, 5],
        )

    def test_sort(self):
        from math import sin
        self.assertEqual(
            self.qclass([1, 2, 3, 4, 5, 6]).tap(
                lambda x: sin(x)
            ).sort().value(),
            [5, 4, 6, 3, 1, 2],
        )

    ##########################################################################
    ## random ################################################################
    ##########################################################################

    def test_choice(self):
        self.assertEqual(
            len(self.qclass([1, 2, 3, 4, 5, 6]).choice()), 1,
        )

    def test_sample(self):
        self.assertEqual(
            len(self.qclass([1, 2, 3, 4, 5, 6]).sample(3).value()), 3,
        )

    def test_shuffle(self):
        self.assertEqual(
            len(self.qclass([1, 2, 3, 4, 5, 6]).shuffle()),
            len([5, 4, 6, 3, 1, 2]),
        )

    ##########################################################################
    ## single slice ##########################################################
    ##########################################################################

    def test_first(self):
        self.assertEqual(
            self.qclass([5, 4, 3, 2, 1]).first().value(), 5,
        )

    def test_nth(self):
        self.assertEqual(
            self.qclass([5, 4, 3, 2, 1]).nth(2).value(), 3,
        )
        self.assertEqual(
            self.qclass([5, 4, 3, 2, 1]).nth(10, 11).value(), 11,
        )

    def test_last(self):
        self.assertEqual(
            self.qclass([5, 4, 3, 2, 1]).last().value(), 1,
        )

    ##########################################################################
    ## large slice ###########################################################
    ##########################################################################

    def test_initial(self):
        self.assertEqual(
            self.qclass([5, 4, 3, 2, 1]).initial().value(), [5, 4, 3, 2]
        )

    def test_rest(self):
        self.assertEqual(
            self.qclass([5, 4, 3, 2, 1]).rest().value(), [4, 3, 2, 1]
        )

    def test_take(self):
        self.assertEqual(
            self.qclass([5, 4, 3, 2, 1]).take(2).value(), [5, 4]
        )

    def test_takeback(self):
        self.assertEqual(
            self.qclass([5, 4, 3, 2, 1]).snatch(2).value(), [2, 1]
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
                [stooges, stoog2, stoog3]
            ).tap(test).members().detap().sort().value(),
            [('age', 40), ('age', 50), ('age', 60),
            ('name', 'curly'), ('name', 'larry'), ('name', 'moe')],
        )

    def test_pick(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self.assertEqual(
            self.qclass(stooges).pick('name').value(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.qclass(stooges).pick('name', 'age').value(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        self.assertEqual(
            self.qclass(stooges).pick('place').value(), [],
        )

    def test_pluck(self):
        from stuf import stuf
        stooges = [
            stuf(name='moe', age=40),
            stuf(name='larry', age=50),
            stuf(name='curly', age=60)
        ]
        self.assertEqual(
            self.qclass(stooges).pluck('name').value(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.qclass(stooges).pluck('name', 'age').value(),
            [('moe', 40), ('larry', 50), ('curly', 60)],
        )
        stooges = [['moe', 40], ['larry', 50], ['curly', 60]]
        self.assertEqual(
            self.qclass(stooges).pluck(0).value(),
            ['moe', 'larry', 'curly'],
        )
        self.assertEqual(
            self.qclass(stooges).pluck(1).value(),
            [40, 50, 60],
        )
        self.assertEqual(
            self.qclass(stooges).pluck('place').value(), [],
        )

    ##########################################################################
    ## repetition ############################################################
    ##########################################################################

    def test_ncycles(self):
        self.assertEqual(
            self.qclass([40, 50, 60]).ncycles(3).value(),
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
    ## truth #################################################################
    ##########################################################################

    def test_all(self):
        self.assertFalse(
            self.qclass([True, 1, None, 'yes']).tap(bool).all().value()
        )

    def test_any(self):
        self.assertTrue(
            self.qclass([None, 0, 'yes', False]).tap(bool).any().value()
        )

    def test_include(self):
        self.assertTrue(
            self.qclass([1, 2, 3]).contains(3).value()
        )

    def test_quantify(self):
        self.assertEqual(
            self.qclass([True, 1, None, 'yes']).tap(bool).quantify().value(),
            3,
        )
        self.assertEqual(
            self.qclass([None, 0, 'yes', False]).tap(bool).quantify().value(),
            1
        )

    ##########################################################################
    ## strip #################################################################
    ##########################################################################

    def test_compact(self):
        self.assertEqual(
            self.qclass([0, 1, False, 2, '', 3]).compact().value(),
            [1, 2, 3],
        )

    def test_without(self):
        self.assertEqual(
            self.qclass([1, 2, 1, 0, 3, 1, 4]).without(0, 1).value(),
            [2, 3, 4],
        )

    ##########################################################################
    ## unique slice ##########################################################
    ##########################################################################

    def test_difference(self):
        self.assertEqual(
            self.qclass([[1, 2, 3, 4, 5], [5, 2, 10]]).difference().value(),
            [1, 3, 4],
        )

    def test_intersection(self):
        self.assertEqual(
            self.qclass(
                [[1, 2, 3], [101, 2, 1, 10], [2, 1]]
            ).intersection().value(), [1, 2],
        )

    def test_union(self):
        self.assertEqual(
            self.qclass([[1, 2, 3], [101, 2, 1, 10], [2, 1]]).union().value(),
            [1, 2, 3, 101, 10],
        )

    def test_unique(self):
        self.assertEqual(
            self.qclass([1, 2, 1, 3, 1, 4]).unique().value(),
            [1, 2, 3, 4],
        )
        self.assertEqual(
            self.qclass([1, 2, 1, 3, 1, 4]).tap(round).unique().value(),
            [1, 2, 3, 4],
        )


if __name__ == '__main__':
    import cProfile
    cProfile.run('unittest.main()')
