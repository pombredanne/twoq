# -*- coding: utf-8 -*-
'''twoq lazy ordering queues'''

from twoq.imps import LookupsMixin
from twoq.ordering import RandomMixin, OrderingMixin, CombineMixin

from twoq.lazy.mixins import AutoResultMixin, ManResultMixin

###############################################################################
## lazy random queues #######################################################
###############################################################################


class arandomq(LookupsMixin, AutoResultMixin, RandomMixin):

    '''auto-balanced random queue'''

randomq = arandomq


class mrandomq(LookupsMixin, ManResultMixin, RandomMixin):

    '''manually balanced random queue'''

###############################################################################
## lazy order queues #####EEE################################################
###############################################################################


class aorderq(LookupsMixin, AutoResultMixin, OrderingMixin):

    '''auto-balanced order queue'''

orderq = aorderq


class morderq(LookupsMixin, ManResultMixin, OrderingMixin):

    '''manually balanced order queue'''


###############################################################################
## active combination queues #####EEE##########################################
###############################################################################


class acombineq(LookupsMixin, AutoResultMixin, CombineMixin):

    '''auto-balanced combination queue'''

combineq = acombineq


class mcombineq(LookupsMixin, ManResultMixin, CombineMixin):

    '''manually balanced combination queue'''
