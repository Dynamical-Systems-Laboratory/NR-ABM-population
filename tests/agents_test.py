import sys
py_path = '../tools/'
sys.path.insert(0, py_path)

py_path = '../src/'
sys.path.insert(0, py_path)

import utils as ut
from colors import *

import abm_residential as res
import abm_public as public
import abm_agents as agents

# ------------------------------------------------------------------
#
# Tests for Agents class functionality
#
# ------------------------------------------------------------------

#
# Input files
#

# File with residential GIS data
res_file = 'test_data/test_residential.txt'
# File with residential building types
res_type_file = 'test_data/residential_types.txt'
# File with public places GIS data
pb_file = 'test_data/public_places.txt'
# File with building types
pb_type_file = 'test_data/public_types.txt'

# File with age distribution
file_age_dist = '../NewRochelle/census_data/age_distribution.txt'
# File with age distribution of the household head
file_hs_age = '../NewRochelle/census_data/age_household_head.txt'
# File with household size distribution
file_hs_size = '../NewRochelle/census_data/household_size.txt'

#
# Output
#

file_out = 'test_data/agents_out.txt'

#
# Other input
#

# Total number of units (households + vacancies)
n_tot = 100 
# Fraction of vacant households
fr_vacant = 0.2
# Total number of agents
n_agents = 1000
# Number of initially infected 
n_inf = 100
# Assumed maximum age
max_age = 100
# Fraction of families
fr_fam = 0.6727
# Fraction of couple no children
fr_couple = 0.49
# Fraction of single parents
fr_sp = 0.25

#
# Generate places
#

households = res.Households(n_tot, res_file, res_type_file)
# Merge with retirement homes
retirement_homes = public.RetirementHomes(pb_file, pb_type_file)
households.merge_with_retirement_homes(retirement_homes.retirement_homes)
# Hospitals
hospitals = public.Hospitals(pb_file, pb_type_file)
# Schools
schools = public.Schools(pb_file, pb_type_file)
# Workplaces
workplaces = public.Workplaces(pb_file, pb_type_file)

#
# Create the population
# 

agents = agents.Agents(file_age_dist, file_hs_age, file_hs_size, n_agents, max_age, n_tot, fr_vacant, fr_fam, fr_couple, fr_sp, n_inf)
agents.distribute_retirement_homes(retirement_homes.retirement_homes)
agents.distribute_hospital_patients(hospitals.hospitals)
agents.distribute_households(households.houses_no_ret, fr_vacant)

agents.distribute_schools(schools.schools)
agents.distribute_hospitals(hospitals.hospitals, 65)
agents.distribute_workplaces(workplaces.workplaces, 75)

with open(file_out, 'w') as fout:
	fout.write(repr(agents))
