# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.mixins.auto.ordering import *  # @UnusedWildImport
from twoq.tests.mixins.auto.queuing import AQMixin


class TestSyncOrderQ(unittest.TestCase, AQMixin, AOrderQMixin):

    def setUp(self):
        from twoq.active.ordering import sorderq
        self.qclass = sorderq


class TestSyncRandomQ(unittest.TestCase, AQMixin, ARandomQMixin):

    def setUp(self):
        from twoq.active.ordering import srandomq
        self.qclass = srandomq

if __name__ == '__main__':
    unittest.main()
