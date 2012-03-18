# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.mixins.man.mapping import *  # @UnusedWildImport
from twoq.tests.mixins.man.manning import Manning
from twoq.tests.mixins.man.queuing import MQMixin


class TestManMap(Manning, MQMixin, MMapQMixin):

    def setUp(self):
        from twoq.active.mapping import mmapq
        self.qclass = mmapq


class TestManRepeatQ(Manning, MQMixin, MRepeatQMixin):

    def setUp(self):
        from twoq.active.mapping import mrepeatq
        self.qclass = mrepeatq


class TestManDelayQ(Manning, MQMixin, MDelayQMixin):

    def setUp(self):
        from twoq.active.mapping import mdelayq
        self.qclass = mdelayq


if __name__ == '__main__':
    unittest.main()
