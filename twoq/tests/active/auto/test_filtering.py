# -*- coding: utf-8 -*-

#pylint: disable-msg=w0614,w0401
from twoq.tests.active.auto.mixins.filtering import *  # @UnusedWildImport
from twoq.tests.active.auto.mixins.queuing import AQMixin


class TestAutoFilterQ(AQMixin, AFilterQMixin):

    def setUp(self):
        from twoq.active.filtering import afilterq
        self.qclass = afilterq


class TestAutoFilteringQ(AQMixin, AFilteringQMixin):

    def setUp(self):
        from twoq.active.filtering import afilteringq
        self.qclass = afilteringq


class TestAutoSliceQ(AQMixin, ASliceQMixin):

    def setUp(self):
        from twoq.active.filtering import asliceq
        self.qclass = asliceq


class TestAutoCollectQ(AQMixin, ACollectQMixin):

    def setUp(self):
        from twoq.active.filtering import acollectq
        self.qclass = acollectq


class TestAutoSetQ(AQMixin, ASetQMixin):

    '''test automatically synchronized filtering'''

    def setUp(self):
        from twoq.active.filtering import asetq
        self.qclass = asetq


class TestSyncFilterQ(AQMixin, AFilterQMixin):

    def setUp(self):
        from twoq.active.filtering import sfilterq
        self.qclass = sfilterq


class TestSyncFilteringQ(AQMixin, AFilteringQMixin):

    def setUp(self):
        from twoq.active.filtering import sfilteringq
        self.qclass = sfilteringq


class TestSyncSliceQ(AQMixin, ASliceQMixin):

    def setUp(self):
        from twoq.active.filtering import ssliceq
        self.qclass = ssliceq


class TestSyncCollectQ(AQMixin, ACollectQMixin):

    def setUp(self):
        from twoq.active.filtering import scollectq
        self.qclass = scollectq


class TestSyncSetQ(AQMixin, ASetQMixin):

    def setUp(self):
        from twoq.active.filtering import ssetq
        self.qclass = ssetq


if __name__ == '__main__':
    import cProfile
    cProfile.run('unittest.main()')
