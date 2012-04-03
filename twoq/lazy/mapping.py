# -*- coding: utf-8 -*-
'''twoq lazy mapping queues'''

from twoq.imps import LookupsMixin
from twoq.mapping import DelayMixin, RepeatMixin, MappingMixin

from twoq.lazy.mixins import AutoResultMixin, ManResultMixin

###############################################################################
## lazy delayed map queues ##################################################
###############################################################################


class adelayq(LookupsMixin, AutoResultMixin, DelayMixin):

    '''auto-balanced delayed map queue'''

delayq = adelayq


class mdelayq(LookupsMixin, ManResultMixin, DelayMixin):

    '''manually balanced delayed map queue'''

###############################################################################
## lazy repeat queues #######################################################
###############################################################################


class arepeatq(LookupsMixin, AutoResultMixin, RepeatMixin):

    '''auto-balanced repeat queue'''

repeatq = arepeatq


class mrepeatq(LookupsMixin, ManResultMixin, RepeatMixin):

    '''manually balanced repeat queue'''

###############################################################################
## lazy mapping queues ######################################################
###############################################################################


class amapq(LookupsMixin, AutoResultMixin, MappingMixin):

    '''auto-balanced map queue'''

mapq = amapq


class mmapq(LookupsMixin, ManResultMixin, MappingMixin):

    '''manually balanced map queue'''
