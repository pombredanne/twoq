# -*- coding: utf-8 -*-
'''twoq active reducing queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.reducing import MathMixin, TruthMixin, ReduceMixin

from twoq.active.mixins import AutoQMixin, ManQMixin, SyncQMixin

###############################################################################
## active math queues #########################################################
###############################################################################


class amathq(AutoQMixin, MathMixin):

    '''auto-balancing math queue'''

mathq = amathq


class mmathq(ManQMixin, MathMixin):

    '''manually balanced math queue'''


class smathq(SyncQMixin, MathMixin):

    '''autosynchronized math queue'''

###############################################################################
## active truth queues ####E###################################################
###############################################################################


class atruthq(AutoQMixin, TruthMixin):

    '''auto-balancing truth queue'''

truthq = atruthq


class mtruthq(ManQMixin, TruthMixin):

    '''manually balanced truth queue'''


class struthq(SyncQMixin, TruthMixin):

    '''autosynchronized truth queue'''

###############################################################################
## reduce queues ##############################################################
###############################################################################


class areduceq(AutoQMixin, ReduceMixin):

    '''auto-balancing reduce queue'''

reduceq = areduceq


class mreduceq(ManQMixin, ReduceMixin):

    '''manually balanced reduce queue'''


class sreduceq(SyncQMixin, ReduceMixin):

    '''autosynchronized reduce queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
del ismodule
