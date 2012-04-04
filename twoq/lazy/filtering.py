# -*- coding: utf-8 -*-
'''twoq lazy filtering queues'''

from twoq.queuing import SLOTS
from twoq.filtering import (
    FilteringMixin, CollectMixin, SetMixin, SliceMixin)

from twoq.lazy.mixins import AutoResultMixin, ManResultMixin


class collectq(AutoResultMixin, CollectMixin):

    '''auto-balanced collecting queue'''

    __slots__ = SLOTS


class mcollectq(ManResultMixin, CollectMixin):

    '''manually balanced collecting queue'''

    __slots__ = SLOTS


class setq(AutoResultMixin, SetMixin):

    '''auto-balanced set queue'''

    __slots__ = SLOTS


class msetq(ManResultMixin, SetMixin):

    '''manually balanced set queue'''

    __slots__ = SLOTS


class sliceq(AutoResultMixin, SliceMixin):

    '''auto-balanced slice queue'''

    __slots__ = SLOTS


class msliceq(ManResultMixin, SliceMixin):

    '''manually balanced slice queue'''

    __slots__ = SLOTS


class filterq(AutoResultMixin, FilteringMixin):

    '''auto-balanced filter queue'''

    __slots__ = SLOTS


class mfilterq(ManResultMixin, FilteringMixin):

    '''manually balanced filtering queue'''

    __slots__ = SLOTS
