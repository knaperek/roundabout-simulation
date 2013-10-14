#!/usr/bin/env python

import collections
import random

import simpy


class CarSource(object):
	""" Generates cars arriving to the crossroad. """
	def __init__(self, env):
		self.env = env
		self.process = env.process(self.generate(meanIAT=5))

	def generate(self, meanIAT):
		while True:
			# print('Car arriving')
			car = Car(self.env)
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

	def __init__(self, env):
		self.env = env
		self.process = env.process(self.drive())
		self.id = Car.counter
		Car.counter += 1

	def start(self, first_slot, last_slot, circle):
		""" Pre-calculates the whole path the car should take and calls drive() method to follow it. """
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

	def __init__(self, env, inner_circle_len, outer_circle_len):
		assert(inner_circle_len % 4 == 0)
		assert(outer_circle_len % 4 == 0)

		self.env = env

		self.inner_circle = [simpy.resources.resource.PriorityResource(env, capacity=1) for i in range(inner_circle_len)]
		self.outer_circle = [simpy.resources.resource.PriorityResource(env, capacity=1) for i in range(outer_circle_len)]

		# we start from the West
		# self.exits = 








