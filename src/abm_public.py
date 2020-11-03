# ------------------------------------------------------------------
#
#	Module for generation of public places in an ABM population
#
# ------------------------------------------------------------------

import math

class Workplaces(object):
	''' Class for generation of workplaces '''

	def __init__(self, fname, fmap):
		''' Generate individual workplaces from input data. 
				Generates all but hospitals, so also 
				retirement homes as workplaces '''

		#
		# fname - input file name with all public places
		# fmap - name of the file with types and descriptions
		#

		# Total number of workplaces
		self.ntot = 0

		# Data
		# Buildings
		self.workplaces = []
		# Type map
		self.workplace_map = {}

		# Load the buildings and the map
		self.read_gis_data(fname)
		self.read_gis_types(fmap)

	def read_gis_data(self, fname):
		''' Read and store workplace data '''

		with open(fname, 'r') as fin:
			# Skip the header
			next(fin)
			ID = 0
			for line in fin:
				temp = {}
				line = line.strip().split()

				# Exclude hospitals, retirement homes, 
				# and schools
				if (line[0] is 'H') or ('AA' in line[0]) or (line[0] is 'F'):
					continue
				
				ID += 1
				# Common information
				temp['ID'] = ID
				temp['type'] = line[0]
				temp['lon'] = float(line[2])
				temp['lat'] = float(line[1])

				# Number of employees always first after
				# coordinates
				temp['num employees'] = int(line[3])

				self.workplaces.append(temp)
		self.ntot = ID

	def read_gis_types(self, fname):
		''' Loads a map with GIS public building types and descriptions '''
	
		with open(fname, 'r') as fin:
			for line in fin:
				line = line.strip().split()
				self.workplace_map[line[0]] = (' ').join(line[2:])

	def merge_with_hospitals(self, hospitals):
		''' Including hospitals for simulations where they are not 
				separate entities. This has to be done before 
				assigning agents to workplaces. '''
	
		ID = len(self.workplaces)
		for hsp in hospitals:
			ID += 1
			temp = {}
			# Common information
			temp['ID'] = ID
			temp['type'] = hsp['type']
			temp['lon'] = hsp['lon']
			temp['lat'] = hsp['lat']

			# Number of employees always first after
			# coordinates
			temp['num employees'] = hsp['num employees']

			self.workplaces.append(temp)

		self.ntot = ID

	def __repr__(self):
		''' String output for stdout or files '''
		
		temp = []
		for place in self.workplaces:
			temp.append((' ').join([str(place['ID']), str(place['lat']), str(place['lon'])])) 
	
		return ('\n').join(temp)
			
class Schools(object):
	''' Class for generation of schools '''

	def __init__(self, fname, fmap):
		''' Generate individual schools from input data '''

		#
		# fname - input file name with all public places
		# fmap - name of the file with types and descriptions
		#

		# Total number of schools 
		self.ntot = 0

		# Data
		# Buildings
		self.schools = []
		# Type map
		self.schools_map = {}

		# Type hierarhy
		self.school_types = {'daycare' : 1, 'primary' : 2, 'middle' : 3, 'high' : 4, 'college' : 5}
		self.school_strings = ['daycare', 'primary', 'middle', 'high', 'college']

		# Load the buildings and the map
		self.read_gis_data(fname)
		self.read_gis_types(fmap)

	def read_gis_data(self, fname):
		''' Read and store school data '''

		with open(fname, 'r') as fin:
			# Skip the header
			next(fin)
			ID = 0
			for line in fin:
				line = line.strip().split()

				# Include only schools
				if line[0] is not 'F':
					continue

				# If one school has multiple levels,
				# split into each level but keep min/type
				# info for reference

				# Add lowest and highest type
				school_type = line[5].split(',')
				min_type = 1000
				max_type = 0
	
				for sc in school_type:
					sc = sc.strip()
					temp_type = self.school_types[sc]
					if temp_type < min_type:
						min_type = temp_type
						min_str = sc
					if temp_type > max_type:
						max_type = temp_type
						max_str = sc
			
				i0 = self.school_strings.index(min_str)
				iF = self.school_strings.index(max_str)
				for ii in range(i0, iF+1):
					temp = {}
					temp['school min type'] = self.school_strings[i0]
					temp['school max type'] = self.school_strings[iF]

					ID += 1
					# Common information
					temp['ID'] = ID
					temp['type'] = line[0]
					temp['lon'] = float(line[2])
					temp['lat'] = float(line[1])
					temp['school type'] = self.school_strings[ii]

					# Number of students always second after
					# coordinates; round and ignore differences
					# is is approximate
					num_types = iF-i0+1
					temp['num students'] = math.floor(float(line[4])/num_types)
					temp['num employees'] = int(line[3])
					self.schools.append(temp)
				self.ntot = ID

	def read_gis_types(self, fname):
		''' Loads a map with GIS public building types and descriptions '''
	
		with open(fname, 'r') as fin:
			for line in fin:
				line = line.strip().split()
				self.schools_map[line[0]] = (' ').join(line[2:])
	
	def __repr__(self):
		''' String output for stdout or files '''
		
		temp = []
		for place in self.schools:
			temp.append((' ').join([str(place['ID']), str(place['lat']), str(place['lon']), place['school type']])) 
	
		return ('\n').join(temp)

	def print_simple(self, fname):
		''' Write basic information for simpler ABM models '''

		with open(fname, 'w') as fout:
			for place in self.schools:
				fout.write((' ').join([str(place['ID']), str(place['lat']), str(place['lon'])]))
				fout.write('\n')

class Hospitals(object):
	''' Class for generation of hospitals '''

	def __init__(self, fname, fmap):
		''' Generate individual hospitals from input data '''

		#
		# fname - input file name with all public places
		# fmap - name of the file with types and descriptions
		#

		# Total number of hospitals
		self.ntot = 0

		# Data
		# Buildings
		self.hospitals = []
		# Type map
		self.hospitals_map = {}

		# Load the buildings and the map
		self.read_gis_data(fname)
		self.read_gis_types(fmap)

	def read_gis_data(self, fname):
		''' Read and store hospital data '''

		with open(fname, 'r') as fin:
			# Skip the header
			next(fin)
			ID = 0
			for line in fin:
				temp = {}
				line = line.strip().split()

				# Include only hospitals 
				if line[0] is not 'H':
					continue
				
				ID += 1
				# Common information
				temp['ID'] = ID
				temp['type'] = line[0]
				temp['lon'] = float(line[2])
				temp['lat'] = float(line[1])

				# Number of employees
				temp['num employees'] = int(line[3])
				# Number of patients
				temp['num patients'] = int(line[4])

				self.hospitals.append(temp)

		self.ntot = ID

	def read_gis_types(self, fname):
		''' Loads a map with GIS public building types and descriptions '''
	
		with open(fname, 'r') as fin:
			for line in fin:
				line = line.strip().split()
				self.hospitals_map[line[0]] = (' ').join(line[2:])
	
	def __repr__(self):
		''' String output for stdout or files '''
		
		temp = []
		for place in self.hospitals:
			temp.append((' ').join([str(place['ID']), str(place['lat']), str(place['lon'])])) 
	
		return ('\n').join(temp)

class RetirementHomes(object):
	''' Class for generation of retirement and nursing homes '''

	def __init__(self, fname, fmap):
		''' Generate individual retirement and nursing homes from input data '''

		#
		# fname - input file name with all public places
		# fmap - name of the file with types and descriptions
		#

		# Total number of retirement and nursing homes
		self.ntot = 0

		# Data
		# Buildings
		self.retirement_homes = []
		# Type map
		self.retirement_homes_map = {}

		# Load the buildings and the map
		self.read_gis_data(fname)
		self.read_gis_types(fmap)
	
	def read_gis_data(self, fname):
		''' Read and store retirement homes data '''

		with open(fname, 'r') as fin:
			# Skip the header
			next(fin)
			ID = 0
			for line in fin:
				temp = {}
				line = line.strip().split()

				# Include only retirement homes
				if not (line[0] in 'AA'):
					continue
				
				ID += 1
				# Common information
				temp['ID'] = ID
				temp['type'] = line[0]
				temp['lon'] = float(line[2])
				temp['lat'] = float(line[1])

				# Number of employees
				temp['num employees'] = int(line[3])
				# Number of residents
				temp['num residents'] = int(line[4])

				self.retirement_homes.append(temp)

		self.ntot = ID-1

	def read_gis_types(self, fname):
		''' Loads a map with GIS public building types and descriptions '''
	
		with open(fname, 'r') as fin:
			for line in fin:
				line = line.strip().split()
				self.retirement_homes_map[line[0]] = (' ').join(line[2:])
	
	def __repr__(self):
		''' String output for stdout or files '''
		
		temp = []
		for place in self.retirement_homes:
			temp.append((' ').join([str(place['ID']), str(place['lat']), str(place['lon'])])) 
	
		return ('\n').join(temp)
