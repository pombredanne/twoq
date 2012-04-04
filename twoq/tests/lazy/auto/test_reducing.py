# -*- coding: utf-8 -*-

from twoq.support import unittest
#pylint: disable-msg=w0614,w0401
from twoq.tests.auto.reducing import *  # @UnusedWildImport
from twoq.tests.auto.queuing import AQMixin


class TestAutoReduceQ(unittest.TestCase, AQMixin, AReduceQMixin):

    def setUp(self):
        from twoq.lazy.reducing import reduceq
        self.qclass = reduceq


class TestAutoMathQ(unittest.TestCase, AQMixin, AMathQMixin):

    def setUp(self):
        from twoq.lazy.reducing import mathq
        self.qclass = mathq


class TestAutoTruthQ(unittest.TestCase, AQMixin, ATruthQMixin):

    def setUp(self):
        from twoq.lazy.reducing import truthq
        self.qclass = truthq


if __name__ == '__main__':
    unittest.main()
