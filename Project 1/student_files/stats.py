""" Used to help you check your comparisons count matches the actual number
of comparisons done 

IMPORTANT - You shouldn't refer to __n_comparisons__ or get_comparisons in 
the answer you submit to the quiz server. They won't be available!
"""


# Set marking mode to False for testing
# NOTE: it will be set to True on the quiz server!
IS_MARKING_MODE = False

class StatCounter:
    """ Used to help you check your comparison count 
    You shouldn't use this in your answer code as it won't work!
    """

    if not IS_MARKING_MODE:
        __n_comparisons__ = 0
    else:
        __n_comparisons__ = "You can't use __n_comparisons__ in marking mode!"

    def __init__(self, *args, **kwargs):
        raise TypeError("The StatCounter class should never be initialized!")

    @classmethod
    def increment(cls):
        if not IS_MARKING_MODE:
            cls.__n_comparisons__ += 1
        else:
            cls.__n_comparisons__ = "You can't use __n_comparisons__ in marking mode!"

    @classmethod
    def get_comparisons(cls):
        if not IS_MARKING_MODE:
            return cls.__n_comparisons__
        else:
            # you shouldn't be using this in your final code!
            raise ValueError(
                "You can't use .get_comparisons() in marking mode!")

    @classmethod
    def reset_comparisons(cls):
        if not IS_MARKING_MODE:
            cls.__n_comparisons__ = 0
        else:
            cls.__n_comparisons__ = "You can't use __n_comparisons__ in marking mode!"

