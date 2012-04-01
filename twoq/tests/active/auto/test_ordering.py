# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.auto.ordering import *  # @UnusedWildImport
from twoq.tests.auto.queuing import AQMixin


class TestAutoOrderQ(unittest.TestCase, AQMixin, AOrderQMixin):

    def setUp(self):
        from twoq.active.ordering import aorderq
        self.qclass = aorderq


class TestAutoRandomQ(unittest.TestCase, AQMixin, ARandomQMixin):

    def setUp(self):
        from twoq.active.ordering import arandomq
        self.qclass = arandomq


class TestAutoPermutationQ(unittest.TestCase, AQMixin, ACombineQMixin):

    def setUp(self):
        from twoq.active.ordering import acombineq
        self.qclass = acombineq


if __name__ == '__main__':
    unittest.main()
