# -*- coding: utf-8 -*-

from twoq.support import unittest
#pylint: disable-msg=w0614,w0401
from twoq.tests.man.mapping import *  # @UnusedWildImport
from twoq.tests.man.queuing import MQMixin
from twoq.tests.man.manning import Manning


class TestManMap(Manning, MQMixin, MMapQMixin):

    def setUp(self):
        from twoq.lazy.mapping import mmapq
        self.qclass = mmapq


class TestManRepeatQ(Manning, MQMixin, MRepeatQMixin):

    def setUp(self):
        from twoq.lazy.mapping import mrepeatq
        self.qclass = mrepeatq


class TestManDelayQ(Manning, MQMixin, MDelayQMixin):

    def setUp(self):
        from twoq.lazy.mapping import mdelayq
        self.qclass = mdelayq


if __name__ == '__main__':
    unittest.main()
