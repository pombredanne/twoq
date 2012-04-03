# -*- coding: utf-8 -*-
'''twoq lazy reducing queues'''

from twoq.imps import LookupsMixin
from twoq.reducing import MathMixin, TruthMixin, ReducingMixin

from twoq.lazy.mixins import AutoResultMixin, ManResultMixin

###############################################################################
## lazy math queues ###########################################################
###############################################################################


class amathq(LookupsMixin, AutoResultMixin, MathMixin):

    '''auto-balancing math queue'''

mathq = amathq


class mmathq(LookupsMixin, ManResultMixin, MathMixin):

    '''manually balanced math queue'''

###############################################################################
## lazy truth queues ######E###################################################
###############################################################################


class atruthq(LookupsMixin, AutoResultMixin, TruthMixin):

    '''auto-balancing truth queue'''

truthq = atruthq


class mtruthq(LookupsMixin, ManResultMixin, TruthMixin):

    '''manually balanced truth queue'''


###############################################################################
## lazy reduce queues #########################################################
###############################################################################


class areduceq(LookupsMixin, AutoResultMixin, ReducingMixin):

    '''auto-balancing reduce queue'''

reduceq = areduceq


class mreduceq(LookupsMixin, ManResultMixin, ReducingMixin):

    '''manually balanced reduce queue'''
