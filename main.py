#!/usr/bin/env python

import numpy
import simpy
import pylab as P

from car import CarSource
from roundabout import RoundAbout
from constants import *


def create_car_sources(env, roundabout, slot_passing_time):
    """ Creates all 12 instances of CarSource and returns an iterator listing them. """
    for start_exit in range(4):
        for n_exit_hops in range(1, 4):
            yield CarSource(env, roundabout, start_exit, start_exit + n_exit_hops, slot_passing_time)

def run_simulation(roundabout_diameter, slot_size, car_speed):
    """
    * roundabout_diameter - in meters
    * slot_size - in meters
    * car_speed - in km/h
    """

    ######## Parameters caluculation

    # Time it takes for moving by one car slot
    SLOT_PASSING_TIME = slot_size / (car_speed / 3.6)

    def _quantize(value):
        return int(round(value - value % 4))

    INNER_CIRCLE_LEN = _quantize((roundabout_diameter - 4) * 3.14 / slot_size)
    OUTER_CIRCLE_LEN = _quantize((roundabout_diameter + 4) * 3.14 / slot_size)

    #############

    print('-------Running simulation with these constants:-----------')
    print('SLOT_PASSING_TIME: {}'.format(SLOT_PASSING_TIME))
    print('INNER_CIRCLE_LEN: {}'.format(INNER_CIRCLE_LEN))
    print('OUTER_CIRCLE_LEN: {}'.format(OUTER_CIRCLE_LEN))
    print('SIMULATION_TIME: {}'.format(SIMULATION_TIME))



    env = simpy.Environment()
    roundabout = RoundAbout(
        env=env,
        inner_circle_len=INNER_CIRCLE_LEN,
        outer_circle_len=OUTER_CIRCLE_LEN
    )

    # Generate all combinations of car sources
    car_sources = list(create_car_sources(env, roundabout, SLOT_PASSING_TIME))

    env.run(until=SIMULATION_TIME)

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

    print('-' * 80)
    print('Average time: %.2f' % numpy.mean(total_times))
    print('Maximum time: %.2f' % max(total_times))
    print('Finished cars: %d' % len(finished_cars))
    unfinished_ratio = len(unfinished_cars) * 100 / len(finished_cars)
    print('Unfinished cars: %d (%d%%)' % (len(unfinished_cars), unfinished_ratio))

    # Draw some nice charts using matplotlib
    P.xlabel('Crossing time')
    P.ylabel('Number of cars')
    P.title('Average: %.2f   Maximum: %.2f' % (numpy.mean(total_times), max(total_times)))
    P.hist(total_times, log=True)
    P.savefig('figures/{}_{}_{}.png'.format(roundabout_diameter, slot_size, car_speed))
    # P.show()
    P.close()


def main():
    """ Run the simulation for all combinations of some reasonable parameters. """

    for roundabout_diameter in [30, 35, 40]:
        for slot_size in [4, 5]:
            for car_speed in [20, 25, 30, 35, 40]:
                run_simulation(roundabout_diameter, slot_size, car_speed)

if __name__ == '__main__':
    main()
