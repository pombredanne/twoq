# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.mixins.man.reducing import *  # @UnusedWildImport
from twoq.tests.mixins.man.queuing import MQMixin


class TestManReduceQ(unittest.TestCase, MQMixin, MReduceQMixin):

    def setUp(self):
        from twoq.active.reducing import mreduceq
        self.qclass = mreduceq


class TestManReducingQ(unittest.TestCase, MQMixin, MReducingQMixin):

    def setUp(self):
        from twoq.active.reducing import mreducingq
        self.qclass = mreducingq


class TestManMathQ(unittest.TestCase, MQMixin, MMathQMixin):

    def setUp(self):
        from twoq.active.reducing import mmathq
        self.qclass = mmathq


class TestManTruthQ(unittest.TestCase, MQMixin, MTruthQMixin):

    def setUp(self):
        from twoq.active.reducing import mtruthq
        self.qclass = mtruthq


if __name__ == '__main__':
    unittest.main()
