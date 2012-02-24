# -*- coding: utf-8 -*-

#pylint: disable-msg=w0614,w0401
from twoq.tests.active.man.mixins.filtering import *  # @UnusedWildImport
from twoq.tests.active.man.mixins.queuing import MQMixin


class TestManFilterQ(MQMixin, MFilterQMixin):

    def setUp(self):
        from twoq.active.filtering import mfilterq
        self.qclass = mfilterq


class TestManFilteringQ(MQMixin, MFilteringQMixin):

    def setUp(self):
        from twoq.active.filtering import mfilteringq
        self.qclass = mfilteringq


class TestManSliceQ(MQMixin, MSliceQMixin):

    def setUp(self):
        from twoq.active.filtering import msliceq
        self.qclass = msliceq


class TestManCollectQ(MQMixin, MCollectQMixin):

    def setUp(self):
        from twoq.active.filtering import mcollectq
        self.qclass = mcollectq


class TestManSetQ(MQMixin, MSetQMixin):

    def setUp(self):
        from twoq.active.filtering import msetq
        self.qclass = msetq


if __name__ == '__main__':
    import cProfile
    cProfile.run('unittest.main()')
