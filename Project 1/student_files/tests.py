"""
tests.py
A module of unit tests to verify your answers
Don't be too worried if you can't understand how they work.
You should be able to understand the output though...
We recommend starting testing yourself with small lists of values
so that you can work out the expected result list and expected number
of comparisons by hand.

These unit tests aren't going to be that useful for debugging!
"""

import os
import shutil
from stats import IS_MARKING_MODE
import signal
import unittest
import math
import time
import utilities

from classes import NumberPlate
from stats import StatCounter
from linear_finder import linear_stolen_plate_finder
from binary_finder import binary_stolen_plate_finder

TEST_FOLDER = './test_data/'
TEST_FILE_TEMPLATE = '{n_stolen}-{n_sighted}-{n_matches}-{seed}.txt'

DEF_SEED = 'a'  # default seed

real_comparisons = StatCounter.get_comparisons


class TypeAssertion(object):

    def assertTypesEqual(self, a, b):
        if type(a) != type(b):
            template = "Type {} does not match type {}"
            error_msg = template.format(type(a), type(b))
            raise AssertionError(error_msg)


class BaseTestMethods(unittest.TestCase, TypeAssertion):

    def get_bounds(self, left_length, right_length):
        raise NotImplementedError("This method should be "
                                  "implemented by a subclass.")

    def use_sorted_stolen(self):
        """ The binary test subclass will over write this method
        with one that returns True so that the stolen list
        is sorted before the test is run """
        return False

    def base_filename(self, n_stolen, n_sighted, n_matches, seed=DEF_SEED):
        if self.use_sorted_stolen():
            n_stolen = str(n_stolen) + 's'
        return TEST_FILE_TEMPLATE.format(n_stolen=n_stolen,
                                         n_sighted=n_sighted,
                                         n_matches=n_matches,
                                         seed=seed)

    def check_comparisons_within_bounds(self, student_count, n_stolen, n_sighted, n_matches):
        lower, upper = self.get_bounds(n_stolen, n_sighted, n_matches)
        if not lower <= student_count <= upper:
            message = f"Your code reported using {student_count} NumberPlate comparisons "
            message += f"but was expected to use between {lower} - {upper} comparisons."
            #template = "{} is not in range {}-{}"
            #error = template.format(student_count, lower, upper)
            raise AssertionError(message)
        # else everything is fine so do nothing

    def plates_test(self, n_stolen, n_sighted, n_matches, seed=DEF_SEED):
        """ Test that the given matching_function returns the correct
            result for the file specified by test_file_name.
        """
        base_file = self.base_filename(n_stolen, n_sighted, n_matches, seed)
        stolen, sightings, expected_list = utilities.read_dataset(
            TEST_FOLDER + base_file)

        start = time.perf_counter()
        student_answer, comps = self.matching_function(stolen, sightings)
        end = time.perf_counter()
        delta = end - start
        print('{}, c={}, {:.8f}s'.format(base_file, comps, delta), end=' ... ')

        self.assertEqual(student_answer, expected_list)
        if len(student_answer) > 0:
            self.assertTypesEqual(student_answer[0], expected_list[0])

    def comparisons_test(self, n_stolen, n_sighted, n_matches,
                         expected=None, seed=DEF_SEED):
        """ Test that the number of comparisons that the student made is
            within the expected bounds (provided by self.get_bounds, or expected)
        """
        base_file = self.base_filename(n_stolen, n_sighted, n_matches, seed)
        stolen, sighted, _ = utilities.read_dataset(TEST_FOLDER + base_file)

        start = time.perf_counter()
        _, student_count = self.matching_function(stolen, sighted)
        end = time.perf_counter()
        delta = end - start
        print('{}, c={}, {:.8f}s'.format(
            base_file, student_count, delta), end=' ... ')

        if expected is not None:
            message = f"Your code reported using {student_count} NumberPlate comparisons "
            message += f"but was expected to use {expected}."
            self.assertEqual(student_count, expected, msg=message)
        else:
            self.check_comparisons_within_bounds(student_count,
                                                 len(stolen),
                                                 len(sighted),
                                                 n_matches)

    def internal_comparisons_test(self,
                                  n_stolen,
                                  n_sighted,
                                  n_matches,
                                  quiet=False,
                                  seed=DEF_SEED):
        """ Test that the student has correctly counted the code against what
            we have counted. This does not mean that the count is correct, just
            that it was correctly counted.
            setting quiet = True means the feedback summary won't be printed,
            which is useful if using along with standard comparisons in
            a single test case.
        """
        base_file = self.base_filename(n_stolen, n_sighted, n_matches, seed)
        (stolen, sighted, _) = utilities.read_dataset(TEST_FOLDER + base_file)

        start = time.perf_counter()
        _, student_count = self.matching_function(stolen, sighted)
        end = time.perf_counter()
        delta = end - start

        # prints student comparisons and time taken
        template = '{}, c={}, {:.8f}s'
        feedback = template.format(base_file, student_count, delta)
        if not quiet:
            print(feedback, end=' ... ')
        actual_comparisons = real_comparisons()
        message = f"Your code reported using {student_count} NumberPlate comparisons "
        message += f"but it actually used {actual_comparisons}."
        message += "This means you are miscounting NumberPlate comparisons, eg, "
        message += "not counting NumberPlate comparisons when they are made or "
        message += "counting NumberPlate comparisons that weren't made."
        self.assertEqual(student_count, actual_comparisons, msg=message)


class BaseTester(BaseTestMethods):

    def setUp(self):
        """Runs before every test case"""
        StatCounter.reset_comparisons()
        self.start_time = time.perf_counter()
        # self.function_to_test should be setup by subclasses with the student function
        # that they want to test

    def tearDown(self):
        self.end_time = time.perf_counter()
        test_time = (self.end_time - self.start_time)
        print(f'{test_time:.4f}s', end=' ')



class TinyTests(BaseTester):

    #== Tests with a trivially tiny dataset ==#
    def test_010_tiny(self):
        n_stolen, n_sighted, n_matches = 2, 5, 1
        self.plates_test(n_stolen, n_sighted, n_matches)

    def test_020_tiny_comps(self):
        n_stolen, n_sighted, n_matches = 2, 5, 1
        self.comparisons_test(n_stolen, n_sighted, n_matches)

    def test_030_tiny_internal_comps(self):
        n_stolen, n_sighted, n_matches = 2, 5, 1
        self.internal_comparisons_test(n_stolen, n_sighted, n_matches)


class SmallTests(BaseTester):

    def test_010_small_no_common(self):
        n_stolen, n_sighted, n_matches = 10, 5, 0
        self.plates_test(n_stolen, n_sighted, n_matches)

    def test_020_small_no_common_comps(self):
        n_stolen, n_sighted, n_matches = 10, 5, 0
        self.comparisons_test(n_stolen, n_sighted, n_matches)

    def test_030_small_no_common_internal_comps(self):
        n_stolen, n_sighted, n_matches = 10, 5, 0
        self.internal_comparisons_test(n_stolen, n_sighted, n_matches)

    def test_small_some_common(self):
        n_stolen, n_sighted, n_matches = 5, 10, 2
        self.plates_test(n_stolen, n_sighted, n_matches)

    def test_small_some_common_comparisons(self):
        n_stolen, n_sighted, n_matches = 5, 10, 2
        self.comparisons_test(n_stolen, n_sighted, n_matches)

    def test_small_some_common_internal_comparisons(self):
        n_stolen, n_sighted, n_matches = 5, 10, 2
        self.internal_comparisons_test(n_stolen, n_sighted, n_matches)

    def test_small_all_common(self):
        n_stolen, n_sighted, n_matches = 5, 10, 5
        self.plates_test(n_stolen, n_sighted, n_matches)

    def test_small_all_common_comparisons(self):
        n_stolen, n_sighted, n_matches = 5, 10, 5
        self.comparisons_test(n_stolen, n_sighted, n_matches)

    def test_small_all_common_internal_comparisons(self):
        n_stolen, n_sighted, n_matches = 5, 10, 5
        self.internal_comparisons_test(n_stolen, n_sighted, n_matches)


class MediumTests(BaseTester):

    def test_medium_some_common(self):
        n_stolen, n_sighted, n_matches = 100, 1000, 10
        self.plates_test(n_stolen, n_sighted, n_matches)

    def test_medium_some_common_comparisons(self):
        n_stolen, n_sighted, n_matches = 100, 1000, 10
        self.comparisons_test(n_stolen, n_sighted, n_matches)

    def test_medium_some_common_internal_comparisons(self):
        n_stolen, n_sighted, n_matches = 100, 1000, 10
        self.internal_comparisons_test(n_stolen, n_sighted, n_matches)

    def test_medium_all_common(self):
        n_stolen, n_sighted, n_matches = 100, 1000, 100
        self.plates_test(n_stolen, n_sighted, n_matches)

    def test_medium_all_common_comparisons(self):
        n_stolen, n_sighted, n_matches = 100, 1000, 100
        self.comparisons_test(n_stolen, n_sighted, n_matches)

    def test_medium_all_common_internal_comparisons(self):
        n_stolen, n_sighted, n_matches = 100, 1000, 100
        self.internal_comparisons_test(n_stolen, n_sighted, n_matches)




class LargeTestsV1(BaseTester):

    def test_010_large_no_common(self):
        n_stolen, n_sighted, n_matches = 1000, 1000, 0
        self.plates_test(n_stolen, n_sighted, n_matches)

    def test_020_large_no_common_comparisons(self):
        n_stolen, n_sighted, n_matches = 1000, 1000, 0
        self.comparisons_test(n_stolen, n_sighted, n_matches)

    def test_030_large_no_common_internal_comparisons(self):
        n_stolen, n_sighted, n_matches = 1000, 20000, 0
        self.internal_comparisons_test(n_stolen, n_sighted, n_matches)


class LargeTestsV2(BaseTester):

    def test_large_some_common(self):
        n_stolen, n_sighted, n_matches = 100, 1000, 100
        self.plates_test(n_stolen, n_sighted, n_matches)

    def test_large_some_common_comparisons(self):
        n_stolen, n_sighted, n_matches = 100, 1000, 100
        self.comparisons_test(n_stolen, n_sighted, n_matches)

    def test_large_some_common_internal_comparisons(self):
        n_stolen, n_sighted, n_matches = 100, 1000, 100
        self.internal_comparisons_test(n_stolen, n_sighted, n_matches)


class LargeTestsV3(BaseTester):

    def test_large_all_common(self):
        n_stolen, n_sighted, n_matches = 1000, 1000, 1000
        self.plates_test(n_stolen, n_sighted, n_matches)

    def test_large_all_common_internal_comparisons(self):
        n_stolen, n_sighted, n_matches = 1000, 1000, 1000
        self.comparisons_test(n_stolen, n_sighted, n_matches)

    def test_large_all_common_comparisons(self):
        n_stolen, n_sighted, n_matches = 1000, 1000, 1000
        self.internal_comparisons_test(n_stolen, n_sighted, n_matches)


class HugeTestsV1(BaseTester):

    def test_huge_none_common(self):
        n_stolen, n_sighted, n_matches = 10000, 20000, 0
        self.plates_test(n_stolen, n_sighted, n_matches)

    def test_huge_none_common_internal_comparisons(self):
        n_stolen, n_sighted, n_matches = 10000, 20000, 0
        self.comparisons_test(n_stolen, n_sighted, n_matches)

    def test_huge_none_common_comparisons(self):
        n_stolen, n_sighted, n_matches = 10000, 20000, 0
        self.internal_comparisons_test(n_stolen, n_sighted, n_matches)


class BaseTestLinear(BaseTester):
    """ Unit tests for the sequential plate finder.
    Overrides the setUp method to set the macthing function.
    Overrides the get_bounds method to give bounds for linear search version.
    """

    def setUp(self):
        super().setUp()
        self.matching_function = linear_stolen_plate_finder

    def get_bounds(self, stolen, seen, matches):
        """ Note this range is very generous!
        The exact tests will give you a better idea of how
        well your linear function is working
        """
        if stolen == matches and stolen < seen:
            lower = matches
        else:
            lower = seen
        return lower, seen * stolen


# The following inherit all the base tests and use the methods given in
# the BaseTestLinear class.
# Basically it says which function to test and which bounds to use
# as well as saying to use the files with sorted stolen plates
# which are obviously needed to be able to do binary searching



class TinyLinear(BaseTestLinear, TinyTests):
    pass


class SmallLinear(BaseTestLinear, SmallTests):
    pass


class LargeLinearV1(BaseTestLinear, LargeTestsV1):
    pass


class LargeLinearV2(BaseTestLinear, LargeTestsV2):
    pass


class LargeLinearV3(BaseTestLinear, LargeTestsV3):
    pass


class HugeLinearV1(BaseTestLinear, HugeTestsV1):
    pass


# Here we do some extra tests with known values
class SmallLinearExact(BaseTestLinear):

    def test_010_tiny_comps_exact(self):
        n_stolen, n_sighted, n_matches, expected = 2, 5, 2, 9
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)

    def test_020_small_no_common_comps_exact(self):
        n_stolen, n_sighted, n_matches, expected = 10, 10, 0, 100
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)

    def test_030_small_some_common_comps_exact(self):
        n_stolen, n_sighted, n_matches, expected = 10, 10, 5, 81
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)

    def test_040_small_all_common_comps_exact(self):
        n_stolen, n_sighted, n_matches = 10, 10, 10
        expected = n_stolen * (n_stolen + 1) // 2
        # can you see why expected must be given by the formula above in this case?
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)

    def test_045_small_all_common_comps_exact(self):
        n_stolen, n_sighted, n_matches, expected = 2, 10, 2, 17
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)

    def test_048_small_all_common_comps_exact(self):
        n_stolen, n_sighted, n_matches, expected = 5, 10, 5, 40
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)

    def test_050_small2_no_common_comps_exact(self):
        n_stolen, n_sighted, n_matches, expected = 10, 100, 0, 1000
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)

    def test_060_small2_some_common_comps_exact(self):
        n_stolen, n_sighted, n_matches, expected = 10, 100, 2, 990
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)

    def test_070_small2_all_common_comps_exact(self):
        n_stolen, n_sighted, n_matches = 100, 100, 100
        expected = n_stolen * (n_stolen + 1) // 2
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)

    def test_080_small3_all_common_comps_exact(self):
        n_stolen, n_sighted, n_matches, expected = 10, 1000, 10, 9135
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)


class MediumLinearExact(BaseTestLinear):
    def test_010_medium_no_common_comps_exact(self):
        n_stolen, n_sighted, n_matches, expected = 100, 1000, 0, 100000
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)

    def test_020_medium_some_common_comps_exact(self):
        n_stolen, n_sighted, n_matches, expected = 100, 1000, 5, 99711
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)

    def test_030_medium_all_common_comps_exact(self):
        n_stolen, n_sighted, n_matches, expected = 100, 1000, 100, 91850
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)




class LargeLinearExact(BaseTestLinear):

    def test_010_large_no_common_comps_exact(self):
        n_stolen, n_sighted, n_matches, expected = 10000, 20000, 0, 200000000
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)

    def test_020_large_some_common_comps_exact(self):
        n_stolen, n_sighted, n_matches, expected = 10000, 20000, 1000, 195045673
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)

    def test_030_large_all_common_comps_exact(self):
        n_stolen, n_sighted, n_matches, expected = 1000, 20000, 1000, 19374500
        self.comparisons_test(n_stolen, n_sighted, n_matches, expected)
        StatCounter.reset_comparisons()
        self.internal_comparisons_test(
            n_stolen, n_sighted, n_matches, quiet=True)


class BaseTestBinary(BaseTester):
    """ Unit tests for the binary plate search function. """

    def setUp(self):
        super().setUp()
        self.matching_function = binary_stolen_plate_finder

    def get_bounds(self, n_stolen, n_sighted, n_matches):
        if n_stolen > 0:
            log_stolen = int(math.log(n_stolen, 2))
            if n_stolen == n_matches and n_stolen < n_sighted:
                lower = n_matches * (log_stolen + 1) - 2
            else:
                lower = n_sighted * (log_stolen + 1) - 2
            upper = n_sighted * (log_stolen + 2) + 2
        else:
            lower = 0
            upper = 0
        return lower, upper

    def use_sorted_stolen(self):
        """ Will use files with sorted stolen plates.
        For example:   10s-10-10-a.txt   has the stolen plates in sorted order
        """
        return True


# The following classes inherit all the base tests and use the methods given in
# the BaseTestBinary class.
# Basically it says which function to test and which bounds to use
# as well as saying to use the files with sorted stolen plates
# which are obviously needed to be able to do binary searching



class TinyBinary(BaseTestBinary, TinyTests):
    pass


class SmallBinary(BaseTestBinary, SmallTests):
    pass


class MediumBinary(BaseTestBinary, MediumTests):
    pass




class LargeBinaryV1(BaseTestBinary, LargeTestsV1):
    pass


class LargeBinaryV2(BaseTestBinary, LargeTestsV2):
    pass


class LargeBinaryV3(BaseTestBinary, LargeTestsV3):
    pass


class HugeBinaryV1(BaseTestBinary, HugeTestsV1):
    pass


def all_tests_suite():
    """ Combines test cases from various classes to make a
    big suite of tests to run.
    You can comment out tests you don't want to run and uncomment
    tests that you do want to run :)
    """
    suite = unittest.TestSuite()
    test_loader = unittest.defaultTestLoader.loadTestsFromTestCase

    # suite.addTest(test_loader(TinyLinear))
    # suite.addTest(test_loader(SmallLinear))
    # suite.addTest(test_loader(LargeLinearV1))
    # suite.addTest(test_loader(LargeLinearV2))
    # suite.addTest(test_loader(LargeLinearV3))
    # suite.addTest(test_loader(HugeLinearV1))
    # suite.addTest(test_loader(SmallLinearExact))
    # suite.addTest(test_loader(MediumLinearExact))
    # suite.addTest(test_loader(LargeLinearExact))

    # IMPORTANT NOTE <==================================================================
    # uncomment the following lines when you are ready for binary testing
    suite.addTest(test_loader(TinyBinary))
    suite.addTest(test_loader(SmallBinary))
    suite.addTest(test_loader(MediumBinary))
    suite.addTest(test_loader(LargeBinaryV1))
    suite.addTest(test_loader(LargeBinaryV2))
    suite.addTest(test_loader(LargeBinaryV3))
    suite.addTest(test_loader(HugeBinaryV1))
    return suite




def main():
    """ Makes a test suite and runs it. Will your code pass? """
    test_runner = unittest.TextTestRunner(verbosity=2)
    all_tests = all_tests_suite()
    test_runner.run(all_tests)


if __name__ == '__main__':
    main()
