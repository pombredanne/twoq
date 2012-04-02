# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.man.reducing import *  # @UnusedWildImport
from twoq.tests.man.manning import Manning
from twoq.tests.man.queuing import MQMixin


class TestManReduceQ(Manning, MQMixin, MReduceQMixin):

    def setUp(self):
        from twoq.active.reducing import mreduceq
        self.qclass = mreduceq


class TestManMathQ(Manning, MQMixin, MMathQMixin):

    def setUp(self):
        from twoq.active.reducing import mmathq
        self.qclass = mmathq


class TestManTruthQ(Manning, MQMixin, MTruthQMixin):

    def setUp(self):
        from twoq.active.reducing import mtruthq
        self.qclass = mtruthq


if __name__ == '__main__':
    unittest.main()
