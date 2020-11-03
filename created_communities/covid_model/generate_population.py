import sys
py_path = '../../tools/'
sys.path.insert(0, py_path)

py_path = '../../src/'
sys.path.insert(0, py_path)

import utils as ut
from colors import *

import abm_residential as res
import abm_public as public
import abm_agents as agents

# ------------------------------------------------------------------
#
# Generate New Rochelle population for the COVID model
#
# ------------------------------------------------------------------

#
# Input files
#

# GIS and type data files database
dpath = '../../NewRochelle/database/'

# File with residential GIS data
res_file = dpath + 'residential.txt' 
# File with residential building types
res_type_file = dpath + 'residential_types.txt'
# File with public places GIS data
pb_file = dpath + 'public.txt'
# File with building types
pb_type_file = dpath + 'public_types.txt'

# File with age distribution
file_age_dist = '../../NewRochelle/census_data/age_distribution.txt'
# File with age distribution of the household head
file_hs_age = '../../NewRochelle/census_data/age_household_head.txt'
# File with household size distribution
file_hs_size = '../../NewRochelle/census_data/household_size.txt'

#
# Other input
#

# Total number of units (households + vacancies)
n_tot = 29645
# Fraction of vacant households
fr_vacant = 0.053
# Total number of agents
n_agents = 79205
# Assumed maximum age
max_age = 100
# Fraction of families
fr_fam = 0.6727
# Fraction of couple no children
fr_couple = 0.49
# Fraction of single parents
fr_sp = 0.25
# Fraction of households with a 60+ person
fr_60 = 0.423
# Initially infected
n_infected = 1

#
# Output files
#

rh_out = 'NR_retirement_homes.txt'
hs_out = 'NR_households.txt' 
wk_out = 'NR_workplaces.txt'
hsp_out = 'NR_hospitals.txt'
sch_out = 'NR_schools.txt'
ag_out = 'NR_agents.txt'

#
# Generate places
#

# Retirement homes
retirement_homes = public.RetirementHomes(pb_file, pb_type_file)
with open(rh_out, 'w') as fout:
	fout.write(repr(retirement_homes))

# Households 
households = res.Households(n_tot, res_file, res_type_file)
with open(hs_out, 'w') as fout:
	fout.write(repr(households))

# Workplaces 
workplaces = public.Workplaces(pb_file, pb_type_file)
with open(wk_out, 'w') as fout:
	fout.write(repr(workplaces))

# Hospitals
hospitals = public.Hospitals(pb_file, pb_type_file)
with open(hsp_out, 'w') as fout:
	fout.write(repr(hospitals))

# Schools
schools = public.Schools(pb_file, pb_type_file)
with open(sch_out, 'w') as fout:
	fout.write(repr(schools))

#
# Create the population
# 

agents = agents.Agents(file_age_dist, file_hs_age, file_hs_size, n_agents, max_age, n_tot, fr_vacant, fr_fam, fr_couple, fr_sp, fr_60, n_infected)
agents.distribute_retirement_homes(retirement_homes.retirement_homes)
agents.distribute_hospital_patients(hospitals.hospitals)
agents.distribute_households(households.households, fr_vacant)
agents.distribute_schools(schools.schools)

agents.distribute_hospitals(hospitals.hospitals, 65)
agents.distribute_other_employees(retirement_homes.retirement_homes, 'worksRH', 75)
agents.distribute_other_employees(schools.schools, 'worksSchool', 75)
agents.distribute_workplaces(workplaces.workplaces, 75)

with open(ag_out, 'w') as fout:
	fout.write(repr(agents))
