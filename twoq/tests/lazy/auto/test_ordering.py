# -*- coding: utf-8 -*-

from twoq.support import unittest
#pylint: disable-msg=w0614,w0401
from twoq.tests.auto.ordering import *  # @UnusedWildImport
from twoq.tests.auto.queuing import AQMixin


class TestAutoOrderQ(unittest.TestCase, AQMixin, AOrderQMixin):

    def setUp(self):
        from twoq.lazy.ordering import orderq
        self.qclass = orderq


class TestAutoRandomQ(unittest.TestCase, AQMixin, ARandomQMixin):

    def setUp(self):
        from twoq.lazy.ordering import randomq
        self.qclass = randomq


class TestAutoPermutationQ(unittest.TestCase, AQMixin, ACombineQMixin):

    def setUp(self):
        from twoq.lazy.ordering import combineq
        self.qclass = combineq

if __name__ == '__main__':
    unittest.main()
