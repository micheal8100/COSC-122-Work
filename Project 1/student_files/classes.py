"""
classes.py
COSC122 Assignment 1

This module provides the NumberPlate class that is to be used in Assignment 1.
"""

from stats import StatCounter


MIN_PLATE_SIZE = 6
CHARACTER_ERROR = 'Number plates must only contain capital letters or digits: '
ERROR_TEMPLATE = 'NumberPlates must be at least {} characters. '
PLATE_LENGTH_ERROR = ERROR_TEMPLATE.format(MIN_PLATE_SIZE)
COMPARISON_TYPE_ERROR = 'NumberPlates can only be compared to other NumberPlates. '


class NumberPlate(object):
    """ A simple variation on strings so actual comparisons can be counted."""

    def __init__(self, plate):
        """ plate should be a string containing only uppercase letter and digits.
        It should have at least MIN_PLATE_SIZE characters 
        """
        if not all(('A' <= c <= 'Z') or ('0' <= c <= '9') for c in plate):
            raise ValueError(CHARACTER_ERROR + ' ' + plate)
        if len(plate) < MIN_PLATE_SIZE:
            raise ValueError(PLATE_LENGTH_ERROR)
        self._plate = plate

    def __repr__(self):
        return repr(self._plate)

    def __str__(self):
        return str(self._plate)

    def __eq__(self, other):
        if not isinstance(other, NumberPlate):
            raise TypeError(COMPARISON_TYPE_ERROR)
        StatCounter.increment()
        return self._plate == other._plate

    def __le__(self, other):
        if not isinstance(other, NumberPlate):
            raise TypeError(COMPARISON_TYPE_ERROR)
        StatCounter.increment()
        return self._plate <= other._plate

    def __ne__(self, other):
        if not isinstance(other, NumberPlate):
            raise TypeError(COMPARISON_TYPE_ERROR)
        StatCounter.increment()
        return self._plate != other._plate

    def __lt__(self, other):
        if not isinstance(other, NumberPlate):
            raise ValueError(COMPARISON_TYPE_ERROR)
        StatCounter.increment()
        return self._plate < other._plate

    def __gt__(self, other):
        if not isinstance(other, NumberPlate):
            raise ValueError(COMPARISON_TYPE_ERROR)
        StatCounter.increment()
        return self._plate > other._plate

    def __ge__(self, other):
        if not isinstance(other, NumberPlate):
            raise ValueError(COMPARISON_TYPE_ERROR)
        StatCounter.increment()
        return self._plate >= other._plate

    def __hash__(self):
        value = ord(self._plate[0]) << 7
        for char in self._plate:
            value = self.__c_mul(1000003, value) ^ ord(char)
        value = value ^ len(self._plate)
        if value == -1:
            value = -2
        return value

    def __c_mul(self, a, b):
        return ((int(a) * int(b)) & 0xFFFFFFFF)

    def __getattr__(self, attr):
        '''All other behaviours use self._plate'''
        return self._plate.__getattribute__(attr)


