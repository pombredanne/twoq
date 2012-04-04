# -*- coding: utf-8 -*-
'''twoq active filtering queues'''

from twoq.filtering import (
    FilteringMixin, CollectMixin, SetMixin, SliceMixin)

from twoq.active.mixins import AutoResultMixin, ManResultMixin

###############################################################################
## active collecting queues ###################################################
###############################################################################


class acollectq(AutoResultMixin, CollectMixin):

    '''auto-balanced collecting queue'''

collectq = acollectq


class mcollectq(ManResultMixin, CollectMixin):

    '''manually balanced collecting queue'''

###############################################################################
## active set queues ##########################################################
###############################################################################


class asetq(AutoResultMixin, SetMixin):

    '''auto-balanced set queue'''

setq = asetq


class msetq(ManResultMixin, SetMixin):

    '''manually balanced set queue'''

###############################################################################
## active slice queues ########################################################
###############################################################################


class asliceq(AutoResultMixin, SliceMixin):

    '''auto-balanced slice queue'''

sliceq = asliceq


class msliceq(ManResultMixin, SliceMixin):

    '''manually balanced slice queue'''

###############################################################################
## active filter queues #######################################################
###############################################################################


class afilterq(AutoResultMixin, FilteringMixin):

    '''auto-balanced filter queue'''

filterq = afilterq


class mfilterq(ManResultMixin, FilteringMixin):

    '''manually balanced filtering queue'''
