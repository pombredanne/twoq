# -*- coding: utf-8 -*-

#pylint: disable-msg=w0614,w0401
from twoq.tests.active.auto.mixins.reducing import *  # @UnusedWildImport
from twoq.tests.active.auto.mixins.queuing import AQMixin


class TestAutoReduceQ(AQMixin, AReduceQMixin):

    def setUp(self):
        from twoq.active.reducing import areduceq
        self.qclass = areduceq


class TestAutoReducingQ(AQMixin, AReducingQMixin):

    def setUp(self):
        from twoq.active.reducing import areducingq
        self.qclass = areducingq


class TestAutoMathQ(AQMixin, AMathQMixin):

    def setUp(self):
        from twoq.active.reducing import amathq
        self.qclass = amathq


class TestAutoTruthQ(AQMixin, ATruthQMixin):

    def setUp(self):
        from twoq.active.reducing import struthq
        self.qclass = struthq


class TestSyncReduceQ(AQMixin, AReduceQMixin):

    def setUp(self):
        from twoq.active.reducing import sreduceq
        self.qclass = sreduceq


class TestSyncReducingQ(AQMixin, AReducingQMixin):

    def setUp(self):
        from twoq.active.reducing import sreducingq
        self.qclass = sreducingq


class TestSyncMathQ(AQMixin, AMathQMixin):

    def setUp(self):
        from twoq.active.reducing import smathq
        self.qclass = smathq


class TestSyncTruthQ(AQMixin, ATruthQMixin):

    def setUp(self):
        from twoq.active.reducing import struthq
        self.qclass = struthq


if __name__ == '__main__':
    import cProfile
    cProfile.run('unittest.main()')
