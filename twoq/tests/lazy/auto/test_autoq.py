# -*- coding: utf-8 -*-
'''autoq tests'''

from twoq.support import unittest
from twoq.tests.auto.queuing import AQMixin
from twoq.tests.auto.mapping import AMapQMixin
from twoq.tests.auto.ordering import AOrderQMixin
from twoq.tests.auto.reducing import AReduceQMixin
from twoq.tests.auto.filtering import AFilterQMixin


class TestAutoQ(
    unittest.TestCase, AQMixin, AFilterQMixin, AMapQMixin, AReduceQMixin,
    AOrderQMixin,
):

    def setUp(self):
        from twoq.lazy.queuing import autoq
        self.qclass = autoq


if __name__ == '__main__':
    unittest.main()
