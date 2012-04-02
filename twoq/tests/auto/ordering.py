# -*- coding: utf-8 -*-
'''auto ordering call chain test mixins'''

from inspect import ismodule

from twoq.support import port


class ARandomQMixin(object):

    def test_choice(self):
        self.assertEqual(len(list(self.qclass(1, 2, 3, 4, 5, 6).choice())), 1)

    def test_sample(self):
        self.assertEqual(len(self.qclass(1, 2, 3, 4, 5, 6).sample(3).end()), 3)

    def test_shuffle(self):
        self.assertEqual(
            len(self.qclass(1, 2, 3, 4, 5, 6).shuffle()),
            len([5, 4, 6, 3, 1, 2]),
        )


class ACombineQMixin(object):

#    def test_combinations(self):
#        foo = self.qclass('ABCD').combinations(2).value(),
#        self.assertEqual(
#            foo[0],
#            [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'),
#            ('C', 'D')],
#            foo,
#        )
#
#    def test_permutations(self):
#        foo = self.qclass('ABCD').permutations(2).value()
#        self.assertEqual(
#            foo[0],
#            [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'A'), ('B', 'C'),
#            ('B', 'D'), ('C', 'A'), ('C', 'B'), ('C', 'D'), ('D', 'A'),
#            ('D', 'B'), ('D', 'C')],
#            foo,
#        )

    def test_product(self):
        foo = self.qclass('ABCD', 'xy').product().value()
        self.assertEqual(
            foo,
            [('A', 'x'), ('A', 'y'), ('B', 'x'), ('B', 'y'), ('C', 'x'),
            ('C', 'y'), ('D', 'x'), ('D', 'y')],
            foo,
        )


class AOrderQMixin(ARandomQMixin, ACombineQMixin):

    '''combination mixin'''

    def test_group(self,):
        from math import floor
        self.assertEqual(
        self.qclass(1.3, 2.1, 2.4).tap(lambda x: floor(x)).group().end(),
            [[1.0, [1.3]], [2.0, [2.1, 2.4]]]
        )
        self.assertEqual(
            self.qclass(1.3, 2.1, 2.4).group().end(),
            [[1.3, [1.3]], [2.1, [2.1]], [2.4, [2.4]]],
        )

    def test_grouper(self):
        self.assertEqual(
            self.qclass(
                'moe', 'larry', 'curly', 30, 40, 50, True
            ).grouper(2, 'x').end(),
             [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')]
        )

    def test_reversed(self):
        self.assertEqual(
            self.qclass(5, 4, 3, 2, 1).reverse().end(), [1, 2, 3, 4, 5],
        )

    def test_sort(self):
        from math import sin
        self.assertEqual(
            self.qclass(1, 2, 3, 4, 5, 6).tap(
                lambda x: sin(x)
            ).sort().end(),
            [5, 4, 6, 3, 1, 2],
        )
        self.assertEqual(
            self.qclass(4, 6, 65, 3, 63, 2, 4).sort().end(),
            [2, 3, 4, 4, 6, 63, 65],
        )


__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
