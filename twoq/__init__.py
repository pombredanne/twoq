# -*- coding: utf-8 -*-
'''twoq iterator utilities'''

from twoq.support import port, iterexcept
from twoq.active.queuing import twoq, manq, autoq, syncq

__all__ = ('twoq', 'manq', 'autoq', 'port', 'syncq', 'iterexcept')

__version__ = (0, 1, 1)
