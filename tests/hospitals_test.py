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
# Tests for Hospitals class functionality
#
# ------------------------------------------------------------------

#
# Input files
#

# File with hospitals GIS data
hospitals_file = 'test_data/public_places.txt'
# File with hospitals building types
hospitals_type_file = 'test_data/public_types.txt'
# File with output
hsp_out = 'test_data/hospitals_output.txt'
# Expected number of workplaces
n_tot = 2 

#
# Test
#

# First remove the old file
if os.path.exists(hsp_out):
	os.remove(hsp_out)

# Create and save
hospitals = public.Hospitals(hospitals_file, hospitals_type_file)
with open(hsp_out, 'w') as fout:
	fout.write(repr(hospitals))

# Check number of workplaces
equal = lambda x, y: x == y 
ut.test_pass(equal(hospitals.ntot, n_tot), "Number of hospitals")


