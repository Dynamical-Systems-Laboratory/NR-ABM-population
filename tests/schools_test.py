import sys
py_path = '../tools/'
sys.path.insert(0, py_path)

py_path = '../src/'
sys.path.insert(0, py_path)

import os
import utils as ut
from colors import *

import abm_public as public

# ------------------------------------------------------------------
#
# Tests for Schools class functionality
#
# ------------------------------------------------------------------

#
# Input
#

# File with school GIS data
school_file = 'test_data/public_places.txt'
# File with school building types
school_type_file = 'test_data/public_types.txt'
# File with output
school_out = 'test_data/school_output.txt'
# Expected number of workplaces
n_tot = 5 

#
# Test
#

# First remove the old file
if os.path.exists(school_out):
	os.remove(school_out)

# Create and save
schools = public.Schools(school_file, school_type_file)
with open(school_out, 'w') as fout:
	fout.write(repr(schools))

# Check number of workplaces
equal = lambda x, y: x == y 
ut.test_pass(equal(schools.ntot, n_tot), "Number of schools")


