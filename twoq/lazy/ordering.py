# -*- coding: utf-8 -*-
'''twoq lazy ordering queues'''

from twoq.queuing import SLOTS
from twoq.ordering import RandomMixin, OrderingMixin, CombineMixin

from twoq.lazy.mixins import AutoResultMixin, ManResultMixin


class randomq(AutoResultMixin, RandomMixin):

    '''auto-balanced random queue'''

    __slots__ = SLOTS


class mrandomq(ManResultMixin, RandomMixin):

    '''manually balanced random queue'''

    __slots__ = SLOTS


class orderq(AutoResultMixin, OrderingMixin):

    '''auto-balanced order queue'''

    __slots__ = SLOTS


class morderq(ManResultMixin, OrderingMixin):

    '''manually balanced order queue'''

    __slots__ = SLOTS


class combineq(AutoResultMixin, CombineMixin):

    '''auto-balanced combination queue'''

    __slots__ = SLOTS


class mcombineq(ManResultMixin, CombineMixin):

    '''manually balanced combination queue'''

    __slots__ = SLOTS
