# -*- coding: utf-8 -*-
'''twoq lazy queues'''

from twoq.queuing import SLOTS
from twoq.mapping import MappingMixin as MapMixin
from twoq.ordering import OrderingMixin as OrderMixin
from twoq.reducing import ReducingMixin as ReduceMixin
from twoq.filtering import FilteringMixin as FilterMixin

from twoq.lazy.mixins import AutoResultMixin, ManResultMixin


class autoq(AutoResultMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''auto-balancing manipulation queue'''

    __slots__ = SLOTS


class manq(ManResultMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''manually balanced manipulation queue'''

    __slots__ = SLOTS


lazyq = autoq
