# -*- coding: utf-8 -*-
'''twoq active mapping queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.mapping import (
    DelayMixin, CopyMixin, MappingMixin, RepeatMixin, MapMixin)

from twoq.active.mixins import AutoQMixin, ManQMixin, SyncQMixin

###############################################################################
## active delayed map queues ##################################################
###############################################################################


class adelayq(AutoQMixin, DelayMixin):

    '''auto-balanced delayed map queue'''

delayq = adelayq


class mdelayq(ManQMixin, DelayMixin):

    '''manually balanced delayed map queue'''


class sdelayq(SyncQMixin, DelayMixin):

    '''autosynchronized  delayed map queue'''

###############################################################################
## active copy queues #########################################################
###############################################################################


class acopyq(AutoQMixin, CopyMixin):

    '''auto-balanced copy queue'''

copyq = acopyq


class mcopyq(ManQMixin, CopyMixin):

    '''manually balanced copy queue'''


class scopyq(SyncQMixin, CopyMixin):

    '''autosynchronized copy queue'''

###############################################################################
## active map queues ##########################################################
###############################################################################


class amappingq(AutoQMixin, MappingMixin):

    '''auto-balanced mapping queue'''

mappingq = amappingq


class mmappingq(ManQMixin, MappingMixin):

    '''manually balanced mapping queue'''


class smappingq(SyncQMixin, MappingMixin):

    '''autosynchronized mapping queue'''

###############################################################################
## active repeat queues #######################################################
###############################################################################


class arepeatq(AutoQMixin, RepeatMixin):

    '''auto-balanced repeat queue'''

repeatq = arepeatq


class mrepeatq(ManQMixin, RepeatMixin):

    '''manually balanced repeat queue'''


class srepeatq(SyncQMixin, RepeatMixin):

    '''autosynchronized repeat queue'''

###############################################################################
## active mapping queues ######################################################
###############################################################################


class amapq(AutoQMixin, MapMixin):

    '''auto-balanced map queue'''

mapq = amapq


class mmapq(ManQMixin, MapMixin):

    '''manually balanced map queue'''


class smapq(SyncQMixin, MapMixin):

    '''autosynchronized map queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
