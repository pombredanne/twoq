# -*- coding: utf-8 -*-
'''ordering test mixins'''

from inspect import ismodule

from twoq.support import port


class MRandomQMixin(object):

    def test_choice(self):
        manq = self.qclass(1, 2, 3, 4, 5, 6).choice()
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        manq.end()
        self.assertTrue(manq.balanced)

    def test_sample(self):
        manq = self.qclass(1, 2, 3, 4, 5, 6).sample(3)
        self.assertFalse(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        manq.end()
        self.assertTrue(manq.balanced)

    def test_shuffle(self):
        manq = self.qclass(1, 2, 3, 4, 5, 6).shuffle()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        manq.end()
        self.assertTrue(manq.balanced)


class MCombineQMixin(object):

#    def test_combinations(self):
#        self._false_true_false(
#            self.qclass('ABCD').combinations(2),
#            self.assertListEqual,
#            [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'),
#            ('C', 'D')],
#        )
#
#    def test_permutations(self):
#        self._false_true_false(
#            self.qclass('ABCD').permutations(2),
#            self.assertListEqual,
#            [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'A'), ('B', 'C'),
#            ('B', 'D'), ('C', 'A'), ('C', 'B'), ('C', 'D'), ('D', 'A'),
#            ('D', 'B'), ('D', 'C')]
#        )

    def test_product(self):
        self._false_true_false(
            self.qclass('ABCD', 'xy').product(),
            self.assertListEqual,
            [('A', 'x'), ('A', 'y'), ('B', 'x'), ('B', 'y'), ('C', 'x'),
            ('C', 'y'), ('D', 'x'), ('D', 'y')]
        )


class MOrderQMixin(MRandomQMixin, MCombineQMixin):

    def test_group(self,):
        from math import floor
        self._false_true_false(
            self.qclass(1.3, 2.1, 2.4).tap(lambda x: floor(x)).group(),
            self.assertListEqual,
            [[1.0, [1.3]], [2.0, [2.1, 2.4]]]
        )
        self._true_true_false(
            self.qclass(1.3, 2.1, 2.4).group(),
            self.assertListEqual,
            [[1.3, [1.3]], [2.1, [2.1]], [2.4, [2.4]]],
        )

    def test_grouper(self):
        self._false_true_false(
            self.qclass(
                'moe', 'larry', 'curly', 30, 40, 50, True,
            ).grouper(2, 'x'),
            self.assertEqual,
            [('moe', 'larry'), ('curly', 30), (40, 50), (True, 'x')],
        )

    def test_reversed(self):
        self._true_true_false(
            self.qclass(5, 4, 3, 2, 1).reverse(),
            self.assertEqual,
            [1, 2, 3, 4, 5],
        )

    def test_sort(self):
        from math import sin
        self._true_true_false(
            self.qclass(1, 2, 3, 4, 5, 6).tap(lambda x: sin(x)).sort(),
           self.assertListEqual,
            [5, 4, 6, 3, 1, 2],
        )
        self._true_true_false(
            self.qclass(4, 6, 65, 3, 63, 2,  4).sort(),
          self.assertListEqual,
            [2, 3, 4, 4, 6, 63, 65],
        )


__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
