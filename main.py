#!/usr/bin/env python

import numpy
import simpy
from car import CarSource
from roundabout import RoundAbout
from constants import *


def create_car_sources(env, roundabout):
    """ Creates all 12 instances of CarSource and returns an iterator listing them. """
    for start_exit in range(4):
        for n_exit_hops in range(1, 4):
            yield CarSource(env, roundabout, start_exit, start_exit + n_exit_hops)

def main():
    env = simpy.Environment()
    roundabout = RoundAbout(
        env=env,
        inner_circle_len=INNER_CIRCLE_LEN,
        outer_circle_len=OUTER_CIRCLE_LEN
    )


    # Generate all combinations of car sources
    car_sources = list(create_car_sources(env, roundabout))

    env.run(until=10000)

    # statistics
    all_cars = []
    finished_cars = []
    unfinished_cars = []
    for source in car_sources:
        for car in source.cars:
            if car.total_time == None:
                unfinished_cars.append(car)
            else:
                finished_cars.append(car)
            all_cars.append(car)

    total_times = [car.total_time for car in finished_cars]

    print('----------------')
    print('Average time: %d' % numpy.mean(total_times))
    print('Finished cars: %d' % len(finished_cars))
    unfinished_ratio = len(unfinished_cars) * 100 / len(finished_cars)
    print('Unfinished cars: %d (%d%%)' % (len(unfinished_cars), unfinished_ratio))

    # Draw some nice charts using matplotlib
    import pylab as P
    P.xlabel('Crossing time')
    P.ylabel('Number of cars')
    P.hist(total_times)
    P.show()


if __name__ == '__main__':
    main()
