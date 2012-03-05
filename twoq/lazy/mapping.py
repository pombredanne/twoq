# -*- coding: utf-8 -*-
'''twoq lazy mapping queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.mapping import (
    DelayMixin, CopyMixin, RepeatMixin, MappingMixin)

from twoq.lazy.mixins import AutoResultMixin, ManResultMixin

###############################################################################
## lazy delayed map queues ##################################################
###############################################################################


class adelayq(AutoResultMixin, DelayMixin):

    '''auto-balanced delayed map queue'''

delayq = adelayq


class mdelayq(ManResultMixin, DelayMixin):

    '''manually balanced delayed map queue'''

###############################################################################
## lazy copy queues #########################################################
###############################################################################


class acopyq(AutoResultMixin, CopyMixin):

    '''auto-balanced copy queue'''

copyq = acopyq


class mcopyq(ManResultMixin, CopyMixin):

    '''manually balanced copy queue'''

###############################################################################
## lazy repeat queues #######################################################
###############################################################################


class arepeatq(AutoResultMixin, RepeatMixin):

    '''auto-balanced repeat queue'''

repeatq = arepeatq


class mrepeatq(ManResultMixin, RepeatMixin):

    '''manually balanced repeat queue'''

###############################################################################
## lazy mapping queues ######################################################
###############################################################################


class amapq(AutoResultMixin, MappingMixin):

    '''auto-balanced map queue'''

mapq = amapq


class mmapq(ManResultMixin, MappingMixin):

    '''manually balanced map queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
