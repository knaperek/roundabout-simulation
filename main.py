#!/usr/bin/env python

import simpy
from car import CarSource
from roundabout import RoundAbout


def main():
    INNER_CIRCLE_LEN = 16
    OUTER_CIRCLE_LEN = 24
    env = simpy.Environment()
    roundabout = RoundAbout(
        env=env,
        inner_circle_len=INNER_CIRCLE_LEN,
        outer_circle_len=OUTER_CIRCLE_LEN
    )

    # car_generator_1 = CarSource(env, roundabout, 0, 1)
    # car_generator_2 = CarSource(env, roundabout, 0, 2)
    # car_generator_3 = CarSource(env, roundabout, 0, 3)

    # Generate all combinations of car sources
    car_sources = []
    for start_exit in range(4):
        for n_exit_hops in range(1, 4):
            source = CarSource(env, roundabout, start_exit, start_exit + n_exit_hops)
            car_sources.append(source)

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
    import numpy
    print('Average time: %d' % numpy.mean(total_times))
    print('Finished cars: %d' % len(finished_cars))
    unfinished_ratio = len(unfinished_cars) * 100 / len(finished_cars)
    print('Unfinished cars: %d (%d%%)' % (len(unfinished_cars), unfinished_ratio))



if __name__ == '__main__':
    main()


# #########################################
# TODO: pohrat sa s parametrami a pravidlami:
# - skusit to zmenit tak, aby auto vchadzajuce na roundabout mali prioritu pred tymi co su tam - malo by to vyjst horsie :-)
#