# -*- coding: utf-8 -*-
'''auto ordering test mixins'''

from inspect import ismodule

from twoq.support import port


class ARandomQMixin(object):

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


class AOrderQMixin(ARandomQMixin):

    '''combination mixin'''

    def test_group(self,):
        from math import floor
        self.assertEqual(
        self.qclass(1.3, 2.1, 2.4).tap(lambda x: floor(x)).group().value(),
            [[1.0, [1.3]], [2.0, [2.1, 2.4]]]
        )
        self.assertEqual(
            self.qclass(1.3, 2.1, 2.4).group().value(),
            [[1.3, [1.3]], [2.1, [2.1]], [2.4, [2.4]]],
        )

    def test_grouper(self):
        self.assertEqual(
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
        self.assertEqual(
            self.qclass(4, 6, 65, 3, 63, 2, 4).sort().value(),
            [2, 3, 4, 4, 6, 63, 65],
        )


__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
