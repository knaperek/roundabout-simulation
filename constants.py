# import random
from numpy.random import poisson, exponential, uniform

# Car priorities for requesting slots in circles
JUNCTION_PRIORITY_INSIDE = 1
JUNCTION_PRIORITY_JOINING = 2

# Time it takes for moving by one car slot
car_speed = 40  # km/h
slot_size = 3  # meters
SLOT_PASSING_TIME = slot_size / (car_speed % 3.6)

# Roundabout size (in slots). Must be multiple of 4 (at least 8)
junction_diameter = 40  # meters
junction_circumference = junction_diameter * 3
circle_len = (junction_circumference / slot_size)
circle_len -= circle_len % 4
# put some estimates...
INNER_CIRCLE_LEN = circle_len - 4
OUTER_CIRCLE_LEN = circle_len + 4


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
		lambda: exponential(0.1),
		# West -> East
		lambda: exponential(0.4),
		# West -> North
		lambda: uniform(7, 83),
	],
	# From exit 1 to exits 2, 3, 0
	[
		# South -> East
		lambda: poisson(0.9),
		# South -> North
		lambda: exponential(0.65),
		# South -> West
		lambda: poisson(4.3),
	],
	# From exit 2 to exits 3, 0, 1
	[
		# East -> North
		lambda: poisson(1.3),
		# East -> West
		lambda: poisson(2.2),
		# East -> South
		lambda: uniform(2, 82),
	],
	# From exit 3 to exits 0, 1, 2
	[
		# North -> West
		lambda: uniform(33, 100),
		# North -> South
		lambda: poisson(1.5),
		# North -> East
		lambda: uniform(10, 71),
	],
]
