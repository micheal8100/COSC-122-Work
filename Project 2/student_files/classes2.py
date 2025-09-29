"""
classes2.py

This module provides the NumberPlate class that is to be used in Assignment 2
"""

from stats import StatCounter, COMPS, HASHES


MIN_PLATE_SIZE = 6
CHARACTER_ERROR = 'Number plates must only contain capital letters or digits: '
ERROR_TEMPLATE = 'NumberPlates must be at least {} characters. '
PLATE_LENGTH_ERROR = ERROR_TEMPLATE.format(MIN_PLATE_SIZE)
COMPARISON_TYPE_ERROR = 'NumberPlates can only be compared to other NumberPlates. '


def _fnv32a_hash(string):
    """ A nice fast little hashing function :)
    You shouldn't use this directly.
    You should use expressions such as hash(my_number_plate)
       see the __hash__ method in the NumberPlate class.
    """
    hval = 0x811c9dc5
    fnv_32_prime = 0x01000193
    uint32_max = 2 ** 32
    for c in string:
        hval = hval ^ ord(c)
        hval = (hval * fnv_32_prime) % uint32_max
    # The result is trimmed down to 31 bits (plus a sign bit) to give
    # consistent results on 32 and 64 bit systems
    # Otherwise hash() will implicitly do this
    # based on build of Python
    # see https://docs.python.org/3/reference/datamodel.html#object.__hash__
    # & is the binary AND operation
    hval = hval & 0b1111111111111111111111111111111
    return hval


class NumberPlate(object):
    """ A simple variation on strings so actual comparisons 
    and hashes can be counted.
    """

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
            print(type(other))
            raise TypeError(COMPARISON_TYPE_ERROR)
        StatCounter.increment(COMPS)
        return self._plate == other._plate

    def __le__(self, other):
        if not isinstance(other, NumberPlate):
            raise TypeError(COMPARISON_TYPE_ERROR)
        StatCounter.increment(COMPS)
        return self._plate <= other._plate

    def __ne__(self, other):
        if not isinstance(other, NumberPlate):
            raise TypeError(COMPARISON_TYPE_ERROR)
        StatCounter.increment(COMPS)
        return self._plate != other._plate

    def __lt__(self, other):
        if not isinstance(other, NumberPlate):
            raise ValueError(COMPARISON_TYPE_ERROR)
        StatCounter.increment(COMPS)
        return self._plate < other._plate

    def __gt__(self, other):
        if not isinstance(other, NumberPlate):
            raise ValueError(COMPARISON_TYPE_ERROR)
        StatCounter.increment(COMPS)
        return self._plate > other._plate

    def __ge__(self, other):
        if not isinstance(other, NumberPlate):
            raise ValueError(COMPARISON_TYPE_ERROR)
        StatCounter.increment(COMPS)
        return self._plate >= other._plate

    def __hash__(self):
        """ hash(my_number_plate) will use this method, ie, it will 
        return the hash value for my_number_plate.
        """
        StatCounter.increment(HASHES)
        return _fnv32a_hash(self._plate)

    def __getattr__(self, attr):
        """All other behaviours use self._plate.
        You probably shouldn't be using any other methods though...
        """
        return self._plate.__getattribute__(attr)


