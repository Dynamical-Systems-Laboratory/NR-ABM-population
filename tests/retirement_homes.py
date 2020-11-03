import sys
py_path = '../tools/'
sys.path.insert(0, py_path)

py_path = '../src/'
sys.path.insert(0, py_path)

import utils as ut
from colors import *

import abm_public as public

# ------------------------------------------------------------------
#
# Tests for RetirementHomes class functionality
#
# ------------------------------------------------------------------

#
# Input files
#

# File with retirement homes GIS data
rh_file = 'test_data/public_places.txt'
# File with building types
rh_type_file = 'test_data/public_types.txt'

retirement_homes = public.RetirementHomes(rh_file, rh_type_file)

