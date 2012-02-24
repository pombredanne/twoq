# -*- coding: utf-8 -*-
'''manq tests'''

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from twoq.tests.active.man.mixins.queuing import MQMixin
from twoq.tests.active.man.mixins.mapping import MMapQMixin
from twoq.tests.active.man.mixins.ordering import MOrderQMixin
from twoq.tests.active.man.mixins.reducing import MReduceQMixin
from twoq.tests.active.man.mixins.filtering import MFilterQMixin


class TestManQ(
    unittest.TestCase, MQMixin, MFilterQMixin, MMapQMixin, MReduceQMixin,
    MOrderQMixin,
):

    def setUp(self):
        from twoq import manq
        self.qclass = manq


if __name__ == '__main__':
    unittest.main()
