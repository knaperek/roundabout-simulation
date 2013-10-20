import random

# Car priorities for requesting slots in circles
JUNCTION_PRIORITY_INSIDE = 1
JUNCTION_PRIORITY_JOINING = 2

# Time it takes for moving by one car slot
SLOT_PASSING_TIME = 1

# Roundabout size (in slots). Must be multiple of 4 (at least 8)
INNER_CIRCLE_LEN = 24
OUTER_CIRCLE_LEN = 32

# Car generator random functions
CAR_GENERATOR_RANDOM_FUNCTIONS = [
	# From exit 0 to exits 1, 2, 3
	[
		lambda: random.expovariate(1.0 / 5),
		lambda: random.expovariate(1.0 / 5),
		lambda: random.expovariate(1.0 / 5),
	],
	# From exit 1 to exits 2, 3, 0
	[
		lambda: random.expovariate(1.0 / 5),
		lambda: random.expovariate(1.0 / 5),
		lambda: random.expovariate(1.0 / 5),
	],
	# From exit 2 to exits 3, 0, 1
	[
		lambda: random.expovariate(1.0 / 5),
		lambda: random.expovariate(1.0 / 5),
		lambda: random.expovariate(1.0 / 5),
	],
	# From exit 3 to exits 0, 1, 2
	[
		lambda: random.expovariate(1.0 / 5),
		lambda: random.expovariate(1.0 / 5),
		lambda: random.expovariate(1.0 / 5),
	],
]
