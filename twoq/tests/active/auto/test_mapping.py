# -*- coding: utf-8 -*-

#pylint: disable-msg=w0614,w0401
from twoq.tests.active.auto.mixins.mapping import *  # @UnusedWildImport
from twoq.tests.active.auto.mixins.queuing import AQMixin


class TestAutoMap(AQMixin, AMapQMixin):

    def setUp(self):
        from twoq.active.mapping import amapq
        self.qclass = amapq


class TestAutoMappingQ(AQMixin, AMappingQMixin):

    def setUp(self):
        from twoq.active.mapping import amappingq
        self.qclass = amappingq


class TestAutoRepeatQ(AQMixin, ARepeatQMixin):

    def setUp(self):
        from twoq.active.mapping import arepeatq
        self.qclass = arepeatq


class TestAutoDelayQ(AQMixin, ADelayQMixin):

    def setUp(self):
        from twoq.active.mapping import adelayq
        self.qclass = adelayq


class TestSyncMap(AQMixin, AMapQMixin):

    def setUp(self):
        from twoq.active.mapping import smapq
        self.qclass = smapq


class TestSyncMappingQ(AQMixin, AMappingQMixin):

    def setUp(self):
        from twoq.active.mapping import smappingq
        self.qclass = smappingq


class TestSyncRepeatQ(AQMixin, ARepeatQMixin):

    def setUp(self):
        from twoq.active.mapping import srepeatq
        self.qclass = srepeatq


class TestSyncDelayQ(AQMixin, ADelayQMixin):

    def setUp(self):
        from twoq.active.mapping import sdelayq
        self.qclass = sdelayq

if __name__ == '__main__':
    import cProfile
    cProfile.run('unittest.main()')
