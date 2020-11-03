# ------------------------------------------------------------------
#
#	Module for generation of households in an ABM population
#
# ------------------------------------------------------------------

import math, copy

class Households(object):
	''' Class for generation of households '''
	
	def __init__(self, n_tot, fres, res_map):
		''' Generate individual households from input data '''
		#
		# Household is defined as a single living unit
		# fr_vacant will not be occupied but will be stored and reported
		#
		# n_tot - total number of households according to census
		# fres - name of the file with residential data, first line assumed header
		# res_map - name of the file with data for mapping residential types
		#

		# Total number of households
		self.ntot = n_tot
		# Number of units per floor
		self.n_u_fl = 0

		# Data
		# Buildings
		self.res_buildings = []
		# Mapped types
		self.res_map = {}
		# Households
		self.households = []
		# Households without retirement homes if merging
		self.houses_no_ret = []

		# Load the building data and the type map 
		self.read_gis_data(fres)
		self.read_gis_types(res_map)

		# Count and create the households
		self.create_households()

	def read_gis_data(self, fname):
		''' Load GIS data on residential buidlings from a file '''
	
		with open(fname, 'r') as fin:
			# Skip the header
			next(fin)
			for line in fin:
				temp = {}
				line = line.strip().split()
				
				# Common information
				temp['type'] = line[0]
				temp['lon'] = float(line[2])
				temp['lat'] = float(line[1])
				temp['is_business_multi'] = False 

				# Units/floors
				if line[0] == 'B':
					temp['floors'] = int(line[3])
					temp['units'] = 0
				elif line[0]  == 'D':
					temp['floors'] = 0
					temp['units'] = int(line[3])			
				elif line[0] == 'A':
					temp['floors'] = 0
					temp['units'] = 0
				elif line[0] == 'C':
					# Check if and apartment building (ignoring townhouses)
					if (len(line) > 3) and (line[3].isdigit()):
						temp['floors'] = int(line[3])
						temp['units'] = 0
						temp['is_business_multi'] = True
					else:
						temp['floors'] = 0
						temp['units'] = 0
				else:
					raise ValueError('Wrong type of residential building in the input')
				self.res_buildings.append(temp)	
					
	def read_gis_types(self, fname):
		''' Loads a map with GIS residential building types and descriptions '''

		with open(fname, 'r') as fin:
			for line in fin:
				line = line.strip().split()
				self.res_map[line[0]] = (' ').join(line[2:])

	def create_households(self):
		''' Create and store all the households '''
		
		# Count all known households and floors
		self.n_u_fl, n_acd = self.compute_units_per_floor()

		# Create individual households
		temp = {}
		ID = 1
		# Total number in type B (multiunit buildings)
		cur_B = 0
		for building in self.res_buildings:
			if (building['type'] == 'A'):
				# Single household residences
				self.add_household(ID, building)
				ID += 1
			elif building['type'] == 'D':
				# Townhouses
				for unit in range(building['units']):
					self.add_household(ID, building)
					ID += 1
			elif building['type'] == 'B':
				# Apartment buildings/multi unit buildings
				n_units_bld = building['floors']*self.n_u_fl
				cur_B += n_units_bld
				for unit in range(n_units_bld):
					self.add_household(ID, building)
					ID += 1			
			elif building['type'] == 'C':
				if building['floors'] == 0:
					# Single household with a business
					self.add_household(ID, building)
					ID += 1
				else:
					# Apartment complex with a business
					n_units_bld = building['floors']*self.n_u_fl
					cur_B += n_units_bld
					for unit in range(n_units_bld):
						self.add_household(ID, building)
						ID += 1	
			else:
				raise ValueError('Wrong type of residential building in the input')
		
		# Correct for rounding - adds a unit per building until number of
		# households equals requested
		wanted_B = self.ntot - n_acd
		if not (cur_B == wanted_B):
			self.add_units(cur_B, wanted_B, ID)

	def compute_units_per_floor(self):
		''' Returns number of households per building floor 
				and total number of housholds except for multiunit 
				buildings '''
		n_fl_tot = 0
		n_u_known = 0
		for building in self.res_buildings:
			# Check if single residence and business
			single_biz = ((building['type'] == 'C') and (building['is_business_multi'] == False))
			# And same for multiunit
			multi_biz = ((building['type'] == 'C') and (building['is_business_multi'] == True))
			if (building['type'] == 'A') or single_biz:
				# Single residences count as one
				n_u_known += 1
			elif building['type'] == 'D':
				# Townhouses - one unit = one household
				n_u_known += building['units']
			elif (building['type'] == 'B') or multi_biz:
				# Accumulate total floor number
				n_fl_tot += building['floors']
			else:
				raise ValueError('Wrong type of residential building in the input')	
		n_b = self.ntot - n_u_known
		return math.floor(n_b/n_fl_tot), n_u_known

	def add_units(self, n_cur, n_wanted, ID_0):
		''' Add units to multiunit buildings to reach
				required number of households '''
		
		#
		# n_cur - current number of units in multiunit
		# n_wanted - required number
		# ID_0 - first valid ID for a household
		#

		# Extract all multiunit buildings
		multi = []
		for building in self.res_buildings:
			multi_biz =  ((building['type'] == 'C') and (building['is_business_multi'] == True))
			if (building['type'] == 'B') or multi_biz:
				multi.append(building)
		
		ID = ID_0
		m_ind = 0
		while n_cur < n_wanted:
			self.add_household(ID, multi[m_ind])
			n_cur += 1
			ID += 1
			if m_ind < len(multi)-1:
				m_ind += 1
			else:
				m_ind = 0

	def add_household(self, ID, building):
		''' Add a household entry '''
			
		temp = {}
		temp['ID'] = ID
		temp['lon'] = building['lon']
		temp['lat'] = building['lat']
			
		self.households.append(temp)

	def merge_with_retirement_homes(self, retirement_homes):
		''' Add retirement homes as households. This has to 
			be done before assigning agents to households. '''
		
		ID = len(self.households)
		self.houses_no_ret = copy.deepcopy(self.households);
		for rh in retirement_homes:
			ID += 1 
			self.add_household(ID, rh)
			# Add household ID for future reference
			rh['houseID'] = ID

	def __repr__(self):
		''' String output for stdout or files '''
		
		temp = []
		for place in self.households:
			temp.append((' ').join([str(place['ID']), str(place['lat']), str(place['lon'])])) 

		return ('\n').join(temp)


