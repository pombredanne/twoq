# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.active.man.mixins.mapping import *  # @UnusedWildImport
from twoq.tests.active.man.mixins.queuing import MQMixin


class TestManMap(unittest.TestCase, MQMixin, MMapQMixin):

    def setUp(self):
        from twoq.active.mapping import amapq
        self.qclass = amapq


class TestManMappingQ(unittest.TestCase, MQMixin, MMappingQMixin):

    def setUp(self):
        from twoq.active.mapping import amappingq
        self.qclass = amappingq


class TestManRepeatQ(
    unittest.TestCase, MQMixin, MRepeatQMixin
):

    def setUp(self):
        from twoq.active.mapping import arepeatq
        self.qclass = arepeatq


class TestManDelayQ(unittest.TestCase, MQMixin, MDelayQMixin):

    def setUp(self):
        from twoq.active.mapping import adelayq
        self.qclass = adelayq


if __name__ == '__main__':
    unittest.main()
