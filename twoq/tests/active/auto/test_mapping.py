# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.auto.mapping import *  # @UnusedWildImport
from twoq.tests.auto.queuing import AQMixin


class TestAutoMap(unittest.TestCase, AQMixin, AMapQMixin):

    def setUp(self):
        from twoq.active.mapping import amapq
        self.qclass = amapq


class TestAutoRepeatQ(unittest.TestCase, AQMixin, ARepeatQMixin):

    def setUp(self):
        from twoq.active.mapping import arepeatq
        self.qclass = arepeatq


class TestAutoDelayQ(unittest.TestCase, AQMixin, ADelayQMixin):

    def setUp(self):
        from twoq.active.mapping import adelayq
        self.qclass = adelayq


if __name__ == '__main__':
    unittest.main()
