# -*- coding: utf-8 -*-
'''iterator chaining, underscored by a two-headed queue'''

from twoq.support import port
from twoq.active.queuing import twoq, manq, autoq

__all__ = ('twoq', 'manq', 'autoq', 'port')

__version__ = (0, 4, 7)
