# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.mixins.auto.reducing import *  # @UnusedWildImport
from twoq.tests.mixins.auto.queuing import AQMixin


class TestSyncReduceQ(unittest.TestCase, AQMixin, AReduceQMixin):

    def setUp(self):
        from twoq.active.reducing import sreduceq
        self.qclass = sreduceq


class TestSyncMathQ(unittest.TestCase, AQMixin, AMathQMixin):

    def setUp(self):
        from twoq.active.reducing import smathq
        self.qclass = smathq


class TestSyncTruthQ(unittest.TestCase, AQMixin, ATruthQMixin):

    def setUp(self):
        from twoq.active.reducing import struthq
        self.qclass = struthq


if __name__ == '__main__':
    unittest.main()
