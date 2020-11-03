# ------------------------------------------------------------------
#
#	Module for testing generated agents 
#
# ------------------------------------------------------------------

def print_age_distribution(fname, ranges, agents):
	''' Write obtained age distribution as defined in ranges.'''
	
	# Ranges is a list of tuples with components 
	#	(min age, max age) as ints for each range.
	# fname - output file name
	# agents - list of agents (dicts)
	# Saves as percent of total population

	# Create a dict with ranges for summing
	age_ranges = {}
	for min_age, max_age in ranges:
		key = str(min_age) + '-' + str(max_age)
		age_ranges[key] = 0

	# Classify all agents into age groups
	for agent in agents:
		for min_age, max_age in ranges:
			if (agent['yrs'] >= min_age) and (agent['yrs']<=max_age):
				key = str(min_age) + '-' + str(max_age)
				age_ranges[key] += 1
				continue
	
	# Compute percents
	for key, value in age_ranges.items():
		age_ranges[key] /= len(agents)
		age_ranges[key] *= 100

	# Print to file
	with open(fname, 'w') as fout:
		for key, value in age_ranges.items():
			fout.write(key + ' ' + str(value) + '\n')

def print_other_sizes(fname, agents, tagW, tagRS, keyType):
	''' Computes and saves info on places that have both employees and
		another agent type associated with them '''
		
	#
	# tagW - key that identifies type of place/workplace e.g. 'worksSchool'
	# tagRS - key that identifies if the agent is the second associated
	#			type e.g. student or RetirementHome
	# keyType - key that identifies ID of the place 
	#

	# Dict with place ID vs. number of agents working and living/studying
	# stored as a list
	places = {}

	# Count agents belonging to the same household
	for agent in agents:
		if agent[tagRS]:
			if str(agent[keyType]) in places:
				places[str(agent[keyType])][1] += 1
			else:
				places[str(agent[keyType])] = [0, 1]
		if agent[tagW]:
			if str(agent['workID']) in places:
				places[str(agent['workID'])][0] += 1
			else:
				places[str(agent['workID'])] = [1, 0]

	# Save to file
	with open(fname, 'w') as fout:
		for key, value in places.items():
			fout.write(key + ' ' + str(value[0]) + ' ' + str(value[1]) + '\n')

def print_household_sizes(fname, agents):
	''' Computes and saves household size '''

	# Dict with house ID vs. number of agents living in it
	houses = {}
	retirement_homes = {}

	# Count agents belonging to the same household
	for agent in agents:
		if agent['RetirementHome'] == True:
			if str(agent['houseID']) in retirement_homes:
				retirement_homes[str(agent['houseID'])] += 1
			else:
				retirement_homes[str(agent['houseID'])] = 1
			continue

		if str(agent['houseID']) in houses:
			houses[str(agent['houseID'])] += 1
		else:
			houses[str(agent['houseID'])] = 1

	# Save to file
	with open(fname, 'w') as fout:
		for key, value in retirement_homes.items():
			fout.write(key + ' ' + str(value) + '\n')
		for key, value in houses.items():
			fout.write(key + ' ' + str(value) + '\n')

def print_household_sizes_w_coords(fname, agents):
	''' Computes and saves household size and coordinates '''

	# Dict with house ID vs. number of agents living in it
	# and location
	houses = {}
	retirement_homes = {}
	# Count agents belonging to the same household
	for agent in agents:
		if agent['RetirementHome'] == True:
			if str(agent['houseID']) in retirement_homes:
				retirement_homes[str(agent['houseID'])][0] += 1
			else:
				retirement_homes[str(agent['houseID'])] = []
				retirement_homes[str(agent['houseID'])].append(1)
				retirement_homes[str(agent['houseID'])].append((agent['lon'], agent['lat']))
			continue

		if str(agent['houseID']) in houses:
			houses[str(agent['houseID'])][0] += 1
		else:
			houses[str(agent['houseID'])] = []
			houses[str(agent['houseID'])].append(1)
			houses[str(agent['houseID'])].append((agent['lon'], agent['lat']))

	# Save to file
	with open(fname, 'w') as fout:
		for key, value in retirement_homes.items():
			fout.write(key + ' ' + str(value[0]) 
						   + ' ' + str(value[1][0])
						   + ' ' + str(value[1][1]) + '\n')
		for key, value in houses.items():
			fout.write(key + ' ' + str(value[0]) 
						   + ' ' + str(value[1][0])
						   + ' ' + str(value[1][1]) + '\n')


def print_building_sizes_w_coords(fname, agents):
	''' Computes and saves residential building size and coordinates '''

	# Dict with house ID vs. number of agents living in it
	houses = {}

	# Count agents belonging to the same household
	for agent in agents:
		agent_key = str(agent['lon']+agent['lat'])
		if agent_key in houses:
			houses[agent_key][0] += 1
		else:
			houses[agent_key] = [1,0,0]
			houses[agent_key][1] = agent['lon']
			houses[agent_key][2] = agent['lat']

	# Save to file
	with open(fname, 'w') as fout:
		for key, value in houses.items():
			fout.write(key + ' ' + str(value[0]) 
						   + ' ' + str(value[1])
						   + ' ' + str(value[2]) + '\n')

def print_workplace_sizes(fname, agents):
	''' Computes and saves workplace size '''

	# Dict with workplace ID vs. number of agents working in it
	works = {}

	# Count agents belonging to the same workplace 
	for agent in agents:
		if str(agent['workID']) in works:
			works[str(agent['workID'])] += 1
		else:
			works[str(agent['workID'])] = 1

	# Save to file
	with open(fname, 'w') as fout:
		for key, value in works.items():
			fout.write(key + ' ' + str(value) + '\n')

def print_school_sizes(fname, agents):
	''' Computes and saves school size '''

	# Dict with school ID vs. number of agents working in it
	schools = {}

	# Count agents belonging to the same school 
	for agent in agents:
		if str(agent['schoolID']) in schools:
			schools[str(agent['schoolID'])] += 1
		else:
			schools[str(agent['schoolID'])] = 1

	# Save to file
	with open(fname, 'w') as fout:
		for key, value in schools.items():
			fout.write(key + ' ' + str(value) + '\n')




