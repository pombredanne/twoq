# -*- coding: utf-8 -*-
'''twoq lazy queues'''

from twoq.mixins.mapping import MappingMixin as MapMixin
from twoq.mixins.reducing import ReducingMixin as ReduceMixin
from twoq.mixins.ordering import OrderingMixin as OrderMixin
from twoq.mixins.filtering import FilteringMixin as FilterMixin

from twoq.lazy.mixins import AutoQMixin, ManQMixin

__all__ = ('autoq', 'manq', 'twoq')


class autoq(AutoQMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''auto-balancing manipulation queue'''


class manq(ManQMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''manually balanced manipulation queue'''


lazyq = autoq
