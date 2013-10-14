#!/usr/bin/env python

import collections
import random

import simpy

from ring import Ring


class CarSource(object):
    """ Generates cars arriving to the crossroad. """
    # TODO: add random function as another argument
    def __init__(self, env, roundabout, ingress_exit, egress_exit):
        self.env = env
        self.roundabout = roundabout
        self.ingress_exit = ingress_exit
        self.egress_exit = egress_exit
        self.process = env.process(self.generate(meanIAT=5))

    def generate(self, meanIAT):
        while True:
            # print('Car arriving')
            car = Car(self.env, self.roundabout, self.ingress_exit, self.egress_exit)
            iat = random.expovariate(1.0 / meanIAT)
            yield self.env.timeout(iat)

class Car(object):
    """
    Car process.

    Split into 2 functions:
    - The first one only generates a list of ResourceEvents to request/wait for
    - and the second one does the "driving"
    """

    counter = 0  # Number of instances

    def __init__(self, env, roundabout, ingress_exit, egress_exit):
        self.env = env
        self.roundabout = roundabout
        self.ingress_exit = ingress_exit
        self.egress_exit = egress_exit
        self.n_exit_hops = (egress_exit - ingress_exit) % 4
        assert(0 < self.n_exit_hops < 4)  # U-turn is not allowed

        self.id = Car.counter
        Car.counter += 1

        self.process = env.process(self.start())

    def start(self):
        """
        Pre-calculates the whole path the car should take and calls drive() method to follow it.

        *ingress_exit* and *egress_exit* parameters are 0-based indexes of exites (West=0, South=1, ...)
        """
        print('(%7.4f) Car #%s starting...' % (self.env.now, self.id))

        if self.n_exit_hops > 2:
            # use inner circle
            raise NotImplementedError('Inner circle is not yet implemented!')
        else:
            # use outer circle
            # convert 0-3 exit index to 0-X slot index
            first_slot = self.roundabout.outer_exits_indices[self.ingress_exit][1]
            last_slot = self.roundabout.outer_exits_indices[self.egress_exit][0]  # actually, it is not used - it's the < boundary

            # event_path = [res.request(priority=1) for res in self.roundabout.outer_circle[first_slot:last_slot]]
            resources_path = list(self.roundabout.outer_circle[first_slot:last_slot])
            event_path = [resources_path[0].request(priority=2)] + [res.request(priority=1) for res in resources_path[1:]]

        return self.drive(event_path)

    def drive(self, event_path):
        """ Follows the precalculated path, spending some time while passing each slot. """
        print('(%7.4f) Car #%s is driving...' % (self.env.now, self.id))
        for i, event in enumerate(event_path):
            with event as req:
                print('(%7.4f) Car #%s requesting %d-th slot' % (self.env.now, self.id, i+1))
                yield req
                print('(%7.4f) Car #%s acquired %d-th slot and waiting...' % (self.env.now, self.id, i+1))
                yield self.env.timeout(2)  # Time to move from one slot to the next
                print('(%7.4f) Car #%s releasing %d-th slot' % (self.env.now, self.id, i+1))
        

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
        self.inner_circle = Ring(
            [simpy.resources.resource.PriorityResource(env, capacity=1) for i in range(inner_circle_len)]
        )
        self.outer_circle = Ring(
            [simpy.resources.resource.PriorityResource(env, capacity=1) for i in range(outer_circle_len)]
        )

        # Create indices of exit slots (exit pointers)
        self.inner_exits_indices = RoundAbout.Exits(*RoundAbout.calculate_exit_indices(len(self.inner_circle)))
        self.outer_exits_indices = RoundAbout.Exits(*RoundAbout.calculate_exit_indices(len(self.outer_circle)))


    @staticmethod
    def calculate_exit_indices(circle_len):
        """
        Helper function that returns 2-tuples of indexes of 4 exits.

        We start from the West.
        """
        quarter = circle_len // 4
        return [((i_exit * quarter - 1) % circle_len, i_exit * quarter) for i_exit in range(4)]



def main():
    INNER_CIRCLE_LEN = 16
    OUTER_CIRCLE_LEN = 24
    env = simpy.Environment()
    roundabout = RoundAbout(
        env=env,
        inner_circle_len=INNER_CIRCLE_LEN,
        outer_circle_len=OUTER_CIRCLE_LEN
    )
    car_generator = CarSource(env, roundabout, 0, 1)

    env.run(until=1000)


if __name__ == '__main__':
    main()


# #########################################
# TODO: pohrat sa s parametrami a pravidlami:
# - skusit to zmenit tak, aby auto vchadzajuce na roundabout mali prioritu pred tymi co su tam - malo by to vyjst horsie :-)
#