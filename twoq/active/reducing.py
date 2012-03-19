# -*- coding: utf-8 -*-
'''twoq active reducing queues'''

from twoq.mixins.reducing import MathMixin, TruthMixin, ReducingMixin

from twoq.active.mixins import AutoResultMixin, ManResultMixin

###############################################################################
## active math queues #########################################################
###############################################################################


class amathq(AutoResultMixin, MathMixin):

    '''auto-balancing math queue'''

mathq = amathq


class mmathq(ManResultMixin, MathMixin):

    '''manually balanced math queue'''

###############################################################################
## active truth queues ####E###################################################
###############################################################################


class atruthq(AutoResultMixin, TruthMixin):

    '''auto-balancing truth queue'''

truthq = atruthq


class mtruthq(ManResultMixin, TruthMixin):

    '''manually balanced truth queue'''

###############################################################################
## reduce queues ##############################################################
###############################################################################


class areduceq(AutoResultMixin, ReducingMixin):

    '''auto-balancing reduce queue'''

reduceq = areduceq


class mreduceq(ManResultMixin, ReducingMixin):

    '''manually balanced reduce queue'''
