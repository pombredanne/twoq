# -*- coding: utf-8 -*-
'''twoq active ordering queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.ordering import OrderMixin, RandomMixin, OrderingMixin

from twoq.active.mixins import AutoQMixin, ManQMixin

###############################################################################
## active order queues ########################################################
###############################################################################


class orderq(AutoQMixin, OrderMixin):

    '''auto synchronizing order queue'''


class manorderq(ManQMixin, OrderMixin):

    '''manually synchronized order queue'''

###############################################################################
## active random queues #######################################################
###############################################################################


class randomq(AutoQMixin, RandomMixin):

    '''auto synchronizing random queue'''


class manrandomq(ManQMixin, RandomMixin):

    '''manually synchronized random queue'''

###############################################################################
## active ordering queues #####################################################
###############################################################################


class orderingq(AutoQMixin, OrderingMixin):

    '''auto synchronizing orderingqueue'''


class manorderingq(ManQMixin, OrderingMixin):

    '''manually synchronized ordering queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
del ismodule
