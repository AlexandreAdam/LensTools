import os

from distutils import config
from ConfigParser import NoOptionError

import numpy as np
import astropy.units as u


############################################################
#############EnvironmentSettings class######################
############################################################

class EnvironmentSettings(object):

	"""
	This class handles the system specific environment settings, such as directory paths, modules, etc...

	"""

	def __init__(self,home="SimTest/Home",storage="SimTest/Storage"):

		"""
		Creates the home (meant to store small files like execution scripts) and storage (meant to store large files like simulation outputs) directories

		:param home: name of the simulation home directory
		:type home: str.

		:param storage: name of the simulation mass storage directory
		:type storage: str.

		"""

		self.home = home
		self.storage = storage


	@classmethod
	def read(cls,config_file):

		#Read the options from the ini file
		options = config.ConfigParser()
		options.read([config_file])

		#Check that the config file has the appropriate section
		section = "EnvironmentSettings"
		assert options.has_section(section),"No {0} section in configuration file {1}".format(section,config_file)

		#Fill in the appropriate fields and return to user
		return cls(home=options.get(section,"home"),storage=options.get(section,"storage"))

#################################################
###########NGenICSettings class##################
#################################################

class NGenICSettings(object):

	"""
	Class handler of NGenIC settings
	
	"""

	def __init__(self,**kwargs):

		self.GlassFile = "dummy_glass_little_endian.dat"
		self.Redshift = 100.0

		self.SphereMode = 1 
		self.WhichSpectrum = 2

		self.InputSpectrum_UnitLength_in_cm = 3.085678e24
		self.ReNormalizeInputSpectrum = 1
		self.ShapeGamma = 0.21
		self.PrimordialIndex = 1.0

		self.NumFilesWrittenInParallel = 4

		self.UnitLength_in_cm = 3.085678e21
		self.UnitMass_in_g = 1.989e43
		self.UnitVelocity_in_cm_per_s = 1e5

		#Typically do not touch these, needed for prefactors calculations
		self._zminact = 0.0
		self._zmaxact = 110.0
		self._iwmode = 3
		self._delz = 0.000001

		#Allow for kwargs override
		for key in kwargs.keys():
			setattr(self,key,kwargs[key])


#################################################
###########PlaneSettings class###################
#################################################

class PlaneSettings(object):

	"""
	Class handler of plane generation settings

	"""

	def __init__(self,**kwargs):

		#Name of the planes batch
		self.directory_name = "Planes"
		
		#Use the pickled options generated at the moment of the batch generation (advised)
		self.override_with_local = True

		self.format = "fits"
		self.plane_resolution = 128
		self.first_snapshot = 46
		self.last_snapshot = 58
		self.cut_points = np.array([7.5/0.7]) * u.Mpc
		self.thickness = (2.5/0.7) * u.Mpc 
		self.length_unit = u.Mpc
		self.normals = range(3)

		#Allow for kwargs override
		for key in kwargs.keys():
			setattr(self,key,kwargs[key])

	@classmethod
	def read(cls,config_file):

		#Read the options from the ini file
		options = config.ConfigParser()
		options.read([config_file])

		#Check that the config file has the appropriate section
		section = "PlaneSettings"
		assert options.has_section(section),"No {0} section in configuration file {1}".format(section,config_file)

		#Fill in the appropriate fields
		settings = cls()
		
		settings.directory_name = options.get(section,"directory_name")
		settings.override_with_local = options.getboolean(section,"override_with_local")
		settings.format = options.get(section,"format")
		settings.plane_resolution = options.getint(section,"plane_resolution")
		settings.first_snapshot = options.getint(section,"first_snapshot")
		settings.last_snapshot = options.getint(section,"last_snapshot")

		#Length units
		settings.length_unit = getattr(u,options.get(section,"length_unit"))

		#Cut points
		settings.cut_points = np.array([ float(p) for p in options.get(section,"cut_points").split(",") ]) * settings.length_unit
		settings.thickness = options.getfloat(section,"thickness") * settings.length_unit

		#Normals
		settings.normals = [ int(n) for n in options.get(section,"normals").split(",") ]

		#Return to user
		return settings


#################################################
###########MapSettings class#####################
#################################################

class MapSettings(object):

	"""
	Class handler of map generation settings

	"""

	def __init__(self,**kwargs):

		#Names of the map batch
		self.directory_name = "Maps"

		#Use the options generated at the moment of the batch generation (advised)
		self.override_with_local = True

		self.format = "fits"
		self.map_resolution = 128
		self.map_angle = 1.6 * u.deg
		self.angle_unit = u.deg
		self.source_redshift = 2.0

		#Random seed used to generate multiple map realizations
		self.seed = 0

		#Set of lens planes to be used during ray tracing
		self.plane_set = "Planes"

		#N-body simulation realizations that need to be mixed
		self.mix_nbody_realizations = [1]
		self.mix_cut_points = [0]
		self.mix_normals = [0]
		self.lens_map_realizations = 4

		#Which lensing quantities do we need?
		self.convergence = True
		self.shear = False
		self.omega = False

		#Allow for kwargs override
		for key in kwargs.keys():
			setattr(self,key,kwargs[key])

	@classmethod
	def read(cls,config_file):

		#Read the options from the ini file
		options = config.ConfigParser()
		options.read([config_file])

		#Check that the config file has the appropriate section
		section = "MapSettings"
		assert options.has_section(section),"No {0} section in configuration file {1}".format(section,config_file)

		#Fill in the appropriate fields
		settings = cls()

		settings.directory_name = options.get(section,"directory_name")
		settings.override_with_local = options.getboolean(section,"override_with_local")
		settings.format = options.get(section,"format")
		settings.map_resolution = options.getint(section,"map_resolution")
		
		settings.angle_unit = getattr(u,options.get(section,"angle_unit"))
		settings.map_angle = options.getfloat(section,"map_angle") * settings.angle_unit
		
		settings.source_redshift = options.getfloat(section,"source_redshift")

		settings.seed = options.getint(section,"seed")
		settings.plane_set = options.get(section,"plane_set")
		settings.mix_nbody_realizations = [ int(n) for n in options.get(section,"mix_nbody_realizations").split(",") ]
		settings.lens_map_realizations = options.getint(section,"lens_map_realizations")
		settings.mix_cut_points = [ int(n) for n in options.get(section,"mix_cut_points").split(",") ]
		settings.mix_normals = [ int(n) for n in options.get(section,"mix_normals").split(",") ]

		settings.convergence = options.getboolean(section,"convergence")
		settings.shear = options.getboolean(section,"shear")
		settings.omega = options.getboolean(section,"omega")

		#Return to user
		return settings

#####################################################
###########CatalogSettings class#####################
#####################################################

class CatalogSettings(object):

	"""
	Class handler of simulated catalog generation settings

	"""

	def __init__(self,**kwargs):
	
		#Name of catalog batch
		self.directory_name = "Catalog"
		self.input_files = "galaxy_positions.fits"
		self.total_num_galaxies = 1000
		self.catalog_angle_unit = u.deg

		#Use the options generated at the moment of the batch generation (advised)
		self.override_with_local = True

		#Format of the simulated catalog files
		self.format = "fits"

		#Random seed used to generate multiple catalog realizations
		self.seed = 0

		#Set of lens planes to be used during ray tracing
		self.plane_set = "Planes"

		#N-body simulation realizations that need to be mixed
		self.mix_nbody_realizations = [1]
		self.mix_cut_points = [0]
		self.mix_normals = [0]
		self.lens_catalog_realizations = 1

		#Allow for kwargs override
		for key in kwargs.keys():
			setattr(self,key,kwargs[key])


	@classmethod
	def read(cls,config_file):

		#Read the options from the ini file
		options = config.ConfigParser()
		options.read([config_file])

		#Check that the config file has the appropriate section
		section = "CatalogSettings"
		assert options.has_section(section),"No {0} section in configuration file {1}".format(section,config_file)

		#Fill in the appropriate fields
		settings = cls()

		#Name of catalog batch
		settings.directory_name = options.get(section,"directory_name")
		settings.input_files = options.get(section,"input_files").split(",")
		settings.total_num_galaxies = options.getint(section,"total_num_galaxies")
		settings.catalog_angle_unit = getattr(u,options.get(section,"catalog_angle_unit"))

		#Use the options generated at the moment of the batch generation (advised)
		settings.override_with_local = options.getboolean(section,"override_with_local")

		#Format of the simulated catalog files
		settings.format = options.get(section,"format")

		#Set of lens planes to be used during ray tracing
		settings.seed = options.getint(section,"seed")

		#Set of lens planes to be used during ray tracing
		settings.plane_set = options.get(section,"plane_set")

		#N-body simulation realizations that need to be mixed
		settings.mix_nbody_realizations = [ int(n) for n in options.get(section,"mix_nbody_realizations").split(",") ]
		settings.lens_catalog_realizations = options.getint(section,"lens_catalog_realizations")
		settings.mix_cut_points = [ int(n) for n in options.get(section,"mix_cut_points").split(",") ]
		settings.mix_normals = [ int(n) for n in options.get(section,"mix_normals").split(",") ]

		#Return to user
		return settings


##################################################
###############JobSettings class##################
##################################################

class JobSettings(object):

	"""
	Class handler of batch job submission settings

	"""

	def __init__(self,**kwargs):

		#Personal settings
		self.email = "apetri@phys.columbia.edu"
		self.charge_account = "TG-AST140041"

		#Path to executable
		self.path_to_executable = "Gadget2"

		#Name of the job, output
		self.job_name = "job"
		self.redirect_stdout = "job.out"
		self.redirect_stderr = "job.err"

		#Resources
		self.cores_per_simulation = 16
		self.queue = "development"
		self.wallclock_time = "02:00:00"

		#Script name
		self.job_script_file = "job.sh"

		#Allow for kwargs override
		for key in kwargs.keys():
			setattr(self,key,kwargs[key])


	@classmethod
	def read(cls,config_file,section):

		#Read the options from the ini file
		options = config.ConfigParser()
		options.read([config_file])

		#Check that the config file has the appropriate section
		assert options.has_section(section),"No {0} section in configuration file {1}".format(section,config_file)

		#Fill in the appropriate fields
		settings = cls()

		#Personal settings
		settings.email = options.get(section,"email")
		settings.charge_account = options.get(section,"charge_account")

		#Path to executable
		try:
			settings.path_to_executable = options.get(section,"path_to_executable")
		except NoOptionError:
			settings.path_to_executable = section

		#Name of the job, output
		settings.job_name = options.get(section,"job_name")
		settings.redirect_stdout = options.get(section,"redirect_stdout")
		settings.redirect_stderr = options.get(section,"redirect_stderr")

		#Resources
		
		#These do not need to be provided necessarily
		try:
			settings.num_cores = options.getint(section,"num_cores")
		except NoOptionError:
			pass

		try:
			settings.num_nodes = options.getint(section,"num_nodes")
		except NoOptionError:
			pass

		try:
			settings.tasks_per_node = options.getint(section,"tasks_per_node")
		except NoOptionError:
			pass

		#These need to be provided
		settings.cores_per_simulation = options.getint(section,"cores_per_simulation")
		settings.queue = options.get(section,"queue")
		settings.wallclock_time = options.get(section,"wallclock_time")

		#Script name
		settings.job_script_file = options.get(section,"job_script_file")

		return settings















