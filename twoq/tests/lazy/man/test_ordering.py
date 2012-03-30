# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

#pylint: disable-msg=w0614,w0401
from twoq.tests.mixins.man.ordering import *  # @UnusedWildImport
from twoq.tests.mixins.man.queuing import MQMixin
from twoq.tests.mixins.man.manning import Manning


class TestManOrderQ(Manning, MQMixin, MOrderQMixin):

    def setUp(self):
        from twoq.lazy.ordering import morderq
        self.qclass = morderq


class TestManRandomQ(Manning, MQMixin, MRandomQMixin):

    def setUp(self):
        from twoq.lazy.ordering import mrandomq
        self.qclass = mrandomq


class TestManPermutationQ(Manning, MQMixin, APermutationQMixin):

    def setUp(self):
        from twoq.lazy.ordering import mpermutationq
        self.qclass = mpermutationq


if __name__ == '__main__':
    unittest.main()
