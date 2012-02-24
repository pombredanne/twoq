# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.active.auto.mixins.ordering import *  # @UnusedWildImport
from twoq.tests.active.auto.mixins.queuing import AQMixin


class TestAutoOrderQ(unittest.TestCase, AQMixin, AOrderQMixin):

    def setUp(self):
        from twoq.active.ordering import aorderq
        self.qclass = aorderq


class TestAutoOrderingQ(unittest.TestCase, AQMixin, AOrderingQMixin):

    def setUp(self):
        from twoq.active.ordering import aorderingq
        self.qclass = aorderingq


class TestAutoRandomQ(unittest.TestCase, AQMixin, ARandomQMixin):

    def setUp(self):
        from twoq.active.ordering import arandomq
        self.qclass = arandomq


class TestSyncOrderQ(unittest.TestCase, AQMixin, AOrderQMixin):

    def setUp(self):
        from twoq.active.ordering import sorderq
        self.qclass = sorderq


class TestSyncOrderingQ(unittest.TestCase, AQMixin, AOrderingQMixin):

    def setUp(self):
        from twoq.active.ordering import sorderingq
        self.qclass = sorderingq


class TestSyncRandomQ(unittest.TestCase, AQMixin, ARandomQMixin):

    def setUp(self):
        from twoq.active.ordering import srandomq
        self.qclass = srandomq

if __name__ == '__main__':
    unittest.main()
