# -*- coding: utf-8 -*-
'''auto mapping test mixins'''

from inspect import ismodule

from twoq.support import port


class AMappingQMixin(object):

    def test_wrap(self):
        from stuf import stuf
        self.assertDictEqual(
            self.qclass(
                ('a', 1), ('b', 2), ('c', 3)
            ).reup().wrap(stuf).map().value(),
            stuf(a=1, b=2, c=3),
        )

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
        
    def test_starmap(self):
        self.assertEquals(
            self.qclass(
                (1, 2), (2, 3), (3, 4)
            ).tap(lambda x, y: x * y).starmap().value(), [2, 6, 12],
        )

    def test_items(self):
        self.assertEquals(
            self.qclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).tap(lambda x, y: x * y).items().value(), [2, 6, 12, 2, 6, 12],
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
        
 
class ACopyQMixin(object):

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


class ARepeatQMixin(object):

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


class ADelayQMixin(object):

    def test_delay_each(self):
        def test(*args, **kw):
            return sum(args) * kw['a']
        self.assertEquals(
            self.qclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            )
            .tap(test)
            .delay_each(0.1)
            .value(),
            [6, 10, 14],
        )

    def test_delay_map(self):
        self.assertEquals(
            self.qclass(1, 2, 3).tap(lambda x: x * 3).delay_map(0.1).value(),
            [3, 6, 9],
        )

    def test_delay_invoke(self):
        self.assertEquals(
            self.qclass([5, 1, 7], [3, 2, 1])
            .args(1)
            .delay_invoke('index', 0.1)
            .value(),
            [1, 2],
        )
        self.assertEquals(
            self.qclass([5, 1, 7], [3, 2, 1])
            .delay_invoke('sort', 0.1).value(),
            [[1, 5, 7], [1, 2, 3]],
        )


class AMapQMixin(ACopyQMixin, ADelayQMixin, AMappingQMixin, ARepeatQMixin):
    
    '''combination mixin'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
