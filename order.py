#!/usr/bin/env python

import simpy
import random


def procA(env, r1, r2):
	""" master """
	with r1.request() as req1:
		yield req1
		print('procA (%7.4f): Beriem si r1' % env.now)
		yield env.timeout(15)
		print('procA (%7.4f): Odovzdavam r1' % env.now)

def procB(env, r1, r2):
	""" Prvy, ale chce obidva. """
	yield env.timeout(5)
	with r1.request() as req1:
		with r2.request() as req2:
			print('procB (%7.4f): Ziadam obidva!' % env.now)
			yield req1 & req2
			print('procB (%7.4f): Dostal som obidva!' % env.now)
			yield env.timeout(5)
			print('procB (%7.4f): Vraciam obidva!' % env.now)


def procC(env, r1, r2):
	""" Druhy, ale staci mu r2 """
	yield env.timeout(10)
	
	with r2.request() as req2:
		print('procC (%7.4f): Ziadam r2!' % env.now)
		yield req2
		print('procC (%7.4f): Dostal som r2!' % env.now)
		yield env.timeout(15)
		print('procC (%7.4f): Vraciam r2!' % env.now)


def main():
	env = simpy.Environment()
	r1 = simpy.Resource(env, 1)
	r2 = simpy.Resource(env, 2)
	env.process(procA(env, r1, r2))
	env.process(procB(env, r1, r2))
	env.process(procC(env, r1, r2))
	env.run(until=100)



if __name__ == '__main__':
	main()