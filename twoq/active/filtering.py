# -*- coding: utf-8 -*-
'''twoq active filtering queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.filtering import (
    FilteringMixin, FilterMixin, CollectMixin, SetMixin, SliceMixin)

from twoq.active.mixins import AutoQMixin, ManQMixin, SyncQMixin

###############################################################################
## active filter queues #######################################################
###############################################################################


class afilteringq(AutoQMixin, FilteringMixin):

    '''auto-balanced filter queue'''


class mfilteringq(ManQMixin, FilteringMixin):

    '''manually balanced filter queue'''


class sfilteringq(SyncQMixin, FilteringMixin):

    '''autosynchronized filter queue'''

###############################################################################
## active collecting queues ###################################################
###############################################################################


class acollectq(AutoQMixin, CollectMixin):

    '''auto-balanced collecting queue'''

collectq = acollectq


class mcollectq(ManQMixin, CollectMixin):

    '''manually balanced collecting queue'''


class scollectq(SyncQMixin, CollectMixin):

    '''autosynchronized collecting queue'''

###############################################################################
## active set queues ##########################################################
###############################################################################


class asetq(AutoQMixin, SetMixin):

    '''auto-balanced set queue'''

setq = asetq


class msetq(ManQMixin, SetMixin):

    '''manually balanced set queue'''


class ssetq(SyncQMixin, SetMixin):

    '''autosynchronized set queue'''

###############################################################################
## active slice queues ########################################################
###############################################################################


class asliceq(AutoQMixin, SliceMixin):

    '''auto-balanced slice queue'''

sliceq = asliceq


class msliceq(ManQMixin, SliceMixin):

    '''manually balanced slice queue'''


class ssliceq(SyncQMixin, SliceMixin):

    '''autosynchronized slice queue'''

###############################################################################
## active filter queues #######################################################
###############################################################################


class afilterq(AutoQMixin, FilterMixin):

    '''auto-balanced filter queue'''

filterq = afilterq


class mfilterq(ManQMixin, FilterMixin):

    '''manually balanced filtering queue'''


class sfilterq(SyncQMixin, FilterMixin):

    '''autosynchronized filter queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
