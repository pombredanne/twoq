# -*- coding: utf-8 -*-
'''manq tests'''

from twoq.support import unittest
from twoq.tests.man.manning import Manning
from twoq.tests.man.queuing import MQMixin
from twoq.tests.man.mapping import MMapQMixin
from twoq.tests.man.ordering import MOrderQMixin
from twoq.tests.man.reducing import MReduceQMixin
from twoq.tests.man.filtering import MFilterQMixin


class TestManQ(
    Manning, MQMixin, MFilterQMixin, MMapQMixin, MReduceQMixin, MOrderQMixin,
):

    def setUp(self):
        from twoq.lazy.queuing import manq
        self.qclass = manq


if __name__ == '__main__':
    unittest.main()
