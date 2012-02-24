# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.active.man.mixins.ordering import *  # @UnusedWildImport
from twoq.tests.active.man.mixins.queuing import MQMixin


class TestManOrderQ(unittest.TestCase, MQMixin, MOrderQMixin):

    def setUp(self):
        from twoq.active.ordering import morderq
        self.qclass = morderq


class TestManOrderingQ(unittest.TestCase, MQMixin, MOrderingQMixin):

    def setUp(self):
        from twoq.active.ordering import morderingq
        self.qclass = morderingq


class TestManRandomQ(unittest.TestCase, MQMixin, MRandomQMixin):

    def setUp(self):
        from twoq.active.ordering import mrandomq
        self.qclass = mrandomq

if __name__ == '__main__':
    unittest.main()
