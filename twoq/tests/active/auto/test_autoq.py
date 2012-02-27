# -*- coding: utf-8 -*-
'''autoq tests'''

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from twoq.tests.mixins.auto.queuing import AQMixin
from twoq.tests.mixins.auto.mapping import AMapQMixin
from twoq.tests.mixins.auto.ordering import AOrderQMixin
from twoq.tests.mixins.auto.reducing import AReduceQMixin
from twoq.tests.mixins.auto.filtering import AFilterQMixin


class TestAutoQ(
    unittest.TestCase, AQMixin, AFilterQMixin, AMapQMixin, AReduceQMixin,
    AOrderQMixin,
):

    def setUp(self):
        from twoq import autoq
        self.qclass = autoq


if __name__ == '__main__':
    unittest.main()
