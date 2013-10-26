import collections
import simpy
from ring import Ring
from constants import *


class RoundAbout(object):
    """ Container for all roundabout resources. """

    Exits = collections.namedtuple('Exits', ['West', 'South', 'East', 'North'])
    Sides = collections.namedtuple('Sides', ['left', 'right'])  # left/right lane - when joining the junction (left goes to the inner circle, right to the outer)

    def __init__(self, env, inner_circle_len, outer_circle_len):
        # Test circle lengths
        for circle_len in (inner_circle_len, outer_circle_len):
            assert circle_len >= 16, 'Circle lenght has to be at least 16'
            assert circle_len % 4 == 0, 'Circle lenght must be divisible by 4'

        self.env = env

        # Generate circles of Resources
        self.inner_circle = Ring(
            [simpy.resources.resource.PriorityResource(env, capacity=1) for i in range(inner_circle_len)]
        )
        self.outer_circle = Ring(
            [simpy.resources.resource.PriorityResource(env, capacity=1) for i in range(outer_circle_len)]
        )

        # Create indices of exit slots (exit pointers)
        self.inner_exits_indices = RoundAbout.Exits(*RoundAbout.calculate_exit_indices(inner_circle_len))
        self.outer_exits_indices = RoundAbout.Exits(*RoundAbout.calculate_exit_indices(outer_circle_len))


    @staticmethod
    def calculate_exit_indices(circle_len):
        """
        Helper function that returns 2-tuples of indexes of 4 exits.

        We start from the West.
        """
        quarter = circle_len // 4
        return [RoundAbout.Sides(
            (i_exit * quarter - 1) % circle_len, i_exit * quarter
        ) for i_exit in range(4)]

