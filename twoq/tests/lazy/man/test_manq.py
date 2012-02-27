# -*- coding: utf-8 -*-
'''manq tests'''

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from twoq.tests.mixins.man.queuing import MQMixin
from twoq.tests.mixins.man.mapping import MMapQMixin
from twoq.tests.mixins.man.ordering import MOrderQMixin
from twoq.tests.mixins.man.reducing import MReduceQMixin
from twoq.tests.mixins.man.filtering import MFilterQMixin


class TestManQ(
    unittest.TestCase, MQMixin, MFilterQMixin, MMapQMixin, MReduceQMixin,
    MOrderQMixin,
):

    def setUp(self):
        from twoq.lazy.queuing import manq
        self.qclass = manq


if __name__ == '__main__':
    unittest.main()
