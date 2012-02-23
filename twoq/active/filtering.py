# -*- coding: utf-8 -*-
'''twoq active filtering queues'''

from inspect import ismodule

from twoq.support import port

from twoq.mixins.filtering import (
    FilterMixin, FilteringMixin, CollectMixin, SetMixin, SliceMixin)

from twoq.active.mixins import AutoQMixin, ManQMixin

###############################################################################
## active filter queues #######################################################
###############################################################################


class filterq(AutoQMixin, FilterMixin):

    '''auto synchronizing filter queue'''


class manfilterq(ManQMixin, FilterMixin):

    '''manually synchronized filter queue'''

###############################################################################
## active collecting queues ###################################################
###############################################################################


class collectq(AutoQMixin, CollectMixin):

    '''auto synchronizing collecting queue'''


class mancollectq(ManQMixin, CollectMixin):

    '''manually synchronized collecting queue'''


###############################################################################
## active set queues ##########################################################
###############################################################################


class setq(AutoQMixin, SetMixin):

    '''auto synchronizing set queue'''


class mansetq(ManQMixin, SetMixin):

    '''manually synchronized set queue'''


###############################################################################
## active slice queues ########################################################
###############################################################################


class sliceq(AutoQMixin, SliceMixin):

    '''auto synchronizing slice queue'''


class mansliceq(ManQMixin, SliceMixin):

    '''manually synchronized slice queue'''

###############################################################################
## active filtering queues ####################################################
###############################################################################


class filteringq(AutoQMixin, FilteringMixin):

    '''auto synchronizing filtering queue'''


class manfilteringq(ManQMixin, FilteringMixin):

    '''manually synchronized filtering queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
