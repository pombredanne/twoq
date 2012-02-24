# -*- coding: utf-8 -*-

#pylint: disable-msg=w0614,w0401
from twoq.tests.active.man.mixins.mapping import *  # @UnusedWildImport
from twoq.tests.active.man.mixins.queuing import MQMixin


class TestManMap(MQMixin, MMapQMixin):

    def setUp(self):
        from twoq.active.mapping import amapq
        self.qclass = amapq


class TestManMappingQ(MQMixin, MMappingQMixin):

    def setUp(self):
        from twoq.active.mapping import amappingq
        self.qclass = amappingq


class TestManRepeatQ(MQMixin, MRepeatQMixin):

    def setUp(self):
        from twoq.active.mapping import arepeatq
        self.qclass = arepeatq


class TestManDelayQ(MQMixin, MDelayQMixin):

    def setUp(self):
        from twoq.active.mapping import adelayq
        self.qclass = adelayq


if __name__ == '__main__':
    import cProfile
    cProfile.run('unittest.main()')
