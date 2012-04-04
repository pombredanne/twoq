# -*- coding: utf-8 -*-
'''twoq active queues'''

from twoq.mapping import MappingMixin as MapMixin
from twoq.ordering import OrderingMixin as OrderMixin
from twoq.reducing import ReducingMixin as ReduceMixin
from twoq.filtering import FilteringMixin as FilterMixin

from twoq.active.mixins import AutoResultMixin, ManResultMixin

__all__ = ('autoq', 'manq')


class autoq(AutoResultMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''auto-balancing manipulation queue'''


class manq(ManResultMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''manually balanced manipulation queue'''


twoq = autoq
