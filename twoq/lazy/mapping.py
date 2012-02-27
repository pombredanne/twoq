# -*- coding: utf-8 -*-
'''twoq lazy mapping queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.mapping import (
    DelayMixin, CopyMixin, MappingMixin, RepeatMixin, MapMixin)

from twoq.lazy.mixins import AutoQMixin, ManQMixin

###############################################################################
## lazy delayed map queues ##################################################
###############################################################################


class adelayq(AutoQMixin, DelayMixin):

    '''auto-balanced delayed map queue'''

delayq = adelayq


class mdelayq(ManQMixin, DelayMixin):

    '''manually balanced delayed map queue'''

###############################################################################
## lazy copy queues #########################################################
###############################################################################


class acopyq(AutoQMixin, CopyMixin):

    '''auto-balanced copy queue'''

copyq = acopyq


class mcopyq(ManQMixin, CopyMixin):

    '''manually balanced copy queue'''

###############################################################################
## lazy map queues ##########################################################
###############################################################################


class amappingq(AutoQMixin, MappingMixin):

    '''auto-balanced mapping queue'''

mappingq = amappingq


class mmappingq(ManQMixin, MappingMixin):

    '''manually balanced mapping queue'''

###############################################################################
## lazy repeat queues #######################################################
###############################################################################


class arepeatq(AutoQMixin, RepeatMixin):

    '''auto-balanced repeat queue'''

repeatq = arepeatq


class mrepeatq(ManQMixin, RepeatMixin):

    '''manually balanced repeat queue'''

###############################################################################
## lazy mapping queues ######################################################
###############################################################################


class amapq(AutoQMixin, MapMixin):

    '''auto-balanced map queue'''

mapq = amapq


class mmapq(ManQMixin, MapMixin):

    '''manually balanced map queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
