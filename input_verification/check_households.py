# ------------------------------------------------------------------
#
#	Module for testing household structure 
#
# ------------------------------------------------------------------

def print_houses_and_age(fname, agents):
	''' Outputs house ID | age of every agent that lives there '''

	# Dict with house ID vs. a list of agent ages 
	houses = {}
	retirement_homes = {}

	for agent in agents:
		if agent['RetirementHome'] == True:
			if str(agent['houseID']) in retirement_homes:
				retirement_homes[str(agent['houseID'])].append(agent['yrs'])
			else:
				retirement_homes[str(agent['houseID'])] = []
				retirement_homes[str(agent['houseID'])].append(agent['yrs'])
			continue

		if str(agent['houseID']) in houses:
			houses[str(agent['houseID'])].append(agent['yrs'])
		else:
			houses[str(agent['houseID'])] = []
			houses[str(agent['houseID'])].append(agent['yrs'])

	# Save to file
	with open(fname, 'w') as fout:
		for key, value in retirement_homes.items():
			fout.write(key + ' ' + (' ').join([str(x) for x in value]) + '\n')
		for key, value in houses.items():
			fout.write(key + ' ' + (' ').join([str(x) for x in value]) + '\n')

def print_houses_and_work_status(fname, fname_fam, agents):
	''' Outputs house ID | and work flag of every 
			agent that lives there; includes the hospitals '''

	# fname_fam is for separate file with families

	# Dict with house ID vs. a list of agent ages 
	houses = {}
	families = {}
	retirement_homes = {}

	for agent in agents:
		works = agent['works'] or agent['worksHospital']
		if agent['RetirementHome'] == True:
			if str(agent['houseID']) in retirement_homes:
				retirement_homes[str(agent['houseID'])].append(works)
			else:
				retirement_homes[str(agent['houseID'])] = []
				retirement_homes[str(agent['houseID'])].append(works)
			continue

		if str(agent['houseID']) in houses:
			houses[str(agent['houseID'])].append(works)
		else:
			houses[str(agent['houseID'])] = []
			houses[str(agent['houseID'])].append(works)
			
		if agent['isFamily'] == True:
			if str(agent['houseID']) in families:
				families[str(agent['houseID'])].append(works)
			else:
				families[str(agent['houseID'])] = []
				families[str(agent['houseID'])].append(works)

	# Save to file
	with open(fname, 'w') as fout:
		for key, value in retirement_homes.items():
			fout.write(key + ' ' + (' ').join([str(x) for x in value]) + '\n')
		for key, value in houses.items():
			fout.write(key + ' ' + (' ').join([str(x) for x in value]) + '\n')
	with open(fname_fam, 'w') as fout:
		for key, value in families.items():
			fout.write(key + ' ' + (' ').join([str(x) for x in value]) + '\n')

def print_houses_and_work_ID(fname, agents):
	''' Outputs house ID | and work ID of every 
			agent that lives there; no work is marked as 0; 
			hospitals are marked by a negative value '''

	# Dict with house ID vs. a list of agent ages 
	houses = {}

	for agent in agents:
		if agent['works']:
			ID = agent['workID']
		elif agent['worksHospital']:
			ID = -1*agent['hospitalID']
		else:
			ID = 0
 
		if str(agent['houseID']) in houses:
			houses[str(agent['houseID'])].append(ID)
		else:
			houses[str(agent['houseID'])] = []
			houses[str(agent['houseID'])].append(ID)

	# Save to file
	with open(fname, 'w') as fout:
		for key, value in houses.items():
			fout.write(key + ' ' + (' ').join([str(x) for x in value]) + '\n')

def print_houses_and_student_status(fname, agents):
	''' Outputs house ID | and student flag of every 
			agent that lives there; includes the hospital '''

	# Dict with house ID vs. a list of agent ages 
	houses = {}
	retirement_homes = {}

	for agent in agents:
		if agent['RetirementHome'] == True:
			if str(agent['houseID']) in retirement_homes:
				retirement_homes[str(agent['houseID'])].append(agent['student'])
			else:
				retirement_homes[str(agent['houseID'])] = []
				retirement_homes[str(agent['houseID'])].append(agent['student'])
			continue

		if str(agent['houseID']) in houses:
			houses[str(agent['houseID'])].append(agent['student'])
		else:
			houses[str(agent['houseID'])] = []
			houses[str(agent['houseID'])].append(agent['student'])

	# Save to file
	with open(fname, 'w') as fout:
		for key, value in retirement_homes.items():
			fout.write(key + ' ' + (' ').join([str(x) for x in value]) + '\n')
		for key, value in houses.items():
			fout.write(key + ' ' + (' ').join([str(x) for x in value]) + '\n')


