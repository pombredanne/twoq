# -*- coding: utf-8 -*-
'''twoq active reducing queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.reducing import MathMixin, TruthMixin, ReduceMixin

from twoq.active.mixins import AutoResultMixin, ManResultMixin, SyncResultMixin

###############################################################################
## active math queues #########################################################
###############################################################################


class amathq(AutoResultMixin, MathMixin):

    '''auto-balancing math queue'''

mathq = amathq


class mmathq(ManResultMixin, MathMixin):

    '''manually balanced math queue'''


class smathq(SyncResultMixin, MathMixin):

    '''autosynchronized math queue'''

###############################################################################
## active truth queues ####E###################################################
###############################################################################


class atruthq(AutoResultMixin, TruthMixin):

    '''auto-balancing truth queue'''

truthq = atruthq


class mtruthq(ManResultMixin, TruthMixin):

    '''manually balanced truth queue'''


class struthq(SyncResultMixin, TruthMixin):

    '''autosynchronized truth queue'''

###############################################################################
## reduce queues ##############################################################
###############################################################################


class areduceq(AutoResultMixin, ReduceMixin):

    '''auto-balancing reduce queue'''

reduceq = areduceq


class mreduceq(ManResultMixin, ReduceMixin):

    '''manually balanced reduce queue'''


class sreduceq(SyncResultMixin, ReduceMixin):

    '''autosynchronized reduce queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
del ismodule
