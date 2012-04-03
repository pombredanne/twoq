# -*- coding: utf-8 -*-
'''twoq active filtering queues'''

from twoq.imps import LookupsMixin
from twoq.filtering import (
    FilteringMixin, CollectMixin, SetMixin, SliceMixin)

from twoq.active.mixins import AutoResultMixin, ManResultMixin

###############################################################################
## active collecting queues ###################################################
###############################################################################


class acollectq(LookupsMixin, AutoResultMixin, CollectMixin):

    '''auto-balanced collecting queue'''

collectq = acollectq


class mcollectq(LookupsMixin, ManResultMixin, CollectMixin):

    '''manually balanced collecting queue'''

###############################################################################
## active set queues ##########################################################
###############################################################################


class asetq(LookupsMixin, AutoResultMixin, SetMixin):

    '''auto-balanced set queue'''

setq = asetq


class msetq(LookupsMixin, ManResultMixin, SetMixin):

    '''manually balanced set queue'''

###############################################################################
## active slice queues ########################################################
###############################################################################


class asliceq(LookupsMixin, AutoResultMixin, SliceMixin):

    '''auto-balanced slice queue'''

sliceq = asliceq


class msliceq(LookupsMixin, ManResultMixin, SliceMixin):

    '''manually balanced slice queue'''

###############################################################################
## active filter queues #######################################################
###############################################################################


class afilterq(LookupsMixin, AutoResultMixin, FilteringMixin):

    '''auto-balanced filter queue'''

filterq = afilterq


class mfilterq(LookupsMixin, ManResultMixin, FilteringMixin):

    '''manually balanced filtering queue'''
