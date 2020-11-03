# ------------------------------------------------------------------
#
#	Module for generation of ABM population (agents)
#
# ------------------------------------------------------------------

import math, random
import numpy as np
from copy import deepcopy

class Agents(object):
	''' Class for generating the population - agents '''

	def __init__(self, fname_age, fname_hs_age, fname_hs_size, ntot, max_age, n_houses, 
					fr_vacancy, fr_fam, fr_couple, fr_sp, fr_60, n_infected):
		''' Load basic data '''

		# Total number of people
		self.ntot = ntot
		# Maximum age to assume
		self.max_age = max_age
		# Number of households excluding vacant
		self.n_houses = math.floor(n_houses*(1-fr_vacancy))
		# Number of unpoulated houses
		self.rem_houses = self.n_houses
		# Fraction of families
		self.fr_families = fr_fam
		# Fraction of married couples without children
		self.fr_couple = fr_couple
		# Fraction of single parent families
		self.fr_single_parent = fr_sp
		# Fraction of households with a 60+ person
		self.fr_60 = fr_60
		# Total number of initially infected
		self.n_infected = n_infected

		# Age group : number of people in that group
		self.age_dist = self.load_age_dist(fname_age, self.ntot, 0, 4)
		# Household head age distribution
		self.hs_age_dist = self.load_age_dist(fname_hs_age, self.n_houses, 18, 34)
		# Household size distribution
		self.hs_size_dist = self.load_data(fname_hs_size)

		# Still left to distribute 
		self.age_remaining = deepcopy(self.age_dist) 

		# Current free agent ID
		self.ID = 1

		# Agents
		self.agents = []
		# List of agents in retirement homes
		self.rh_agents = []

		# Default Agent paramters
		# Deepcopy and use to create specific parameters
		self.default_parameters = {'ID':0, 'student':False, 'works':False,
							  'yrs':-1, 'lon':0, 'lat':0, 'houseID':0,
							  'isPatient':False, 'schoolID':0, 
							  'workID':0, 'worksHospital':False, 
							  'hospitalID':0, 'infected':False, 
							  'RetirementHome': False, 'worksRH': False, 
							  'worksSchool': False, 'isFamily': False}

	def load_age_dist(self, fname_age, ntot, min_age, max_min_age):
		''' Read and process an age distribution '''
		# Returns a map with age group : number of people
		# in that group

		with open(fname_age, 'r') as fin:

			# Total generated 
			cur_total = 0

			age_dist = {}    
			# First line is different
			line = next(fin)
			in_group = math.floor(float(line.strip().split()[-1])/100*ntot)
			key = str(min_age)+'-'+str(max_min_age)
			age_dist[key] = {'min': min_age, 'max': max_min_age, 'number': in_group}			
			cur_total += in_group

			for line in fin:
				line = line.strip().split()
				in_group = math.floor(float(line[-1])/100*ntot)
				if not (line[0] == '85'):
					key = line[0] + '-' + line[2]
					age_dist[key] = {'min': int(line[0]), 'max': int(line[2]), 'number': in_group}
				else:
					age_dist['85-'+str(self.max_age)] = {'min': 85, 'max': self.max_age, 'number': in_group}
				cur_total += in_group
				
			# Correct for rounding
			if cur_total != ntot:
				ind = 0
				keys = list(age_dist.keys())
				if cur_total < ntot:
					while (cur_total < ntot):
						age_dist[keys[ind]]['number'] += 1 
						cur_total += 1
						if ind < len(keys)-1:
							ind += 1
						else:
							ind = 0
				else:
					while (cur_total > ntot):
						age_dist[keys[ind]]['number'] -= 1 
						cur_total -= 1
						if ind < len(keys)-1:
							ind += 1
						else:
							ind = 0
			return age_dist

	def load_data(self, fname):
		''' Loads simple two column file into a dictionary
				with key the first and value (percents converted 
				to fractions) in the second column '''

		temp = {}
		with open(fname, 'r') as fin:
			for line in fin:
				line = line.strip().split()
				temp[line[0]] = float(line[1])/100
		return temp

	def distribute_retirement_homes(self, retirement_homes):
		''' Select agents 75+ for retirement homes '''
	
		for rh in retirement_homes:
			n_residents = rh['num residents']
			for ai in range(n_residents):
				temp = {}
				temp = deepcopy(self.default_parameters)
				# Agent ID
				temp['ID'] = self.ID
				self.ID += 1
				# Age + update
				temp['yrs'] = np.random.randint(75, self.max_age+1)
				self.update_ages(temp['yrs'])
				# Agents position
				temp['lon'] = rh['lon']
				temp['lat'] = rh['lat']
				# House ID
				temp['houseID'] = rh['ID']
				# Processing flag that it's retirement home
				temp['RetirementHome'] = True
				self.agents.append(temp)
				# List of agents in retirement homes
				self.rh_agents.append(temp)
			

	def distribute_hospital_patients(self, hospitals):
		''' Select patients with conditions other than 
				COVID, all ages '''
	
		for hosp in hospitals:
			n_patients = hosp['num patients']
			for ai in range(n_patients):
				temp = {}
				temp = deepcopy(self.default_parameters)
				# Agent ID
				temp['ID'] = self.ID
				self.ID += 1
				# Age + update
				temp['yrs'] = np.random.randint(0, self.max_age+1)
				self.update_ages(temp['yrs'])
				# Agents position
				temp['lon'] = hosp['lon']
				temp['lat'] = hosp['lat']
				# Other info
				temp['isPatient'] = True
				temp['hospitalID'] = hosp['ID']
				self.agents.append(temp)

	def distribute_households(self, households, fr_vacancy):
		''' Assign agents to households '''
		
		# fr_vacancy - fraction of vacant households
		
		# Exclude vacant
		houses_tot = len(households)
		nh_vacant = math.floor(fr_vacancy*houses_tot)
		ind_vacant = random.sample(range(1, houses_tot+1), nh_vacant)

		# Select head of each household 		
		ind_available = list(set(range(1,houses_tot+1))-set(ind_vacant))
		household_heads = self.select_household_heads(households, ind_available)
	
		# Select household type for each head
		# Returns total number of households in each category
		hs_size_totals = self.assign_household_type(household_heads)
		# Assign remaining agents
		self.complete_households(hs_size_totals, household_heads, households)

	def update_ages(self, age):
		''' Reduce the number of agents in a given age group by 1 '''
		
		key = self.find_age_range(age)
		self.age_remaining[key]['number'] -= 1
		if self.age_remaining[key]['number'] < 0:
			self.age_remaining[key]['number'] = 0
			raise RuntimeError('Number of agents in the age group below zero')

	def find_age_range(self, age):
		''' Find the range in which the age is '''

		found_range = False
		for key, value in self.age_remaining.items():
			if (age >= value['min']) and (age <= value['max']):
				found_range = True
				break
		if not found_range:
			raise RuntimeError('Agents age not found in the age groups')
		return key

	def select_household_heads(self, households, house_ind):
		''' Defines the head of the household 
				and stores relevant information ''' 

		household_heads = []
		for key, value in self.hs_age_dist.items():
			for head in range(value['number']):
				temp = {}
				temp = deepcopy(self.default_parameters)

				# Randomly select index and remove it
				# These are actually IDs
				ind = house_ind[random.sample(range(0, len(house_ind)), 1)[0]]
				house_ind.remove(ind)
					
				# Select specific age
				spec_age = np.random.randint(value['min'], value['max']+1)
				# Maintain 60+ fraction
				while (spec_age >= 60) and (np.random.uniform(0,1) > self.fr_60): 
					spec_age = np.random.randint(value['min'], value['max']+1)
				age_dist_key = self.find_age_range(spec_age)
	
				# Remove that age from total poll and create agent entry
				self.update_ages(spec_age)
				# Agent ID
				temp['ID'] = self.ID
				self.ID += 1
				# Age + update
				temp['yrs'] = spec_age 
				# Agents position
				temp['lon'] = households[ind-1]['lon']
				temp['lat'] = households[ind-1]['lat']
				# House ID
				temp['houseID'] = households[ind-1]['ID']
				self.agents.append(temp)

				# Add an entry to head storage
				household_heads.append({'ID': temp['ID'], 'yrs' : spec_age, 'houseID': temp['houseID'], 'lon' : temp['lon'], 'lat': temp['lat']})

		return household_heads
			
	def assign_household_type(self, household_heads):
		''' Associate a household type with a 
				head - randomly '''
	
		# Turn percents into numbers
		h_tot = len(household_heads)
		hs_numbers = {}
		h_cur = 0
		for h_size, value in self.hs_size_dist.items():
			hs_numbers[h_size] = math.floor(value*h_tot)
			h_cur += hs_numbers[h_size]
		# Correction
		if h_cur != h_tot:
			size_range = list(self.hs_size_dist.keys())
			ind = 0
			len_keys = len(size_range)
			while (h_cur < h_tot):
				hs_numbers[size_range[ind]] += 1
				h_cur += 1
				if ind < len_keys - 1:
					ind += 1
				else:
					ind = 0

		# For later calculation - totals
		hs_total_numbers = deepcopy(hs_numbers)

		# Now randomly distribute the agents
		# using the dict with actual numbers of each houseld type
		for agent in household_heads:
			h_ind = np.random.randint(1,5)
			h_size = hs_numbers[str(h_ind)]
			if h_size > 0:
				hs_numbers[str(h_ind)] -= 1
				agent['household size'] = h_ind
			else:
				# Pick next available
				found_household = False
				for key, value in hs_numbers.items():
					if value > 0:
						agent['household size'] = int(key)
						hs_numbers[key] -= 1
						found_household = True
						break
				if found_household == False:
					raise RuntimeError('Not enough households for household heads')

		return hs_total_numbers

	def complete_households(self, hs_size_totals, household_heads, households):
		''' Assign remaining agents to households based on heads and 
				household sizes; assumes max parent age is 60 '''

		# IDs of houses that have 4+ members for correction
		houses_4p = []

		for head in household_heads:
			# Nothing to do for one person	
			if head['household size'] == '1':
				continue
			elif  head['household size'] == 2:
				# Probability a family
				if (np.random.uniform(0,1) <= self.fr_families):
					# Probability a married couple, no children
					if head['yrs'] > 60:
						# Married couple
						self.add_spouse(head)
					else:
						if (np.random.uniform(0,1) <= self.fr_couple):
							# Married couple
							self.add_spouse(head)
						else:
							# Single parent + one child
							self.add_children(head, 1, head['yrs'], head['yrs'])
				else:
					# Not a family
					# Add a random age roommate or child that is not own
					# Preference to former (not own children are a small
					# fraction)
					self.add_agent_iterate_age(head, 18, self.max_age)
			elif head['household size'] == 3:
				# Probability a family
				if ((np.random.uniform(0,1) <= self.fr_families) and (head['yrs'] <= 60)):
					# Probability single parent 
					if (np.random.uniform(0,1) <= self.fr_single_parent):
						# Add two children
						self.add_children(head, 2, head['yrs'], head['yrs'])
					else:
						# Add a spouse
						spouse = self.add_spouse(head)
						# Add a child
						self.add_children(head, 1, head['yrs'], spouse['yrs'])
				else:
					# Not a family
					# Add two random age roommates 18+
					# Less preferably a child that is not a family member
					for i in range(2):
						self.add_agent_iterate_age(head, 18, self.max_age)

			elif head['household size'] == 4:
				# Probability a family
				if ((np.random.uniform(0,1) <= self.fr_families) and (head['yrs'] <= 60)):					
					# Probability single parent 
					if (np.random.uniform(0,1) <= self.fr_single_parent):
						# Add three children
						self.add_children(head, 3, head['yrs'], head['yrs'])
						houses_4p.append({'houseID' : head['houseID'], 'size' : 4})
					else:
						# Add a spouse
						spouse = self.add_spouse(head)
						# Add two children
						self.add_children(head, 2, head['yrs'], spouse['yrs'])
						houses_4p.append({'houseID' : head['houseID'], 'size' : 4})
				else:
					# Not a family
					# Add three random age roommates 18+
					# Or not own children
					for i in range(3):
						self.add_agent_iterate_age(head, 18, self.max_age)
					houses_4p.append({'houseID' : head['houseID'], 'size' : 4})
			
		self.household_agents_correction(houses_4p, households)

	def add_children(self, head, n_children, age_1, age_2):
		''' Add n_children to agents of age_1 and age_2 '''

		parent_min = min(age_1, age_2)
		parent_max = max(age_1, age_2)

		# Children age range - hardcoded to 18-43 age difference
		# with parent but not strongly enforced
		min_age = max(0, min(17, parent_max-43)) 
		max_age = max(0, min(17, parent_min-18))

		# Find children in range, if not available in that range
		# add any age
		for ni in range(n_children):
			self.add_agent_iterate_age(head, min_age, max_age, True)
		self.agents[head['ID']-1]['isFamily'] = True

	def add_spouse(self, head):
		''' Add spouse with constraints of age difference max 
				15 years '''
		
		min_age = max(18, head['yrs']-15)
		max_age = min(self.max_age, head['yrs']+15)

		# Try adding in range, if not any age 
		# like roommate, family, etc.
		temp = self.add_agent_iterate_age(head, min_age, max_age, True)
		self.agents[head['ID']-1]['isFamily'] = True
		return temp

	def add_agent_iterate_age(self, head, min_age, max_age, family = False):	
		''' Find and register agent with age in min/max range.
				If range depleted - add random age. '''
	
		if min_age > (max_age+1):
			temp = max_age+1
			max_age = min_age
			min_age = temp
		if min_age == max_age + 1:
			max_age = min(100, max_age+2)

		agent_age = np.random.randint(min_age, max_age+1)
		key = self.find_age_range(agent_age)

		if self.age_remaining[key]['number'] == 0:
			flag_60 = False
			# Add any age that is not zero and less than 60
			while (self.age_remaining[key]['number'] == 0) or flag_60 == True:
				flag_60 = False
				agent_age = np.random.randint(0, self.max_age+1)
				if agent_age >= 60:
					if (np.random.uniform(0,1) > self.fr_60):
						flag_60 = True
						continue
				key = self.find_age_range(agent_age)

		self.update_ages(agent_age)
		
		# Once found, assign
		temp = {}
		temp = deepcopy(self.default_parameters)
		# Agent ID
		temp['ID'] = self.ID
		self.ID += 1
		# Age + update
		temp['yrs'] = agent_age 
		# Agents position
		temp['lon'] = head['lon']
		temp['lat'] = head['lat']
		# House ID
		temp['houseID'] = head['houseID']
		# Family status - just for tracking
		temp['isFamily'] = family

		self.agents.append(temp)
		return temp

	def household_agents_correction(self, houses_4p, households):
		''' Assign remanining agents to 4+ households and 
				retirement homes '''
		
		# Simple random assignment for now
		num_houses = len(houses_4p)
		num_rh = len(self.rh_agents)
		
		for key, value in self.age_remaining.items():
			while not (value['number'] == 0):
				agent_age = np.random.randint(value['min'], value['max']+1)
				self.update_ages(agent_age)
				
				temp = deepcopy(self.default_parameters)
				if agent_age >= 60:
					# Determine if placed in a household 
					if (np.random.uniform(0,1) <= self.fr_60):
						ind4p = np.random.randint(0, num_houses)
						houseID = houses_4p[ind4p]['houseID']
						houses_4p[ind4p]['size'] += 1
					else:
						# Place in a retirment home
						indRH = np.random.randint(0, num_rh)
						houseID = self.rh_agents[indRH]['houseID']
						temp['RetirementHome'] = True
				else:
					ind4p = np.random.randint(0, num_houses)
					houseID = houses_4p[ind4p]['houseID']
					houses_4p[ind4p]['size'] += 1

				# Agent ID
				temp['ID'] = self.ID
				self.ID += 1
				# Age + update
				temp['yrs'] = agent_age 
				# Agents position
				temp['lon'] = households[int(houseID)-1]['lon']
				temp['lat'] = households[int(houseID)-1]['lat']
				# House ID
				temp['houseID'] = houseID
				self.agents.append(temp)	

	def distribute_schools(self, schools):
		''' Assigns school IDs (daycare - college) to agents '''

		# Preprocess for easier usage
		all_schools = {'daycare':[], 'primary':[], 'middle':[], 
						'high':[], 'college':[]}
		
		for school in schools:
			all_schools[school['school type']].append({'ID':school['ID'], 'num students' : school['num students']})

		school_ages = {'daycare': [0,1,2,3,4], 'primary' : [5,6,7,8,9,10],
						'middle': [11,12,13], 'high' : [14,15,16,17],
						'college': [18,19,20,21]}

		# Loop through agents and assign school based on age
		for agent in self.agents:
			age = agent['yrs']
			# Exclude agents that are assumed to be out of school
			if (age > 21) or (agent['isPatient'] == True):
				continue
			# Select school type and available schools
			for key, value in school_ages.items():
				if age in value:
					spec_schools = all_schools[key]
					school_type = key
					
			# Assign first that's non zero
			found_school = False
			for scl in spec_schools:
				if scl['num students'] == 0:
					continue
				found_school = True
				agent['student'] = True
				agent['schoolID'] = scl['ID']
				scl['num students'] -= 1
				break

			# If all are zero and not daycare or college  - assign randomly
			if (found_school == False) and (school_type != 'daycare') and (school_type != 'college'):
				agent['student'] = True
				agent['schoolID'] = spec_schools[np.random.randint(0,len(spec_schools))]['ID']
			else:
				continue
	
	def distribute_other_employees(self, workplaces, tag, max_working_age):
		''' Assigns school or retirement home IDs to school/RH employees '''
	
		# max_working_age - max age to work at a give workplace type 

		temp_workplaces = deepcopy(workplaces)

		can_work = []
		for agent in self.agents:
			age = agent['yrs']
			# Exclude agents not within working age, patients and retirement homes residents,
			# And agents already working in one of the special categories
			if ((age < 16) or (age > max_working_age)): 
				continue
			if (agent['isPatient'] == True) or (agent['RetirementHome'] == True):
				continue
			if (agent['worksHospital'] == True) or (agent['worksSchool'] == True) or (agent['worksRH'] == True):
				continue

			# Random choice if working in this category
			# To avoid having agents in the same household working there
			if np.random.uniform(0,1) > 0.8:
				can_work.append(int(agent['ID']))
				continue

			for workplace in temp_workplaces:
				if workplace['num employees'] > 0:
					agent[tag] = True
					agent['works'] = True
					agent['workID'] = workplace['ID']
					workplace['num employees'] -= 1
					break

		# If missing - random choice of qualitfying
		for workplace in temp_workplaces:
			while workplace['num employees'] > 0:
				agID = random.shuffle(can_work).pop()	
				agent = self.agents[agID-1]
				agent[tag] = True
				agent['works'] = True
				agent['workID'] = workplace['ID']
				school['num employees'] -= 1	

	def distribute_hospitals(self, hospitals, max_working_age):
		''' Assigns hospital IDs to hospital employees '''

		# max_working_age - max age to work in a hospital

		temp_hospitals = deepcopy(hospitals)

		for agent in self.agents:
			age = agent['yrs']
			# Exclude agents not within working age, patients and retirement homes residents 
			if ((age < 16) or (age > max_working_age)): 
				continue
			if (agent['isPatient'] == True) or (agent['RetirementHome'] == True):
				continue
			# And agents already working in any of these categories
			if (agent['worksHospital'] == True) or (agent['worksSchool'] == True) or (agent['worksRH'] == True):
				continue

			# Random choice if working in a hospital
			# To avoid having agents in the same household working there
			if np.random.uniform(0,1) > 0.5:
				continue

			for hospital in temp_hospitals:
				if hospital['num employees'] > 0:
					agent['worksHospital'] = True
					agent['hospitalID'] = hospital['ID']
					hospital['num employees'] -= 1
					break
				

	def distribute_workplaces(self, workplaces, max_working_age):
		''' Assigns workplace IDs to agents within working age '''

		# max_working_age - max age to work 

		temp_workplaces = deepcopy(workplaces)

		for agent in self.agents:
			age = agent['yrs']
			# Exclude agents not within working age, 
			# hospital employees and non-covid patients 
			# and retirement homes residents 
			if ((age < 16) or (age > max_working_age)): 
				continue
			if (agent['isPatient'] == True) or (agent['worksHospital'] == True):
				continue
			if (agent['RetirementHome'] == True):
				continue
			# And agents already working in any of these categories
			if (agent['worksHospital'] == True) or (agent['worksSchool'] == True) or (agent['worksRH'] == True):
				continue

			for workplace in temp_workplaces:
				if workplace['num employees'] > 0:
					agent['works'] = True
					agent['workID'] = workplace['ID']
					workplace['num employees'] -= 1
					break

	def print_agents_seir(self, fname, n_infected_0):
		''' Creates a file for seir model with agents 
				working at a hospital and hospital non-covid
				patients ommitted. '''

		self.set_infected(n_infected_0)
		with open(fname, 'w') as fout:
			for agent in self.agents:
				data = (' ').join([str(int(agent['student'])), str(int(agent['works'])), 
									str(agent['yrs']), str(agent['lon']), str(agent['lat']), 
									str(agent['houseID']), '0', str(agent['schoolID']), str(agent['workID']), 
									'0', '0', str(int(agent['infected']))])
				fout.write(data)
				fout.write('\n')


	def print_agents_basic(self, fname, n_infected_0):
		''' Creates a file with basic angent information like 
				for the DSL-ABM SIS code with randomly 
				chosen initially infected agents. '''

		self.set_infected(n_infected_0)
		with open(fname, 'w') as fout:
			for agent in self.agents:
				data = (' ').join([str(int(agent['student'])), str(int(agent['works'])), 
									str(agent['yrs']), str(agent['lat']), str(agent['lon']), 
									str(agent['houseID']), str(agent['schoolID']), str(agent['workID']),
									str(int(agent['infected']))])
				fout.write(data)
				fout.write('\n')

	def set_infected(self, n_infected_0):
		''' Randomly chooses n_infected_0 agents to be initially
				infected '''

		# Indices of agents that are infected
		infected_index = random.sample(range(0, len(self.agents)), n_infected_0)
		for idx in infected_index:
			self.agents[idx]['infected'] = True	

	def __repr__(self):
		''' String output for stdout or files '''

		self.set_infected(self.n_infected)
		temp = []
		for agent in self.agents:
			temp.append((' ').join([str(int(agent['student'])), str(int(agent['works'])), 
									str(agent['yrs']), str(agent['lon']), str(agent['lat']), 
									str(agent['houseID']), str(int(agent['isPatient'])), 
									str(agent['schoolID']), str(int(agent['RetirementHome'])),
									str(int(agent['worksRH'])), str(int(agent['worksSchool'])),
									str(agent['workID']), str(int(agent['worksHospital'])), 
									str(agent['hospitalID']), str(int(agent['infected']))])) 
	
		return ('\n').join(temp)

