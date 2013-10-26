#!/usr/bin/env python

import collections

class Ring(object):
    """ Doubly linked list, supporting indices with overflow """

    def __init__(self, sequence):
        self._data = list(sequence)
        self._circumference = len(self._data)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return 'Ring(%s)' % repr(self._data)

    def __len__(self):
        return self._circumference

    def __getitem__(self, value):
        if type(value) == slice:  # Slicing
            # step is not supported for now
            start, stop = [i % self._circumference for i in (value.start, value.stop)]
            if start < stop:
                # normal slice
                return self._data[start:stop]
            else:
                # overflowing slice
                return self._data[start:] + self._data[:stop]

        else:  # Indexing
            return self._data[value % self._circumference]


    def __iter__(self):
        """ Returns infinite iterator, going to the circle. """
        i = 0
        while True:
            i = (i + 1) % self._circumference
            yield self[i]

        