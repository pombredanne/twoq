# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.mixins.auto.filtering import *  # @UnusedWildImport
from twoq.tests.mixins.auto.queuing import AQMixin


class TestAutoFilterQ(unittest.TestCase, AQMixin, AFilterQMixin):

    def setUp(self):
        self.maxDiff = None
        from twoq.active.filtering import afilterq
        self.qclass = afilterq


class TestAutoFilteringQ(unittest.TestCase, AQMixin, AFilteringQMixin):

    def setUp(self):
        from twoq.active.filtering import afilteringq
        self.qclass = afilteringq


class TestAutoSliceQ(unittest.TestCase, AQMixin, ASliceQMixin):

    def setUp(self):
        from twoq.active.filtering import asliceq
        self.qclass = asliceq


class TestAutoCollectQ(unittest.TestCase, AQMixin, ACollectQMixin):

    def setUp(self):
        self.maxDiff = None
        from twoq.active.filtering import acollectq
        self.qclass = acollectq


class TestAutoSetQ(unittest.TestCase, AQMixin, ASetQMixin):

    '''test automatically synchronized filtering'''

    def setUp(self):
        from twoq.active.filtering import asetq
        self.qclass = asetq


class TestSyncFilterQ(unittest.TestCase, AQMixin, AFilterQMixin):

    def setUp(self):
        self.maxDiff = None
        from twoq.active.filtering import sfilterq
        self.qclass = sfilterq


class TestSyncFilteringQ(unittest.TestCase, AQMixin, AFilteringQMixin):

    def setUp(self):
        from twoq.active.filtering import sfilteringq
        self.qclass = sfilteringq


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
