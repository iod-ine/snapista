""" This package contains the operator definitions.

This version of snapista is my personal take on what is originally presented here:
    https://github.com/snap-contrib/snapista

"""

from snapista.operators._operator import Operator

from snapista.operators._subset import Subset
from snapista.operators._resample import Resample
from snapista.operators._collocate import Collocate
from snapista.operators._reproject import Reproject
from snapista.operators._band_maths import BandMaths
from snapista.operators._band_select import BandSelect
from snapista.operators._land_sea_mask import LandSeaMask
from snapista.operators._add_elevation import AddElevation
from snapista.operators._import_vector import ImportVector
from snapista.operators._add_land_cover import AddLandCover
