# -*- coding: utf-8 -*-
'''twoq active mapping queues'''

from inspect import ismodule

from twoq.support import port
from twoq.mixins.mapping import (
    DelayMixin, CopyMixin, RepeatMixin, MappingMixin)

from twoq.active.mixins import AutoResultMixin, ManResultMixin, SyncResultMixin

###############################################################################
## active delayed map queues ##################################################
###############################################################################


class adelayq(AutoResultMixin, DelayMixin):

    '''auto-balanced delayed map queue'''

delayq = adelayq


class mdelayq(ManResultMixin, DelayMixin):

    '''manually balanced delayed map queue'''


class sdelayq(SyncResultMixin, DelayMixin):

    '''autosynchronized  delayed map queue'''

###############################################################################
## active copy queues #########################################################
###############################################################################


class acopyq(AutoResultMixin, CopyMixin):

    '''auto-balanced copy queue'''

copyq = acopyq


class mcopyq(ManResultMixin, CopyMixin):

    '''manually balanced copy queue'''


class scopyq(SyncResultMixin, CopyMixin):

    '''autosynchronized copy queue'''

###############################################################################
## active repeat queues #######################################################
###############################################################################


class arepeatq(AutoResultMixin, RepeatMixin):

    '''auto-balanced repeat queue'''

repeatq = arepeatq


class mrepeatq(ManResultMixin, RepeatMixin):

    '''manually balanced repeat queue'''


class srepeatq(SyncResultMixin, RepeatMixin):

    '''autosynchronized repeat queue'''

###############################################################################
## active mapping queues ######################################################
###############################################################################


class amapq(AutoResultMixin, MappingMixin):

    '''auto-balanced map queue'''

mapq = amapq


class mmapq(ManResultMixin, MappingMixin):

    '''manually balanced map queue'''


class smapq(SyncResultMixin, MappingMixin):

    '''autosynchronized map queue'''

__all__ = sorted(name for name, obj in port.items(locals()) if not any([
    name.startswith('_'), ismodule(obj),
]))
