# from random import uniform
from numpy.random import poisson, uniform

# Car priorities for requesting slots in circles
JUNCTION_PRIORITY_INSIDE = 1
JUNCTION_PRIORITY_JOINING = 2


SIMULATION_TIME = 24 * 3600

DEBUG = False


####################### Random functions for generating inter-arrival times ################################
# Exit map:
# 0 - West
# 1 - South
# 2 - East
# 3 - North

# Car generator random functions
CAR_GENERATOR_RANDOM_FUNCTIONS = [
	# From exit 0 to exits 1, 2, 3
	[
		# West -> South
		lambda: poisson(20.72),
		# West -> East
		lambda: poisson(8.42),
		# West -> North
		lambda: uniform(7, 83),
	],
	# From exit 1 to exits 2, 3, 0
	[
		# South -> East
		lambda: poisson(9.039),
		# South -> North
		lambda: poisson(19.208),
		# South -> West
		lambda: poisson(36.417),
	],
	# From exit 2 to exits 3, 0, 1
	[
		# East -> North
		lambda: poisson(9.125),
		# East -> West
		lambda: poisson(9.319),
		# East -> South
		lambda: uniform(2, 82),
	],
	# From exit 3 to exits 0, 1, 2
	[
		# North -> West
		lambda: uniform(33, 100),
		# North -> South
		lambda: poisson(24.11),
		# North -> East
		lambda: uniform(10, 71),
	],
]
