import sys
py_path = '../tools/'
sys.path.insert(0, py_path)

py_path = '../src/'
sys.path.insert(0, py_path)

import utils as ut
from colors import *

import abm_residential as res
import abm_public as public

# ------------------------------------------------------------------
#
# Tests for Households class functionality
#
# ------------------------------------------------------------------

#
# Input files
#

# File with residential GIS data
res_file = 'test_data/test_residential.txt'
# File with residential building types
res_type_file = 'test_data/residential_types.txt'
# File with retirement homes GIS data
rh_file = 'test_data/public_places.txt'
# File with building types
rh_type_file = 'test_data/public_types.txt'
# File with output
house_out = 'test_data/house_output.txt'

#
# Other input
#

# Total number of units (households + vacancies)
n_tot = 100 

households = res.Households(n_tot, res_file, res_type_file)

# Merge with retirement homes
retirement_homes = public.RetirementHomes(rh_file, rh_type_file)
households.merge_with_retirement_homes(retirement_homes.retirement_homes)

with open(house_out, 'w') as fout:
	fout.write(repr(households))
