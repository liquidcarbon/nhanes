# pynhanes/__init__.py

__doc__ = """
PyNHANES: library for working with NHANES data
"""

#-----------------------------------------------------------------------------
# Logging
#-----------------------------------------------------------------------------

import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

from . import data

#-----------------------------------------------------------------------------
# A function to test logging
#-----------------------------------------------------------------------------

_l = logging.getLogger(__name__)
_l.debug(f'{__name__} package (re)loaded')