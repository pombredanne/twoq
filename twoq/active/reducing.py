# -*- coding: utf-8 -*-
'''twoq active reducing queues'''

from inspect import ismodule

from twoq.support import port

from twoq.mixins.reducing import (
    MathMixin, ReduceMixin, TruthMixin, ReducingMixin)

from twoq.active.mixins import AutoQMixin, ManQMixin

###############################################################################
## active math queues #########################################################
###############################################################################


class mathq(AutoQMixin, MathMixin):

    '''auto synchronizing math queue'''


class manmathq(ManQMixin, MathMixin):

    '''manually synchronized math queue'''

###############################################################################
## active reduce queues #######################################################
###############################################################################


class reduceq(AutoQMixin, ReduceMixin):

    '''auto synchronizing reduce queue'''


class manreduceq(ManQMixin, ReduceMixin):

    '''manually synchronized reduce queue'''

###############################################################################
## active truth queues ####E###################################################
###############################################################################


class truthq(AutoQMixin, TruthMixin):

    '''auto synchronizing truth queue'''


class mantruthq(ManQMixin, TruthMixin):

    '''manually synchronized truth queue'''

###############################################################################
## reducing queues ########E###################################################
###############################################################################


class reducingq(AutoQMixin, ReducingMixin):

    '''auto synchronizing reducing queue'''


class manreducingq(ManQMixin, ReducingMixin):

    '''manually synchronized reducing queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
del ismodule
