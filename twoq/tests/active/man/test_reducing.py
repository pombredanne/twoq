# -*- coding: utf-8 -*-

#pylint: disable-msg=w0614,w0401
from twoq.tests.active.man.mixins.reducing import *  # @UnusedWildImport
from twoq.tests.active.man.mixins.queuing import MQMixin


class TestManReduceQ(MQMixin, MReduceQMixin):

    def setUp(self):
        from twoq.active.reducing import mreduceq
        self.qclass = mreduceq


class TestManReducingQ(MQMixin, MReducingQMixin):

    def setUp(self):
        from twoq.active.reducing import mreducingq
        self.qclass = mreducingq


class TestManMathQ(MQMixin, MMathQMixin):

    def setUp(self):
        from twoq.active.reducing import mmathq
        self.qclass = mmathq


class TestManTruthQ(MQMixin, MTruthQMixin):

    def setUp(self):
        from twoq.active.reducing import struthq
        self.qclass = struthq
