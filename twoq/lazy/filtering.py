# -*- coding: utf-8 -*-
'''twoq lazy filtering queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.filtering import (
    FilteringMixin, CollectMixin, SetMixin, SliceMixin)

from twoq.lazy.mixins import AutoResultMixin, ManResultMixin

###############################################################################
## lazy collecting queues ###################################################
###############################################################################


class acollectq(AutoResultMixin, CollectMixin):

    '''auto-balanced collecting queue'''

collectq = acollectq


class mcollectq(ManResultMixin, CollectMixin):

    '''manually balanced collecting queue'''

###############################################################################
## lazy set queues ##########################################################
###############################################################################


class asetq(AutoResultMixin, SetMixin):

    '''auto-balanced set queue'''

setq = asetq


class msetq(ManResultMixin, SetMixin):

    '''manually balanced set queue'''

###############################################################################
## lazy slice queues ########################################################
###############################################################################


class asliceq(AutoResultMixin, SliceMixin):

    '''auto-balanced slice queue'''

sliceq = asliceq


class msliceq(ManResultMixin, SliceMixin):

    '''manually balanced slice queue'''

###############################################################################
## lazy filter queues #######################################################
###############################################################################


class afilterq(AutoResultMixin, FilteringMixin):

    '''auto-balanced filter queue'''

filterq = afilterq


class mfilterq(ManResultMixin, FilteringMixin):

    '''manually balanced filtering queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
