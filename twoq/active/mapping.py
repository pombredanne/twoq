# -*- coding: utf-8 -*-
'''twoq active mapping queues'''

from twoq.queuing import SLOTS
from twoq.mapping import DelayMixin, RepeatMixin, MappingMixin

from twoq.active.mixins import AutoResultMixin, ManResultMixin


class delayq(AutoResultMixin, DelayMixin):

    '''auto-balanced delayed map queue'''

    __slots__ = SLOTS


class mdelayq(ManResultMixin, DelayMixin):

    '''manually balanced delayed map queue'''

    __slots__ = SLOTS


class repeatq(AutoResultMixin, RepeatMixin):

    '''auto-balanced repeat queue'''

    __slots__ = SLOTS


class mrepeatq(ManResultMixin, RepeatMixin):

    '''manually balanced repeat queue'''

    __slots__ = SLOTS


class mapq(AutoResultMixin, MappingMixin):

    '''auto-balanced mapping queue'''

    __slots__ = SLOTS


class mmapq(ManResultMixin, MappingMixin):

    '''manually balanced mapping queue'''

    __slots__ = SLOTS
