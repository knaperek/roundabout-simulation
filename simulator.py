#!/usr/bin/env python

import simpy
import random

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
	""" Car process. """
	# Number of instances
	counter = 0

	def __init__(self, env):
		self.env = env
		self.process = env.process(self.drive())
		self.id = Car.counter
		Car.counter += 1

	def drive(self):
		print('Car #%s is driving...' % self.id)
		yield self.env.timeout(1)
		
class LaneResource(simpy.resources.resource.PriorityResource):
	""" Quater of circle in the roundabout. """

	def __init__(self, *args, **kwargs):
		ret = super(LaneResource, self).__init__(*args, **kwargs)
		# initialize references to resources around
		self.previous = None
		self.next = None
		return ret

	def enter_circle(self):
		""" For cars entering the roundabout. They have lower priority. """
		# TODO: implement checking previous LaneResource()
		# with self.request(priority=0, preempt=False) as event:
		# 	yield event
		# 	# 
		return self.request(priority=0, preempt=False)

	def continue_driving(self):
		""" For cars that are already in the roundabout, finishing one quarter and starting another one. They have higher priority. """
		return self.request(priority=1, preempt=False)
		

def main():
	env = simpy.Environment()
	generator = CarSource(env)
	env.run(until=100)



if __name__ == '__main__':
	main()