# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.mixins.man.filtering import *  # @UnusedWildImport
from twoq.tests.mixins.man.queuing import MQMixin


class TestManFilterQ(unittest.TestCase, MFilterQMixin):

    def setUp(self):
        self.maxDiff = None
        from twoq.lazy.filtering import mfilterq
        self.qclass = mfilterq


class TestManFilteringQ(unittest.TestCase, MQMixin, MFilteringQMixin):

    def setUp(self):
        from twoq.lazy.filtering import mfilteringq
        self.qclass = mfilteringq


class TestManSliceQ(unittest.TestCase, MQMixin, MSliceQMixin):

    def setUp(self):
        from twoq.lazy.filtering import msliceq
        self.qclass = msliceq


class TestManCollectQ(unittest.TestCase, MQMixin, MCollectQMixin):

    def setUp(self):
        from twoq.lazy.filtering import mcollectq
        self.qclass = mcollectq


class TestManSetQ(unittest.TestCase, MQMixin, MSetQMixin):

    def setUp(self):
        from twoq.lazy.filtering import msetq
        self.qclass = msetq


if __name__ == '__main__':
    unittest.main()
