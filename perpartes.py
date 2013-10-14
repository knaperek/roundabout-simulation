#!/usr/bin/env python

import collections
import random

import simpy


class CarSource(object):
	""" Generates cars arriving to the crossroad. """
	def __init__(self, env, roundabout):
		self.env = env
		self.roundabout = roundabout
		self.process = env.process(self.generate(meanIAT=5))

	def generate(self, meanIAT):
		while True:
			# print('Car arriving')
			car = Car(self.env, self.roundabout)
			iat = random.expovariate(1.0 / meanIAT)
			yield self.env.timeout(iat)

class Car(object):
	"""
	Car process.

	Car will get (as arguments):
	- reference to INPUT EXIT
	- reference to OUTPUT EXIT
	- which circle should the car use

	Maybe split into 2 functions:
	- The first one will only generate a list of ResourceEvents to request/wait for
	- and the second one will do it

	"""
	# Number of instances
	counter = 0

	def __init__(self, env, roundabout):
		self.env = env
		self.roundabout = roundabout
		self.id = Car.counter
		Car.counter += 1
		self.process = env.process(self.drive())

	# def start(self, first_slot, last_slot, circle):
	def start(self, ingress_exit, egress_exit, circle):
		"""
		Pre-calculates the whole path the car should take and calls drive() method to follow it.

		*ingress_exit* and *egress_exit* parameters are 0-based indexes of exites (West=0, South=1, ...)
		"""
		print('(%7.4f) Car #%s starting...' % (env.now, self.id))
		# TODO
		return self.drive()

	def drive(self, event_path):
		""" Follows the precalculated path, spending some time while passing each slot. """
		print('(%7.4f) Car #%s is driving...' % (env.now, self.id))
		for i, event in enumerate(event_path):
			with event as req:
				print('(%7.4f) Car #%s requesting %d-th slot' % (env.now, self.id, i+1))
				yield req
				print('(%7.4f) Car #%s acquired %d-th slot and waiting...' % (env.now, self.id, i+1))
				yield self.env.timeout(2)  # Time to move from one slot to the next
				print('(%7.4f) Car #%s releasing %d-th slot' % (env.now, self.id, i+1))
		

class RoundAbout(object):
	""" Container for all roundabout resources. """

	Exits = collections.namedtuple('Exits', ['West', 'South', 'East', 'North'])

	def __init__(self, env, inner_circle_len, outer_circle_len):
		# Test circle lengths
		for circle_len in (inner_circle_len, outer_circle_len):
			assert(circle_len >= 8)
			assert(circle_len % 4 == 0)

		self.env = env

		# Generate circles of Resources
		self.inner_circle = [simpy.resources.resource.PriorityResource(env, capacity=1) for i in range(inner_circle_len)]
		self.outer_circle = [simpy.resources.resource.PriorityResource(env, capacity=1) for i in range(outer_circle_len)]

		# Create indices of exit slots (exit pointers)
		self.inner_exits_indices = Exits(*calculate_exit_indexes(len(self.inner_circle)))
		self.outer_exits_indices = Exits(*calculate_exit_indexes(len(self.outer_circle)))


	@staticmethod
	def calculate_exit_indexes(circle_len):
		"""
		Helper function that returns 2-tuples of indexes of 4 exits.

		We start from the West.
		"""
		quarter = circle_len // 4
		return [
			(i_exit * quarter - 1 + circle_len) % circle_len, i_exit * quarter for i_exit in range(4)
		]




def main():
	INNER_CIRCLE_LEN = 16
	OUTER_CIRCLE_LEN = 24
	env = simpy.Environment()
	roundabout = RoundAbout(
		env=env,
		inner_circle_len=INNER_CIRCLE_LEN,
		outer_circle_len=OUTER_CIRCLE_LEN
	)
	car_generator = CarSource(env)

	env.run(until=1000)


if __name__ == '__main__':
	main()