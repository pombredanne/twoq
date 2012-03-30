# -*- coding: utf-8 -*-
'''twoq active ordering queues'''

from twoq.mixins.ordering import RandomMixin, OrderingMixin, PermutationMixin

from twoq.active.mixins import AutoResultMixin, ManResultMixin

###############################################################################
## active random queues #######################################################
###############################################################################


class arandomq(AutoResultMixin, RandomMixin):

    '''auto-balanced random queue'''

randomq = arandomq


class mrandomq(ManResultMixin, RandomMixin):

    '''manually balanced random queue'''

###############################################################################
## active order queues #####EEE################################################
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
