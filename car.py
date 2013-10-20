import random
import simpy
from constants import *


class CarSource(object):
    """ Generates cars arriving to the crossroad. """

    def __init__(self, env, roundabout, ingress_exit, egress_exit):
        self.env = env
        self.roundabout = roundabout
        self.ingress_exit = ingress_exit % 4
        self.egress_exit = egress_exit % 4
        assert(self.ingress_exit != self.egress_exit)  # U-turn not allowed!

        # select inter-arrival-time random function
        n_exit_hops = (self.egress_exit - self.ingress_exit) % 4
        self.iat_random_func = CAR_GENERATOR_RANDOM_FUNCTIONS[self.ingress_exit][n_exit_hops-1]

        # create empty list of cars
        self.cars = []

        self.process = env.process(self.generate())

    def generate(self):
        while True:
            car = Car(self.env, self.roundabout, self.ingress_exit, self.egress_exit)
            self.cars.append(car)
            yield self.env.timeout(self.iat_random_func())
            

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

        self.start_time = None
        self.stop_time = None

        self.process = env.process(self.start())

    def start(self):
        """
        Pre-calculates the whole path the car should take and calls drive() method to follow it.

        *ingress_exit* and *egress_exit* parameters are 0-based indexes of exites (West=0, South=1, ...)
        """
        self.log('starting...')

        if self.n_exit_hops > 2:
            # use inner circle
            first_outer_slot = self.roundabout.outer_exits_indices[self.ingress_exit][0]
            first_inner_slot = self.roundabout.inner_exits_indices[self.ingress_exit][0]
            last_inner_slot = self.roundabout.inner_exits_indices[self.egress_exit][0]
            last_outer_slot = self.roundabout.outer_exits_indices[self.egress_exit][0]

            # first slot (on outer circle) used just to get into the inner circle
            join_resource = self.roundabout.outer_circle[first_outer_slot]

            # all inner slots (resources)
            resources_path = list(self.roundabout.inner_circle[first_inner_slot+1:last_inner_slot])
            # compound resource containing first slots for both inner and outer circle
            resources_path.insert(0, [
                self.roundabout.outer_circle[first_outer_slot],
                self.roundabout.inner_circle[first_inner_slot]
            ])
            # cross outer circle when exiting the roundabout
            resources_path.append(self.roundabout.outer_circle[last_outer_slot])

        else:
            # use outer circle
            # convert 0-3 exit index to 0-X slot index
            first_slot = self.roundabout.outer_exits_indices[self.ingress_exit][1]
            last_slot = self.roundabout.outer_exits_indices[self.egress_exit][0]  # actually, it is not used - it's the < boundary
            resources_path = list(self.roundabout.outer_circle[first_slot:last_slot])

        return self.drive(resources_path)


    def drive(self, resource_path):
        """ Follows the precalculated path, spending some time while passing each slot. """
        self.log('is driving...')

        self.start_time = self.env.now
        for i, step in enumerate(resource_path):
            # low priority for first iteration
            if i == 0:
                self.log('joining the roundabout')
                priority = JUNCTION_PRIORITY_JOINING
            else:
                priority = JUNCTION_PRIORITY_INSIDE

            self.log('requesting %d-th slot' % (i+1))

            if isinstance(step, list) or isinstance(step, tuple):  # two resources
                self.log('requesting compound resource')
                
                # resources = step
                requests = [res.request(priority=priority) for res in step]
                yield simpy.events.AllOf(self.env, requests)
                self.log('acquired %d-th slot (Compound) and waiting...' % (i+1))
                yield self.env.timeout(SLOT_PASSING_TIME )
                self.log('releasing %d-th slot (Compound)' % (i+1))
                for request in requests:
                    request.resource.release(request)
            else:  # single resource
                with step.request(priority=priority) as req:
                    yield req
                    self.log('acquired %d-th slot and waiting...' % (i+1))
                    yield self.env.timeout(SLOT_PASSING_TIME )
                    self.log('releasing %d-th slot' % (i+1))

        # end of the path
        self.stop_time = self.env.now

    @property
    def total_time(self):
        if self.stop_time == None:
            # simulation ended before the car could finish the crossing
            return self.stop_time
        return self.stop_time - self.start_time

    def log(self, message):
        prefix = '(%7.4f) Car #%s: ' % (self.env.now, self.id)
        text = prefix + message
        # print(text)
