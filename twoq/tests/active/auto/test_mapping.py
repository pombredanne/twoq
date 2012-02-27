# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.mixins.auto.mapping import *  # @UnusedWildImport
from twoq.tests.mixins.auto.queuing import AQMixin


class TestAutoMap(AQMixin, AMapQMixin):

    def setUp(self):
        from twoq.active.mapping import amapq
        self.qclass = amapq


class TestAutoMappingQ(unittest.TestCase, AQMixin, AMappingQMixin):

    def setUp(self):
        from twoq.active.mapping import amappingq
        self.qclass = amappingq


class TestAutoRepeatQ(unittest.TestCase, AQMixin, ARepeatQMixin):

    def setUp(self):
        from twoq.active.mapping import arepeatq
        self.qclass = arepeatq


class TestAutoDelayQ(unittest.TestCase, AQMixin, ADelayQMixin):

    def setUp(self):
        from twoq.active.mapping import adelayq
        self.qclass = adelayq


class TestSyncMap(AQMixin, AMapQMixin):

    def setUp(self):
        from twoq.active.mapping import smapq
        self.qclass = smapq


class TestSyncMappingQ(unittest.TestCase, AQMixin, AMappingQMixin):

    def setUp(self):
        from twoq.active.mapping import smappingq
        self.qclass = smappingq


class TestSyncRepeatQ(unittest.TestCase, AQMixin, ARepeatQMixin):

    def setUp(self):
        from twoq.active.mapping import srepeatq
        self.qclass = srepeatq


class TestSyncDelayQ(unittest.TestCase, AQMixin, ADelayQMixin):

    def setUp(self):
        from twoq.active.mapping import sdelayq
        self.qclass = sdelayq

if __name__ == '__main__':
    unittest.main()
