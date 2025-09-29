""" Used to help you check your comparisons count matches the actual number
of comparisons done 

IMPORTANT - You shouldn't refer to __n_comparisons__ or get_comparisons in 
the answer you submit to the quiz server. They won't be available!
"""


# Set marking mode to False for testing
# NOTE: it will be set to True on the quiz server!
IS_MARKING_MODE = False
ERROR = "You can't use the stats in marking mode!"

COMPS = 'comparisons'
HASHES = 'hashes'


class StatCounter:
    """ Used to help you check your comparison count 
    You shouldn't use this in your answer code as it won't work!
    """

    if not IS_MARKING_MODE:
        _stats = {COMPS: 0, HASHES: 0}
    else:
        _stats = {COMPS: ERROR, HASHES: ERROR}

    def __init__(self, *args, **kwargs):
        raise TypeError("The StatCounter class should never be initialized!")

    @classmethod
    def increment(cls, counter):
        if not IS_MARKING_MODE:
            cls._stats[counter] += 1
        else:
            cls._stats[counter] = ERROR

    @classmethod
    def get_count(cls, counter):
        if not IS_MARKING_MODE:
            return cls._stats[counter]
        else:
            # you shouldn't be using this in your final code!
            raise ValueError(ERROR)

    @classmethod
    def reset_counts(cls):
        if not IS_MARKING_MODE:
            cls._stats = {COMPS: 0, HASHES: 0}
        else:
            cls._stats = {COMPS: ERROR, HASHES: ERROR}

    @classmethod
    def reset_count(cls, counter):
        """ Resets the count for just the given counter """
        if not IS_MARKING_MODE:
            cls._stats[counter] = 0
        else:
            # you shouldn't be using this in your final code!
            cls._stats[counter] = ERROR

