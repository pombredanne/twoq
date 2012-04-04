# -*- coding: utf-8 -*-

from twoq.support import unittest
from twoq.tests.auto.filtering import *  # @UnusedWildImport
from twoq.tests.auto.queuing import AQMixin


class TestAutoFilterQ(unittest.TestCase, AQMixin, AFilterQMixin):

    def setUp(self):
        self.maxDiff = None
        from twoq.active.filtering import filterq
        self.qclass = filterq


class TestAutoSliceQ(unittest.TestCase, AQMixin, ASliceQMixin):

    def setUp(self):
        from twoq.active.filtering import sliceq
        self.qclass = sliceq


class TestAutoCollectQ(unittest.TestCase, AQMixin, ACollectQMixin):

    def setUp(self):
        self.maxDiff = None
        from twoq.active.filtering import collectq
        self.qclass = collectq


class TestAutoSetQ(unittest.TestCase, AQMixin, ASetQMixin):

    def setUp(self):
        from twoq.active.filtering import setq
        self.qclass = setq


if __name__ == '__main__':
    unittest.main()
