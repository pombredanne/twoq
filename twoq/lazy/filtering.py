# -*- coding: utf-8 -*-
'''twoq lazy filtering queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.filtering import (
    FilteringMixin, CollectMixin, SetMixin, SliceMixin)

from twoq.lazy.mixins import AutoQMixin, ManQMixin

###############################################################################
## lazy collecting queues ###################################################
###############################################################################


class acollectq(AutoQMixin, CollectMixin):

    '''auto-balanced collecting queue'''

collectq = acollectq


class mcollectq(ManQMixin, CollectMixin):

    '''manually balanced collecting queue'''

###############################################################################
## lazy set queues ##########################################################
###############################################################################


class asetq(AutoQMixin, SetMixin):

    '''auto-balanced set queue'''

setq = asetq


class msetq(ManQMixin, SetMixin):

    '''manually balanced set queue'''

###############################################################################
## lazy slice queues ########################################################
###############################################################################


class asliceq(AutoQMixin, SliceMixin):

    '''auto-balanced slice queue'''

sliceq = asliceq


class msliceq(ManQMixin, SliceMixin):

    '''manually balanced slice queue'''

###############################################################################
## lazy filter queues #######################################################
###############################################################################


class afilterq(AutoQMixin, FilteringMixin):

    '''auto-balanced filter queue'''

filterq = afilterq


class mfilterq(ManQMixin, FilteringMixin):

    '''manually balanced filtering queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
