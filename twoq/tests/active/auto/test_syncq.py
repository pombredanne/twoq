# -*- coding: utf-8 -*-
'''syncq tests'''

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from twoq.tests.active.auto.mixins.queuing import AQMixin
from twoq.tests.active.auto.mixins.mapping import AMapQMixin
from twoq.tests.active.auto.mixins.ordering import AOrderQMixin
from twoq.tests.active.auto.mixins.reducing import AReduceQMixin
from twoq.tests.active.auto.mixins.filtering import AFilterQMixin


class TestSyncQ(unittest.TestCase,
    AQMixin, AFilterQMixin, AMapQMixin, AReduceQMixin, AOrderQMixin,
):

    def setUp(self):
        from twoq import syncq
        self.qclass = syncq


if __name__ == '__main__':
    unittest.main()
