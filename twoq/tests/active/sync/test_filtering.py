# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.mixins.auto.filtering import *  # @UnusedWildImport
from twoq.tests.mixins.auto.queuing import AQMixin


class TestSyncFilterQ(unittest.TestCase, AQMixin, AFilterQMixin):

    def setUp(self):
        self.maxDiff = None
        from twoq.active.filtering import sfilterq
        self.qclass = sfilterq


class TestSyncSliceQ(unittest.TestCase, AQMixin, ASliceQMixin):

    def setUp(self):
        from twoq.active.filtering import ssliceq
        self.qclass = ssliceq


class TestSyncCollectQ(unittest.TestCase, AQMixin, ACollectQMixin):

    def setUp(self):
        self.maxDiff = None
        from twoq.active.filtering import scollectq
        self.qclass = scollectq


class TestSyncSetQ(unittest.TestCase, AQMixin, ASetQMixin):

    def setUp(self):
        from twoq.active.filtering import ssetq
        self.qclass = ssetq


if __name__ == '__main__':
    unittest.main()
