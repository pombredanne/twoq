# -*- coding: utf-8 -*-
'''twoq lazy ordering queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.ordering import OrderingMixin, RandomMixin, OrderMixin

from twoq.lazy.mixins import AutoQMixin, ManQMixin

###############################################################################
## lazy ordering queues #####################################################
###############################################################################


class aorderingq(AutoQMixin, OrderingMixin):

    '''auto-balanced ordering queue'''

orderingq = aorderingq


class morderingq(ManQMixin, OrderingMixin):

    '''manually balanced ordering queue'''

###############################################################################
## lazy random queues #######################################################
###############################################################################


class arandomq(AutoQMixin, RandomMixin):

    '''auto-balanced random queue'''

randomq = arandomq


class mrandomq(ManQMixin, RandomMixin):

    '''manually balanced random queue'''

###############################################################################
## lazy order queues #####EEE################################################
###############################################################################


class aorderq(AutoQMixin, OrderMixin):

    '''auto-balanced order queue'''

orderq = aorderq


class morderq(ManQMixin, OrderMixin):

    '''manually balanced order queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
del ismodule
