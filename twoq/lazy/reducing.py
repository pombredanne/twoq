# -*- coding: utf-8 -*-
'''twoq lazy reducing queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.reducing import (
    MathMixin, ReducingMixin, TruthMixin, ReduceMixin)

from twoq.lazy.mixins import AutoQMixin, ManQMixin

###############################################################################
## lazy math queues ###########################################################
###############################################################################


class amathq(AutoQMixin, MathMixin):

    '''auto-balancing math queue'''

mathq = amathq


class mmathq(ManQMixin, MathMixin):

    '''manually balanced math queue'''

###############################################################################
## lazy reducing queues #######################################################
###############################################################################


class areducingq(AutoQMixin, ReducingMixin):

    '''auto-balancing reducing queue'''

reducingq = areducingq


class mreducingq(ManQMixin, ReducingMixin):

    '''manually balanced reducing queue'''

###############################################################################
## lazy truth queues ######E###################################################
###############################################################################


class atruthq(AutoQMixin, TruthMixin):

    '''auto-balancing truth queue'''

truthq = atruthq


class mtruthq(ManQMixin, TruthMixin):

    '''manually balanced truth queue'''


###############################################################################
## reduce queues ##############################################################
###############################################################################


class areduceq(AutoQMixin, ReduceMixin):

    '''auto-balancing reduce queue'''

reduceq = areduceq


class mreduceq(ManQMixin, ReduceMixin):

    '''manually balanced reduce queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
del ismodule
