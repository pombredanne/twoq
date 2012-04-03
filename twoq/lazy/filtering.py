# -*- coding: utf-8 -*-
'''twoq lazy filtering queues'''

from twoq.imps import LookupsMixin
from twoq.filtering import (
    FilteringMixin, CollectMixin, SetMixin, SliceMixin)

from twoq.lazy.mixins import AutoResultMixin, ManResultMixin

###############################################################################
## lazy collecting queues ###################################################
###############################################################################


class acollectq(LookupsMixin, AutoResultMixin, CollectMixin):

    '''auto-balanced collecting queue'''

collectq = acollectq


class mcollectq(LookupsMixin, ManResultMixin, CollectMixin):

    '''manually balanced collecting queue'''

###############################################################################
## lazy set queues ##########################################################
###############################################################################


class asetq(LookupsMixin, AutoResultMixin, SetMixin):

    '''auto-balanced set queue'''

setq = asetq


class msetq(LookupsMixin, ManResultMixin, SetMixin):

    '''manually balanced set queue'''

###############################################################################
## lazy slice queues ########################################################
###############################################################################


class asliceq(LookupsMixin, AutoResultMixin, SliceMixin):

    '''auto-balanced slice queue'''

sliceq = asliceq


class msliceq(LookupsMixin, ManResultMixin, SliceMixin):

    '''manually balanced slice queue'''

###############################################################################
## lazy filter queues #######################################################
###############################################################################


class afilterq(LookupsMixin, AutoResultMixin, FilteringMixin):

    '''auto-balanced filter queue'''

filterq = afilterq


class mfilterq(LookupsMixin, ManResultMixin, FilteringMixin):

    '''manually balanced filtering queue'''
