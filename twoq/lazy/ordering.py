# -*- coding: utf-8 -*-
'''twoq lazy ordering queues'''

from twoq.mixins.ordering import RandomMixin, OrderingMixin, PermutationMixin

from twoq.lazy.mixins import AutoResultMixin, ManResultMixin

###############################################################################
## lazy random queues #######################################################
###############################################################################


class arandomq(AutoResultMixin, RandomMixin):

    '''auto-balanced random queue'''

randomq = arandomq


class mrandomq(ManResultMixin, RandomMixin):

    '''manually balanced random queue'''

###############################################################################
## lazy order queues #####EEE################################################
###############################################################################


class aorderq(AutoResultMixin, OrderingMixin):

    '''auto-balanced order queue'''

orderq = aorderq


class morderq(ManResultMixin, OrderingMixin):

    '''manually balanced order queue'''


###############################################################################
## active permutation queues #####EEE##########################################
###############################################################################


class apermutationq(AutoResultMixin, PermutationMixin):

    '''auto-balanced permutation queue'''

permutationq = apermutationq


class mpermutationq(ManResultMixin, PermutationMixin):

    '''manually balanced permutation queue'''
