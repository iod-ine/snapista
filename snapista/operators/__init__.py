""" This package contains the operator definitions.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""

from snapista.operators.operator import Operator

from snapista.operators.subset import Subset
from snapista.operators.reproject import Reproject
from snapista.operators.band_maths import BandMaths
from snapista.operators.band_select import BandSelect
from snapista.operators.add_elevation import AddElevation
