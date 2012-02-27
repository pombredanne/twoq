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
        from twoq.lazy.filtering import afilterq
        self.qclass = afilterq


class TestAutoFilteringQ(unittest.TestCase, AQMixin, AFilteringQMixin):

    def setUp(self):
        from twoq.lazy.filtering import afilteringq
        self.qclass = afilteringq


class TestAutoSliceQ(unittest.TestCase, AQMixin, ASliceQMixin):

    def setUp(self):
        from twoq.lazy.filtering import asliceq
        self.qclass = asliceq


class TestAutoCollectQ(unittest.TestCase, AQMixin, ACollectQMixin):

    def setUp(self):
        self.maxDiff = None
        from twoq.lazy.filtering import acollectq
        self.qclass = acollectq


class TestAutoSetQ(unittest.TestCase, AQMixin, ASetQMixin):

    '''test automatically synchronized filtering'''

    def setUp(self):
        from twoq.lazy.filtering import asetq
        self.qclass = asetq


if __name__ == '__main__':
    unittest.main()
