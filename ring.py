#!/usr/bin/env python

import collections

class Ring(object):
	# """ Doubly linked list, supporting both references and indices """
	""" Doubly linked list, supporting indices with overflow """

	def __init__(self, sequence):
		self._data = list(sequence)
		self._perimeter = len(self._data)

	def __str__(self):
		return str(self._data)

	def __repr__(self):
		return 'Ring(%s)' % repr(self._data)

	def __getitem__(self, value):
		if type(value) == slice:  # Slicing
			# step is not supported for now
			start, stop = value.start % self._perimeter, value.stop % self._perimeter
			if start <= stop:
				# normal slice
				return self._data[start:stop]
			else:
				# overflowing slice
				return self._data[start:] + self._data[:stop]

		else:  # Indexing
			return self._data[value % self._perimeter]


	def __iter__(self):
		""" Returns infinite iterator, going to the circle. """
		i = 0
		while True:
			i = (i + 1) % self._perimeter
			yield self[i]

		