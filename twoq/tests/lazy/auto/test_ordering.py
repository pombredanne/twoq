# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.mixins.auto.ordering import *  # @UnusedWildImport
from twoq.tests.mixins.auto.queuing import AQMixin


class TestAutoOrderQ(unittest.TestCase, AQMixin, AOrderQMixin):

    def setUp(self):
        from twoq.lazy.ordering import aorderq
        self.qclass = aorderq


class TestAutoOrderingQ(unittest.TestCase, AQMixin, AOrderingQMixin):

    def setUp(self):
        from twoq.lazy.ordering import aorderingq
        self.qclass = aorderingq


class TestAutoRandomQ(unittest.TestCase, AQMixin, ARandomQMixin):

    def setUp(self):
        from twoq.lazy.ordering import arandomq
        self.qclass = arandomq

if __name__ == '__main__':
    unittest.main()
