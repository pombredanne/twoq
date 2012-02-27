# -*- coding: utf-8 -*-
'''ordering test mixins'''

from inspect import ismodule

from twoq.support import port


class MOrderingQMixin(object):

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
        manq = self.qclass(4, 6, 65, 3, 63, 2,  4).sort()
        self.assertTrue(manq.balanced)
        manq.sync()
        self.assertTrue(manq.balanced)
        self.assertEqual(
            manq.value(),
            [2, 3, 4, 4, 6, 63, 65],
        )
        self.assertFalse(manq.balanced)
        self.assertEqual(manq.outcount(), 0)


class MRandomQMixin(object):

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


class MOrderQMixin(MOrderingQMixin, MRandomQMixin):

    '''combination mixin'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj), name in ['ismodule', 'port']
]))
del ismodule
