# -*- coding: utf-8 -*-
'''twoq active ordering queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.ordering import OrderingMixin, RandomMixin, OrderMixin

from twoq.active.mixins import AutoQMixin, ManQMixin, SyncQMixin

###############################################################################
## active ordering queues #####################################################
###############################################################################


class aorderingq(AutoQMixin, OrderingMixin):

    '''auto-balanced ordering queue'''

orderingq = aorderingq


class morderingq(ManQMixin, OrderingMixin):

    '''manually balanced ordering queue'''


class sorderingq(SyncQMixin, OrderingMixin):

    '''autosynchronized ordering queue'''

###############################################################################
## active random queues #######################################################
###############################################################################


class arandomq(AutoQMixin, RandomMixin):

    '''auto-balanced random queue'''

randomq = arandomq


class mrandomq(ManQMixin, RandomMixin):

    '''manually balanced random queue'''


class srandomq(SyncQMixin, RandomMixin):

    '''autosynchronized random queue'''

###############################################################################
## active order queues #####EEE################################################
###############################################################################


class aorderq(AutoQMixin, OrderMixin):

    '''auto-balanced order queue'''

orderq = aorderq


class morderq(ManQMixin, OrderMixin):

    '''manually balanced order queue'''


class sorderq(SyncQMixin, OrderMixin):

    '''autosynchronized order queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
del ismodule
