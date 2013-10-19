import collections
import simpy
from ring import Ring


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
