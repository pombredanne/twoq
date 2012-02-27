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
        from twoq.lazy.reducing import areduceq
        self.qclass = areduceq


class TestAutoReducingQ(unittest.TestCase, AQMixin, AReducingQMixin):

    def setUp(self):
        from twoq.lazy.reducing import areducingq
        self.qclass = areducingq


class TestAutoMathQ(unittest.TestCase, AQMixin, AMathQMixin):

    def setUp(self):
        from twoq.lazy.reducing import amathq
        self.qclass = amathq


class TestAutoTruthQ(unittest.TestCase, AQMixin, ATruthQMixin):

    def setUp(self):
        from twoq.lazy.reducing import atruthq
        self.qclass = atruthq


if __name__ == '__main__':
    unittest.main()
