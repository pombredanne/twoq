# -*- coding: utf-8 -*-
'''twoq active queues'''

from twoq.mixins.mapping import MapMixin
from twoq.mixins.reducing import ReduceMixin
from twoq.mixins.ordering import OrderMixin
from twoq.mixins.filtering import FilterMixin

from twoq.active.mixins import AutoQMixin, ManQMixin, SyncQMixin

__all__ = ['twoq', 'manq', 'autoq', 'syncq']


class autoq(
    AutoQMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin
):

    '''auto-balancing manipulation queue'''


class manq(
    ManQMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin
):

    '''manually balanced manipulation queue'''


class syncq(
    SyncQMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin
):

    '''autosyncing manipulation queue'''

twoq = autoq
