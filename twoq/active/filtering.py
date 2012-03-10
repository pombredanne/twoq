# -*- coding: utf-8 -*-
'''twoq active filtering queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.filtering import (
    FilteringMixin, CollectMixin, SetMixin, SliceMixin)

from twoq.active.mixins import AutoResultMixin, ManResultMixin, SyncResultMixin

###############################################################################
## active collecting queues ###################################################
###############################################################################


class acollectq(AutoResultMixin, CollectMixin):

    '''auto-balanced collecting queue'''

collectq = acollectq


class mcollectq(ManResultMixin, CollectMixin):

    '''manually balanced collecting queue'''


class scollectq(SyncResultMixin, CollectMixin):

    '''autosynchronized collecting queue'''

###############################################################################
## active set queues ##########################################################
###############################################################################


class asetq(AutoResultMixin, SetMixin):

    '''auto-balanced set queue'''

setq = asetq


class msetq(ManResultMixin, SetMixin):

    '''manually balanced set queue'''


class ssetq(SyncResultMixin, SetMixin):

    '''autosynchronized set queue'''

###############################################################################
## active slice queues ########################################################
###############################################################################


class asliceq(AutoResultMixin, SliceMixin):

    '''auto-balanced slice queue'''

sliceq = asliceq


class msliceq(ManResultMixin, SliceMixin):

    '''manually balanced slice queue'''


class ssliceq(SyncResultMixin, SliceMixin):

    '''autosynchronized slice queue'''

###############################################################################
## active filter queues #######################################################
###############################################################################


class afilterq(AutoResultMixin, FilteringMixin):

    '''auto-balanced filter queue'''

filterq = afilterq


class mfilterq(ManResultMixin, FilteringMixin):

    '''manually balanced filtering queue'''


class sfilterq(SyncResultMixin, FilteringMixin):

    '''autosynchronized filter queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
