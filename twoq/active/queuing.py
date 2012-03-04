# -*- coding: utf-8 -*-
'''twoq active queues'''

from twoq.mixins.mapping import MappingMixin as MapMixin
from twoq.mixins.ordering import OrderingMixin as OrderMixin
from twoq.mixins.reducing import ReducingMixin as ReduceMixin
from twoq.mixins.filtering import FilteringMixin as FilterMixin

from twoq.active.mixins import AutoResultMixin, ManResultMixin, SyncResultMixin

__all__ = ('autoq', 'manq', 'syncq', 'twoq')


class autoq(AutoResultMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''auto-balancing manipulation queue'''


class manq(ManResultMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''manually balanced manipulation queue'''


class syncq(SyncResultMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''autosyncing manipulation queue'''


twoq = autoq
