# -*- coding: utf-8 -*-
'''twoq active reducing queues'''

from twoq.imps import LookupsMixin
from twoq.reducing import MathMixin, TruthMixin, ReducingMixin

from twoq.active.mixins import AutoResultMixin, ManResultMixin

###############################################################################
## active math queues #########################################################
###############################################################################


class amathq(LookupsMixin, AutoResultMixin, MathMixin):

    '''auto-balancing math queue'''

mathq = amathq


class mmathq(LookupsMixin, ManResultMixin, MathMixin):

    '''manually balanced math queue'''

###############################################################################
## active truth queues ####E###################################################
###############################################################################


class atruthq(LookupsMixin, AutoResultMixin, TruthMixin):

    '''auto-balancing truth queue'''

truthq = atruthq


class mtruthq(LookupsMixin, ManResultMixin, TruthMixin):

    '''manually balanced truth queue'''

###############################################################################
## reduce queues ##############################################################
###############################################################################


class areduceq(LookupsMixin, AutoResultMixin, ReducingMixin):

    '''auto-balancing reduce queue'''

reduceq = areduceq


class mreduceq(LookupsMixin, ManResultMixin, ReducingMixin):

    '''manually balanced reduce queue'''
