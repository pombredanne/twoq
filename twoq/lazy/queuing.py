# -*- coding: utf-8 -*-
'''twoq lazy queues'''

from twoq.mixins.mapping import MapMixin
from twoq.mixins.reducing import ReduceMixin
from twoq.mixins.ordering import OrderMixin
from twoq.mixins.filtering import FilterMixin

from twoq.lazy.mixins import AutoQMixin, ManQMixin

__all__ = ('autoq', 'manq', 'twoq')


class autoq(AutoQMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''auto-balancing manipulation queue'''


class manq(ManQMixin, FilterMixin, MapMixin, ReduceMixin, OrderMixin):

    '''manually balanced manipulation queue'''


twoq = autoq
