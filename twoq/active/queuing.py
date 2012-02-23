# -*- coding: utf-8 -*-
'''twoq active queues'''

from twoq.mixins.filtering import FilteringMixin
from twoq.active.mixins import AutoQMixin, ManQMixin
from twoq.mixins.mapping import MappingMixin
from twoq.mixins.reducing import ReducingMixin
from twoq.mixins.ordering import OrderingMixin

__all__ = ['twoq', 'manq', 'autoq']


class autoq(
    AutoQMixin, FilteringMixin, MappingMixin, ReducingMixin, OrderingMixin
):

    '''autosyncing manipulation queue'''


class manq(
    ManQMixin, FilteringMixin, MappingMixin, ReducingMixin, OrderingMixin
):

    '''maunual balancing manipulation queue'''

twoq = autoq
