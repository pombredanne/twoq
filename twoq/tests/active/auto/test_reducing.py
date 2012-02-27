# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.mixins.auto.reducing import *  # @UnusedWildImport
from twoq.tests.mixins.auto.queuing import AQMixin


class TestAutoReduceQ(unittest.TestCase, AQMixin, AReduceQMixin):

    def setUp(self):
        from twoq.active.reducing import areduceq
        self.qclass = areduceq


class TestAutoReducingQ(unittest.TestCase, AQMixin, AReducingQMixin):

    def setUp(self):
        from twoq.active.reducing import areducingq
        self.qclass = areducingq


class TestAutoMathQ(unittest.TestCase, AQMixin, AMathQMixin):

    def setUp(self):
        from twoq.active.reducing import amathq
        self.qclass = amathq


class TestAutoTruthQ(unittest.TestCase, AQMixin, ATruthQMixin):

    def setUp(self):
        from twoq.active.reducing import atruthq
        self.qclass = atruthq


class TestSyncReduceQ(unittest.TestCase, AQMixin, AReduceQMixin):

    def setUp(self):
        from twoq.active.reducing import sreduceq
        self.qclass = sreduceq


class TestSyncReducingQ(unittest.TestCase, AQMixin, AReducingQMixin):

    def setUp(self):
        from twoq.active.reducing import sreducingq
        self.qclass = sreducingq


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
