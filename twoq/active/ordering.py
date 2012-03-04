# -*- coding: utf-8 -*-
'''twoq active ordering queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.ordering import RandomMixin, OrderingMixin

from twoq.active.mixins import AutoResultMixin, ManResultMixin, SyncResultMixin

###############################################################################
## active random queues #######################################################
###############################################################################


class arandomq(AutoResultMixin, RandomMixin):

    '''auto-balanced random queue'''

randomq = arandomq


class mrandomq(ManResultMixin, RandomMixin):

    '''manually balanced random queue'''


class srandomq(SyncResultMixin, RandomMixin):

    '''autosynchronized random queue'''

###############################################################################
## active order queues #####EEE################################################
###############################################################################


class aorderq(AutoResultMixin, OrderingMixin):

    '''auto-balanced order queue'''

orderq = aorderq


class morderq(ManResultMixin, OrderingMixin):

    '''manually balanced order queue'''


class sorderq(SyncResultMixin, OrderingMixin):

    '''autosynchronized order queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
del ismodule
