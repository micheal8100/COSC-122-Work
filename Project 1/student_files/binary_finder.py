""" Your docstring should go here
Along with your name and email address
"""

import classes




def binary_stolen_plate_finder(stolen_plates, sighted_plates):
    """ Takes two lists of NumberPlates, returns a list and an integer.
    You can assume the stolen list will be in ascending order.
    You must assume that the sighted list is unsorted.

    The returned list contains stolen number plates that were sighted,
    in the same order as they appeared in the sighted list.
    The integer is the number of NumberPlate comparisons that
    were made.

    You can assume that each input list contains only unique plates,
    ie, neither list will contain more than one copy of any given plate.
    This fact will be very helpful in some special cases - you should
    think about when you can stop searching.    

    Note: you shouldn't alter either of the provided lists and you
    shouldn't make copies of either provided list. 
    """
    result_list = []
    total_comparisons = 0
    # ---start student section---
    for plate in sighted_plates:
        low = 0
        high = len(stolen_plates) - 1
        
        while low < high:
            mid = (low + high) // 2
            total_comparisons += 1
            if stolen_plates[mid] < plate:
                low = mid + 1
            else:
                high = mid
        
        total_comparisons += 1
        if low < len(stolen_plates) and stolen_plates[low] == plate:
            result_list.append(plate)
    # ===end student section===
    return result_list, total_comparisons


# ------------------------------------------------
# Extra stuff for your personal testing regime
# You can leave this stuff out of your submission


def run_tests():
    """ Use this function to run some simple tests 
    to help with developing your awesome answer code.
    You should leave this out of your submission """
    from linear_finder import linear_stolen_plate_finder
    sighted_plates = [5]
    stolen_plates = []
    print(binary_stolen_plate_finder(stolen_plates, sighted_plates))



if __name__ == '__main__':
    # This won't run when your module is imported from.
    # Use run_tests to try out some of your own simple tests.

    run_tests()
