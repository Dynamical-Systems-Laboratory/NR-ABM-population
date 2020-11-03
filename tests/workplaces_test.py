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
# Tests for Workplaces class functionality
#
# ------------------------------------------------------------------

#
# Input
#

# File with workplace GIS data
work_file = 'test_data/public_places.txt'
# File with workplace building types
work_type_file = 'test_data/public_types.txt'
# File with output
work_out = 'test_data/work_output.txt'
# Expected number of workplaces
n_tot = 14

#
# Test
#

# First remove the old file
if os.path.exists(work_out):
	os.remove(work_out)

# Create and save
workplaces = public.Workplaces(work_file, work_type_file)
with open(work_out, 'w') as fout:
	fout.write(repr(workplaces))

# Check number of workplaces
equal = lambda x, y: x == y 
ut.test_pass(equal(workplaces.ntot, n_tot), "Number of workplaces")
