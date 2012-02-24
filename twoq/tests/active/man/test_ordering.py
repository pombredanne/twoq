# -*- coding: utf-8 -*-

#pylint: disable-msg=w0614,w0401
from twoq.tests.active.man.mixins.ordering import *  # @UnusedWildImport
from twoq.tests.active.man.mixins.queuing import MQMixin


class TestManOrderQ(MQMixin, MOrderQMixin):

    def setUp(self):
        from twoq.active.ordering import morderq
        self.qclass = morderq


class TestManOrderingQ(MQMixin, MOrderingQMixin):

    def setUp(self):
        from twoq.active.ordering import morderingq
        self.qclass = morderingq


class TestManRandomQ(MQMixin, MRandomQMixin):

    def setUp(self):
        from twoq.active.ordering import mrandomq
        self.qclass = mrandomq
