# ------------------------------------------------------------------
#
#	Check generated population 
#
# ------------------------------------------------------------------

import sys
py_path = '../../src/'
sys.path.insert(0, py_path)

py_path = '../../input_verification/'
sys.path.insert(0, py_path)

import check_agents as ca
import check_households as ch
import abm_residential as res
import abm_public as public
import abm_agents as agents

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
n_infected = 100

#
# Output files
#

ad_file = 'check_age_dist.txt'
rh_file = 'check_retirement_home_size.txt'
hs_file = 'check_household_size.txt'
wk_file = 'check_workplace_size.txt'
sch_file = 'check_school_size.txt'

hs_age_file = 'household_age_dist.txt'
hs_work_file = 'household_work_dist.txt'
fm_work_file = 'family_work_dist.txt'
hs_work_ID_file = 'household_work_ID_dist.txt'
hs_school_file = 'household_school_dist.txt'

# Household coordinates and sizes
hs_coords_sizes = 'check_hs_size_w_coords.txt'
building_coords_sizes = 'check_bld_size_w_coords.txt'

#
# Generate places
#

# Households and retirement homes
households = res.Households(n_tot, res_file, res_type_file)
retirement_homes = public.RetirementHomes(pb_file, pb_type_file)

# Workplaces and hospitals 
workplaces = public.Workplaces(pb_file, pb_type_file)
hospitals = public.Hospitals(pb_file, pb_type_file)

# Schools
schools = public.Schools(pb_file, pb_type_file)

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

#
# Check the generated population
# 

# Age distribution
age_groups = [(0,4),(5,9),(10,14),(15,19),(20,24),(25,34),(35,44),(45,54),(55,59),(60,64),(65,74),(75,84),(85,max_age)]
ca.print_age_distribution(ad_file, age_groups, agents.agents)

# Retirement home sizes - employees and residents
ca.print_other_sizes(rh_file, agents.agents, 'worksRH', 'RetirementHome', 'houseID')
# Schools - employees and schools
ca.print_other_sizes(sch_file, agents.agents, 'worksSchool', 'student', 'schoolID')

# Household sizes
ca.print_household_sizes(hs_file, agents.agents)
ca.print_household_sizes_w_coords(hs_coords_sizes, agents.agents)
ca.print_building_sizes_w_coords(building_coords_sizes, agents.agents)

# Workplace sizes
ca.print_workplace_sizes(wk_file, agents.agents)

# Household characteristics
ch.print_houses_and_age(hs_age_file, agents.agents)
ch.print_houses_and_work_status(hs_work_file, fm_work_file, agents.agents)
ch.print_houses_and_work_ID(hs_work_ID_file, agents.agents)
ch.print_houses_and_student_status(hs_school_file, agents.agents)



