# -*- coding: utf-8 -*-
'''mapping call chain test mixins'''

from inspect import ismodule

from twoq.support import port


class MRepeatQMixin(object):

    def test_range(self):
        self._false_true_false(
            self.qclass().range(3), self.assertEqual, [0, 1, 2]
        )
        self._false_true_false(
            self.qclass().range(1, 3), self.assertEqual, [1, 2],
        )
        self._false_true_false(
            self.qclass().range(1, 3, 2), self.assertEqual, 1,
        )

    def test_repeat(self):
        self._true_true_false(
            self.qclass(40, 50, 60).repeat(3),
            self.assertEqual,
            [(40, 50, 60), (40, 50, 60), (40, 50, 60)],
        )

    def test_times(self):
        def test(*args):
            return list(args)
        self._true_true_false(
            self.qclass(40, 50, 60).tap(test).times(3),
            self.assertEqual,
            [[40, 50, 60], [40, 50, 60], [40, 50, 60]],
        )

    def test_copy(self):
        testlist = [[1, [2, 3]], [4, [5, 6]]]
        manq = self.qclass(testlist).copy()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        newlist = manq.end()
        self.assertFalse(newlist is testlist)
        self.assertListEqual(newlist, testlist)
        self.assertFalse(newlist[0] is testlist[0])
        self.assertListEqual(newlist[0], testlist[0])
        self.assertFalse(newlist[1] is testlist[1])
        self.assertListEqual(newlist[1], testlist[1])
#        self.assertFalse(manq.balanced)


class MDelayQMixin(object):

    def test_delay_each(self):
        def test(*args, **kw):
            return sum(args) * kw['a']
        self._true_true_false(
            self.qclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).tap(test).delay_each(0.01),
            self.assertEqual,
            [6, 10, 14],
        )

    def test_delay_map(self):
        self._true_true_false(
            self.qclass(1, 2, 3).tap(lambda x: x * 3).delay_map(0.01),
            self.assertEqual,
            [3, 6, 9],
        )

    def test_delay_invoke(self):
        self._true_true_false(
            self.qclass(
                [5, 1, 7], [3, 2, 1]
            ).args(1).delay_invoke('index', 0.01),
            self.assertEqual,
            [1, 2],
        )
        self._true_true_false(
            self.qclass([5, 1, 7], [3, 2, 1]).delay_invoke('sort', 0.01),
            self.assertEqual,
            [[1, 5, 7], [1, 2, 3]],
        )


class MMapQMixin(MDelayQMixin, MRepeatQMixin):

    def test_wrap(self):
        from stuf import stuf
        thing = self.qclass(
            ('a', 1), ('b', 2), ('c', 3)
        ).reup().wrap(stuf).map().shift().end()
        self.assertDictEqual(thing, stuf(a=1, b=2, c=3), thing)

    def test_each(self):
        def test(*args, **kw):
            return sum(args) * kw['a']
        self._true_true_false(
            self.qclass(
                ((1, 2), {'a': 2}), ((2, 3), {'a': 2}), ((3, 4), {'a': 2})
            ).tap(test).each(),
            self.assertEqual,
            [6, 10, 14],
        )

    def test_map(self):
        self._true_true_false(
            self.qclass(1, 2, 3).tap(lambda x: x * 3).map(),
            self.assertEqual,
            [3, 6, 9],
        )

    def test_starmap(self):
        self._true_true_false(
            self.qclass(
                (1, 2), (2, 3), (3, 4)
            ).tap(lambda x, y: x * y).starmap(),
            self.assertEqual,
            [2, 6, 12],
        )

    def test_items(self):
        self._false_true_false(
            self.qclass(
                dict([(1, 2), (2, 3), (3, 4)]), dict([(1, 2), (2, 3), (3, 4)])
            ).tap(lambda x, y: x * y).items(),
            self.assertEqual,
            [2, 6, 12, 2, 6, 12],
        )

    def test_invoke(self):
        self._true_true_false(
            self.qclass([5, 1, 7], [3, 2, 1]).args(1).invoke('index'),
            self.assertEqual,
            [1, 2],
        )
        self._true_true_false(
            self.qclass([5, 1, 7], [3, 2, 1]).invoke('sort'),
            self.assertEqual,
            [[1, 5, 7], [1, 2, 3]]
        )

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
