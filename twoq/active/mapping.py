# -*- coding: utf-8 -*-
'''twoq active mapping queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.mapping import (
    DelayMixin, CopyMixin, MapMixin, RepeatMixin, MappingMixin)

from twoq.active.mixins import AutoQMixin, ManQMixin

###############################################################################
## active delayed map queues ##################################################
###############################################################################


class delayq(AutoQMixin, DelayMixin):

    '''auto synchronizing delayed map queue'''


class mandelayq(ManQMixin, DelayMixin):

    '''manually synchronized delayed map queue'''

###############################################################################
## active copy queues #########################################################
###############################################################################


class copyq(AutoQMixin, CopyMixin):

    '''auto synchronizing delayed copy queue'''


class mancopyq(ManQMixin, CopyMixin):

    '''manually synchronized delayed copy queue'''

###############################################################################
## active map queues ##########################################################
###############################################################################


class mapq(AutoQMixin, MapMixin):

    '''auto synchronizing map queue'''


class manmapq(ManQMixin, MapMixin):

    '''manually synchronized map queue'''

###############################################################################
## active repeat queues #######################################################
###############################################################################


class repeatq(AutoQMixin, RepeatMixin):

    '''auto synchronizing repeat queue'''


class manrepeatq(ManQMixin, RepeatMixin):

    '''manually synchronized repeat queue'''

###############################################################################
## active mapping queues ######################################################
###############################################################################


class mappingq(AutoQMixin, MappingMixin):

    '''auto synchronizing mapping queue'''


class manmappingq(ManQMixin, MappingMixin):

    '''manually synchronized mapping queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
