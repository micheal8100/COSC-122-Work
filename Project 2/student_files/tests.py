"""
tests.py
A module of unit tests to verify your answers
Don't be too worried if you can't understand how they work. You 
should only be commenting/uncommenting the tests in all_tests_suite(),
and then running tests.py.

We recommend starting testing yourself with small lists of values
so that you can work out the expected result list and expected number
of comparisons by hand (instead of running tests.py right away).

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
import string

from classes2 import NumberPlate
from stats import StatCounter, COMPS, HASHES
from hashing import ListTable, LinearHashTable, ChainingHashTable, generate_db_hash_table, process_camera_sightings

TEST_FOLDER = './test_data/'
TEST_FILE_TEMPLATE = '{n_db}-{n_sighted}-{n_flagged_seen}-{seed}.txt'
DEF_SEED = 'a'  # default seed

TEST_FLAG = 'test'

real_count = StatCounter.get_count


def test_records_sequence(max_records):
    """ Generates a sequence of (number_plate, flag) records
    (NumberPlate('AAA000'), 'AAA000_test_1')
    (NumberPlate('AAA001'), 'AAA001_test_2')
    (NumberPlate('AAA002'), 'AAA002_test_3')
    etc...

    n_slots is only used if with_unique_hash is True
    """
    records = []
    count = 0
    for char1 in string.ascii_uppercase:
        for char2 in string.ascii_uppercase:
            for char3 in string.ascii_uppercase:
                for digit1 in string.digits:
                    for digit2 in string.digits:
                        for digit3 in string.digits:
                            plate_str = char1 + char2 + char3
                            plate_str += digit1 + digit2 + digit3
                            flag = '{}_{}_{}'.format(
                                plate_str, TEST_FLAG, count)
                            number_plate = NumberPlate(plate_str)
                            record = (number_plate, flag)
                            records.append(record)
                            count += 1
                            #print(count)
                            if count >= max_records:
                                return records
    return records


TEST_RECORDS = test_records_sequence(200000)
# Note: using a global list for efficiency, each test will use a sequence from
# this global list.


def record_sequence(max_records, n_slots=13, unique_hash=False):
    """ Makes a subset of records from TEST_RECORDS.
    If unique_hash is True then only plates with unique hashes are included
    Generates a sequence of (number_plate, flag) records
    (NumberPlate('AAA000'), 'AAA000_test_1')
    (NumberPlate('AAA001'), 'AAA001_test_2')
    (NumberPlate('AAA002'), 'AAA002_test_3')
    etc...
    n_slots is only used if with_unique_hash is True
    """
    if not unique_hash:
        for i in range(max_records):
            yield TEST_RECORDS[i]
    else:
        if max_records > n_slots:
            raise ValueError(
                "Can't generate more unique slots than there are slots!")
        count = 0
        checked = 0
        hashes_so_far = set()
        result = []
        n_test_records = len(TEST_RECORDS)
        for record in TEST_RECORDS:
            plate, flag = record
            plate_hash = hash(plate) % n_slots
            if plate_hash not in hashes_so_far:
                count += 1
                hashes_so_far.add(plate_hash)
                yield record
            checked += 1
            if count >= max_records:
                return  # done
            if checked >= n_test_records:
                raise IndexError('Whoops, exhausted test sequence...\n'
                                 'This shouldn\'t happen unless you edited the tests - please let the staff know!')

class BaseTestMethods(unittest.TestCase):

    def setUp(self, is_subtest=False):
        """Runs before every test case"""
        StatCounter.reset_counts()
        if not is_subtest:
            # start timer for the test
            self.start_time = time.perf_counter()
        # self.function_to_test should be setup by subclasses with the student function
        # that they want to test

    def tearDown(self):
        self.end_time = time.perf_counter()
        test_time = (self.end_time - self.start_time)
        print(f'{test_time:.4f}s', end=' ')

    def use_sorted_db(self):
        """ Whether to use files with sorted database entries
        or unsorted. Defaults to True.
        Can be over-ridden by sub classes if needed
        """
        return True

    def base_filename(self, n_db, n_sighted, n_matches, seed=DEF_SEED):
        """ n_matches = number of time stamps recorded for sighted vehicles
        that have flags """
        if self.use_sorted_db():
            n_db = str(n_db) + 's'
        return TEST_FILE_TEMPLATE.format(n_db=n_db,
                                         n_sighted=n_sighted,
                                         n_flagged_seen=n_matches,
                                         seed=seed)


class BaseTableTestMethods(BaseTestMethods):

    def table_test_add(self, n_plates, n_slots, records=None, unique_hash=False):
        # needed each time as subtests don't run setup
        self.setUp(is_subtest=True)
        table = self.table_class(n_slots)
        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            table[plate] = flag
        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            flag_from_table = table[plate]
            message = f"Failed to set table[{plate}] to value '{flag}' (got value '{flag_from_table}' instead)"
            self.assertEqual(flag_from_table, flag, msg=message)
        return True  # only happens if passes

    def table_test_contains(self, n_plates, n_slots, records=None, unique_hash=False):
        # needed each time as subtests don't run setup
        self.setUp(is_subtest=True)
        table = self.table_class(n_slots)
        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            table[plate] = flag
        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            message = f"{plate} not found in table (after running table[{plate}] = {flag})"
            self.assertTrue(plate in table, msg=message)
        return True  # only happens if passes

    def table_test_not_contains(self, n_plates, n_slots, records=None, unique_hash=False):
        # needed each time as subtests don't run setup
        self.setUp(is_subtest=True)
        table = self.table_class(n_slots)
        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            table[plate] = flag
        message = f"ZZZ999 was found in table (using __contains__) when it was never added"
        self.assertFalse(NumberPlate('ZZZ999') in table, msg=message)
        return True  # only happens if passes

    def table_test_update(self, n_plates, n_slots, records=None, unique_hash=False):
        # needed each time as subtests don't run setup
        self.setUp(is_subtest=True)
        table = self.table_class(n_slots)
        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            #print(plate, hash(plate)%n_slots)
            table[plate] = flag

        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            #print(plate, hash(plate)%n_slots)
            table[plate] = flag + '-updated'

        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            flag_from_table = table[plate]
            message = f"Failed to update the value of table[{plate}] to '{flag}-updated' (got value '{flag_from_table}' instead)"
            self.assertEqual(flag_from_table, flag + '-updated', msg=message)
        return True  # only happens if passes

    def table_build_comparisons_unique(self, n_plates, n_slots, records=None):
        # needed each time as subtests don't run setup
        self.setUp(is_subtest=True)
        unique_hash = True
        table = self.table_class(n_slots)
        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            table[plate] = flag
        n_plate_comparisons = table.n_plate_comparisons
        expected_comparisons = self.build_comps_with_unique_hashes(n_plates)
        message = f"Your code reported using {n_plate_comparisons} NumberPlate comparisons "
        message += f"but was expected to use {int(expected_comparisons)}."
        self.assertEqual(n_plate_comparisons, expected_comparisons, msg=message)
        return True  # only happens if passes

    def table_build_comparisons_non_unique(self, n_plates, n_slots, records=None):
        # needed each time as subtests don't run setup
        self.setUp(is_subtest=True)
        unique_hash = False
        table = self.table_class(n_slots)
        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            table[plate] = flag
        n_plate_comparisons = table.n_plate_comparisons
        expected_comparisons = self.build_comps_upper_limit_non_unique(
            n_plates, n_slots)
        message = f"Your code reported using {n_plate_comparisons} NumberPlate comparisons "
        message += f"but was expected to use less than or equal to {int(expected_comparisons)}."
        self.assertLessEqual(n_plate_comparisons, expected_comparisons, msg=message)
        return True  # only happens if passes

    def table_test_expected_hash_count(self, n_plates, n_slots, records=None):
        # needed each time as subtests don't run setup
        self.setUp(is_subtest=True)
        unique_hash = False
        table = self.table_class(n_slots)
        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            table[plate] = flag
            plate in table
        n_plate_hashes = table.n_plate_hashes
        expected_hashes = n_plates*2
        try:
            if self.table_class is ListTable:
                expected_hashes = 0
        except NameError:
            pass #if ListTable is not defined

        message = f"Your code reported using {n_plate_hashes} NumberPlate hashes "
        message += f"but was expected to use {int(expected_hashes)}."
        self.assertEqual(n_plate_hashes, expected_hashes, msg=message)
        return True  # only happens if passes

    def table_test_actual_hash_count(self, n_plates, n_slots, records=None):
        # needed each time as subtests don't run setup
        self.setUp(is_subtest=True)
        unique_hash = False
        table = self.table_class(n_slots)
        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            table[plate] = flag
            plate in table
        n_plate_hashes = table.n_plate_hashes
        actual_hashes = real_count(HASHES)
        message = f"Your code reported using {n_plate_hashes} NumberPlate hashes "
        message += f"but it actually used {int(actual_hashes)}. "
        message += "This means you are miscounting NumberPlate hashes, eg, "
        message += "not counting NumberPlate hashes when they are done or "
        message += "counting NumberPlate hashes that weren't done."
        self.assertEqual(n_plate_hashes, actual_hashes, msg=message)
        return True  # only happens if passes

    def db_actual_comparisons_test_add(self, n_plates, n_slots, records=None, unique_hash=False):
        # needed each time as subtests don't run setup
        self.setUp(is_subtest=True)
        table = self.table_class(n_slots)
        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            table[plate] = flag
        n_plate_comparisons = table.n_plate_comparisons
        message = f"Your code reported using {n_plate_comparisons} NumberPlate comparisons "
        message += f"but it actually used {real_count(COMPS)}. "
        message += "This means you are miscounting NumberPlate comparisons, eg, "
        message += "not counting NumberPlate comparisons when they are made or "
        message += "counting NumberPlate comparisons that weren't made."
        self.assertEqual(n_plate_comparisons, real_count(COMPS), msg=message)
        #print('c={}'.format(n_plate_comparisons), end=' ')
        return True  # only happens if passes

    def db_actual_comps_test_add_and_read(self, n_plates, n_slots, records=None, unique_hash=False):
        # needed each time as subtests don't run setup
        self.setUp(is_subtest=True)
        table = self.table_class(n_slots)
        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            table[plate] = flag
        n_plate_comparisons = table.n_plate_comparisons

        message_suffix = "This means you are miscounting NumberPlate comparisons, eg, "
        message_suffix += "not counting NumberPlate comparisons when they are made or "
        message_suffix += "counting NumberPlate comparisons that weren't made."

        message = f"Your code reported using {n_plate_comparisons} NumberPlate comparisons "
        message += f"but it actually used {real_count(COMPS)}. " + message_suffix
        self.assertEqual(n_plate_comparisons, real_count(COMPS), msg=message)
        # now find them all
        for plate, flag in record_sequence(n_plates, n_slots, unique_hash):
            flag_from_table = table[plate]
            message = f"Failed to set table[{plate}] to value '{flag}' (got value '{flag_from_table}' instead)"
            self.assertEqual(flag_from_table, flag, msg=message)
        n_plate_comparisons = table.n_plate_comparisons
        message = f"Your code reported using {n_plate_comparisons} NumberPlate comparisons "
        message += f"but it actually used {real_count(COMPS)}. " + message_suffix
        self.assertEqual(n_plate_comparisons, real_count(COMPS), msg=message)
        return True  # only happens if passes


class TableTests(BaseTableTestMethods):

    def test_010_add_plates(self):
        unique_hash = True
        max_plates = int(self.n_test_slots * self.max_load_factor)
        if max_plates > self.n_test_slots:
            unique_hash = False
        for n_plates in range(1, max_plates, self.step):
            passed = False
            with self.subTest(n_plates=n_plates):
                passed = self.table_test_add(
                    n_plates, self.n_test_slots, unique_hash)
            if not passed:
                break  # stop after the first subtest failure

    def test_020_contains(self):
        unique_hash = True
        max_plates = int(self.n_test_slots * self.max_load_factor)
        if max_plates > self.n_test_slots:
            unique_hash = False
        for n_plates in range(1, max_plates, self.step):
            passed = False
            with self.subTest(n_plates=n_plates):
                passed = self.table_test_contains(
                    n_plates, self.n_test_slots, unique_hash)
            if not passed:
                break  # stop after the first subtest failure

    def test_030_not_contains(self):
        unique_hash = True
        max_plates = int(self.n_test_slots * self.max_load_factor)
        if max_plates > self.n_test_slots:
            unique_hash = False
        for n_plates in range(1, max_plates, self.step):
            passed = False
            with self.subTest(n_plates=n_plates):
                passed = self.table_test_not_contains(
                    n_plates, self.n_test_slots, unique_hash)
            if not passed:
                break  # stop after the first subtest failure

    def test_040_build_comparisons_unique(self):
        unique_hash = True
        # can't have all unique slots if there aren't enough...
        max_plates = self.n_test_slots
        for n_plates in range(1, max_plates, self.step):
            passed = False
            with self.subTest(n_plates=n_plates):
                passed = self.table_build_comparisons_unique(
                    n_plates, self.n_test_slots)
            if not passed:
                break  # stop after the first subtest failure

    def test_050_build_comparisons_non_unique(self):
        max_plates = int(self.n_test_slots * self.max_load_factor)
        for n_plates in range(1, max_plates, self.step):
            passed = False
            if n_plates / self.n_test_slots <= 0.5:
                with self.subTest(n_plates=n_plates, n_slots=self.n_test_slots):
                    passed = self.table_build_comparisons_non_unique(
                        n_plates, self.n_test_slots)
                if not passed:
                    break  # stop after the first subtest failure
            else:
                # don't run for high load factors as our estimate gets wobbly
                pass

    def test_060_actual_comps_add_unique(self):
        unique_hash = True
        max_plates = int(self.n_test_slots * self.max_load_factor)
        if max_plates > self.n_test_slots:
            unique_hash = False
        for n_plates in range(1, max_plates, self.step):
            passed = False
            with self.subTest(n_plates=n_plates, n_slots=self.n_test_slots):
                passed = self.db_actual_comparisons_test_add(
                    n_plates, self.n_test_slots, unique_hash)
            if not passed:
                break  # stop after the first subtest failure

    def test_070_actual_comps_add_non_unique(self):
        max_plates = self.n_test_slots
        for n_plates in range(1, max_plates, self.step):
            passed = False
            with self.subTest(n_plates=n_plates, n_slots=self.n_test_slots):
                passed = self.db_actual_comparisons_test_add(
                    n_plates, self.n_test_slots, unique_hash=False)
            if not passed:
                break  # stop after the first subtest failure

    def test_080_actual_comps_add_and_read(self):
        max_plates = self.n_test_slots
        for n_plates in range(1, max_plates, self.step):
            passed = False
            with self.subTest(n_plates=n_plates):
                passed = self.db_actual_comps_test_add_and_read(
                    n_plates, self.n_test_slots, unique_hash=False)
            if not passed:
                break  # stop after the first subtest failure

    def test_090_table_test_update(self):
        unique_hash = True
        max_plates = int(self.n_test_slots * self.max_load_factor)
        if max_plates > self.n_test_slots:
            unique_hash = False
        for n_plates in range(1, max_plates, self.step):
            passed = False
            with self.subTest(n_plates=n_plates):
                passed = self.table_test_update(
                    n_plates, self.n_test_slots, unique_hash)
            if not passed:
                break  # stop after the first subtest failure

    def test_100_expected_hash_count(self):
        max_plates = int(self.n_test_slots * self.max_load_factor)
        for n_plates in range(1, max_plates, self.step):
            passed = False
            if n_plates / self.n_test_slots <= 0.5:
                with self.subTest(n_plates=n_plates, n_slots=self.n_test_slots):
                    passed = self.table_test_expected_hash_count(
                        n_plates, self.n_test_slots)
                if not passed:
                    break  # stop after the first subtest failure
            else:
                # don't run for high load factors as our estimate gets wobbly
                pass

    def test_110_actual_hash_count(self):
        max_plates = int(self.n_test_slots * self.max_load_factor)
        for n_plates in range(1, max_plates, self.step):
            passed = False
            if n_plates / self.n_test_slots <= 0.5:
                with self.subTest(n_plates=n_plates, n_slots=self.n_test_slots):
                    passed = self.table_test_actual_hash_count(
                        n_plates, self.n_test_slots)
                if not passed:
                    break  # stop after the first subtest failure
            else:
                # don't run for high load factors as our estimate gets wobbly
                pass

class TinyTableTests(TableTests):

    def setUp(self, is_subtest=False):
        super().setUp(is_subtest)
        self.n_test_slots = 11
        self.step = 1  # tests with 1, 2, 3, ... 11 plates


class MediumTableTests(TableTests):

    def setUp(self, is_subtest=False):
        super().setUp(is_subtest)
        self.n_test_slots = 1009
        self.step = 100  # tests with 1, 101, 201, ... 1001 plates


class LargeTableTests(TableTests):

    def setUp(self, is_subtest=False):
        super().setUp(is_subtest)
        self.n_test_slots = 51803
        self.step = 10000  # tests with 1, 10001, ... 50001 plates

        # add one thing then check if it's there
        # add one thing then check for something that's not there
        # add one thing, then update, then check it's updated
        # add two things then check if they are both there
        # add two things and check for something that's not there


class BaseTestListTable(TableTests):
    """ Unit tests for the Linear Probing Hash Table.
    Overrides the setUp method to set the type of table being used.
    Overrides the get_bounds method to give bounds for linear search version.
    """

    def setUp(self, is_subtest=False):
        super().setUp(is_subtest)
        self.table_class = ListTable
        self.max_load_factor = 1  # not actually relevant but here for completeness

    def build_comps_with_unique_hashes(self, n_items, n_slots=None):
        """ As a list is being used this will be
        0+1+2+3+4+...+n-1 = (n(n-1))/2
        NOTE: n_slots isn't used here as the list isn't of fixed size,
        ie, it grows as more items are added...
        """
        return (n_items * (n_items - 1)) / 2

    def build_comps_upper_limit_non_unique(self, n_items, n_slots):
        """ Will be the same as for the unique version as
        no hashing is done...
        """
        return (n_items * (n_items - 1)) / 2


class TinyTableTestsListTable(BaseTestListTable, TinyTableTests):
    pass


class MediumTableTestsListTable(BaseTestListTable, MediumTableTests):
    pass


class LargeTableTestsListTable(BaseTestListTable):

    def setUp(self, is_subtest=False):
        super().setUp(is_subtest)
        self.n_test_slots = 51803
        # set step so just does 1 plate and then 26000 plates, as ListTable sucks!
        self.step = 26000


class BaseTestLinearProbing(BaseTableTestMethods):
    """ Unit tests for the Linear Probing Hash Table.
    Overrides the setUp method to set the type of table being used.
    Overrides the get_bounds method to give bounds for linear search version.
    """

    def setUp(self, is_subtest=False):
        super().setUp(is_subtest)
        self.table_class = LinearHashTable  # ListTable
        self.max_load_factor = 1

    def build_comps_with_unique_hashes(self, n_items, n_slots=None):
        """ n_items must be <= n_slots and all items have unique
        hashes.
        If n_slots isn't provided it will be assumed to be > n_items.

        This will mean that zero comparisons are used when adding
        all the items as they all go straight to their own slot
        which will initially be empty.
        """
        return 0

    def build_comps_upper_limit_non_unique(self, n_items, n_slots):
        """ Uses the worst case for a search when the table has
        been fully built as an upper limit for all insertions.
        Note: This is a very generous upper limit...
        """
        load = n_items / n_slots
        return n_items * (0.5 * (1 + (1 / (1 - load)) ** 2))

# The following inherit all the base tests and use the methods given in
# the BaseTestBinary class.
# Basically it says which function to test and which bounds to use
# as well as saying to use the files with sorted stolen plates
# which are obviously needed to be able to do binary searching


class TinyTableTestsLP(BaseTestLinearProbing, TinyTableTests):
    pass


class MediumTableTestsLP(BaseTestLinearProbing, MediumTableTests):
    pass


class LargeTableTestsLP(BaseTestLinearProbing, LargeTableTests):
    pass


class BaseTestChaining(BaseTableTestMethods):
    """ Unit tests for the Linear Probing Hash Table.
    Overrides the setUp method to set the type of table being used.
    Overrides the get_bounds method to give bounds for linear search version.
    """

    def setUp(self, is_subtest=False):
        super().setUp(is_subtest)
        self.table_class = ChainingHashTable
        self.max_load_factor = 2

    def build_comps_with_unique_hashes(self, n_items, n_slots=None):
        """ n_items must be <= n_slots and all items have unique
        hashes.
        If n_slots isn't provided it will be assumed to be > n_items.

        This will mean that zero comparisons are used when adding
        all the items as they all go straight to their own slot
        which will initially be empty.
        """
        return 0

    def build_comps_upper_limit_non_unique(self, n_items, n_slots):
        """ Uses the worst case for a search when the table has
        been fully built as an upper limit for all insertions.
        Note: This is a very generous upper limit...
        """
        load = n_items / n_slots
        return n_items * load


class TinyTableTestsChaining(BaseTestChaining, TinyTableTests):
    pass


class MediumTableTestsChaining(BaseTestChaining, MediumTableTests):
    pass


class LargeTableTestsChaining(BaseTestChaining, LargeTableTests):
    pass


class TestMakingDbTableBase(BaseTableTestMethods):

    def generate_db_hash_table_test(self, n_items, n_sighted, n_matches, n_slots):
        base_file = self.base_filename(n_items, n_sighted, n_matches)
        test_file_name = TEST_FOLDER + base_file
        database_list, sightings, matches = utilities.read_dataset(
            test_file_name)
        if self.table_class == LinearHashTable:
            expected_part = 'expected_db_linear_'
        elif self.table_class == ChainingHashTable:
            expected_part = 'expected_db_chaining_'
        else:
            expected_part = 'expected_db_table_list_'
        template = '{}{}{}-{}.txt'
        txtless_basefile = base_file[:-4]  # strips the .txt
        expected_file_name = template.format(TEST_FOLDER,
                                             expected_part,
                                             txtless_basefile,
                                             n_slots)
        expected_table_str = utilities.read_expected(expected_file_name)
        database = generate_db_hash_table(database_list,
                                          n_slots,
                                          table_class=self.table_class)
        self.assertEqual(str(database), expected_table_str)
        return True


class TestMakingDbTableSmall(TestMakingDbTableBase):

    def test_1000_making_small_db_tables_from_file_data(self):
        settings = [(5, 10, 5),
                    (5, 10, 2),
                    (10, 10, 5),
                    (10, 10, 2),
                    ]
        for n_items, n_sighted, n_matches in settings:
            passed = False
            n_slots = n_items * 2
            with self.subTest(n_items=n_items, n_sighted=n_sighted, n_matches=n_matches):
                self.setUp(
                    is_subtest=True)  # needed each time as subtests don't run setup
                passed = self.generate_db_hash_table_test(
                    n_items, n_sighted, n_matches, n_slots)
            if not passed:
                break  # stop after the first subtest failure
            passed = False
            if self.max_load_factor == 2:  # for testing chainging hash table
                n_slots = n_items // 2
                with self.subTest(n_items=n_items, n_sighted=n_sighted, n_matches=n_matches):
                    passed = self.generate_db_hash_table_test(
                        n_items, n_sighted, n_matches, n_slots)
                if not passed:
                    break  # stop after the first subtest failure


class TestMakingDbTableLarge(TestMakingDbTableBase):

    def test_1010_making_large_db_tables_from_file_data(self):
        settings = [(100, 10, 5),
                    (100, 10, 2),
                    (100, 5, 2),
                    (100, 5, 0),
                    ]
        passed = False
        for n_items, n_sighted, n_matches in settings:
            passed = False
            n_slots = n_items * 2
            with self.subTest(n_items=n_items, n_sighted=n_sighted, n_matches=n_matches):
                passed = self.generate_db_hash_table_test(
                    n_items, n_sighted, n_matches, n_slots)
            if not passed:
                break  # stop after the first subtest failure
            passed = False
            if self.max_load_factor == 2:  # for testing chainging hash table
                n_slots = n_items // 2
                with self.subTest(n_items=n_items, n_sighted=n_sighted, n_matches=n_matches):
                    passed = self.generate_db_hash_table_test(
                        n_items, n_sighted, n_matches, n_slots)
                if not passed:
                    break  # stop after the first subtest failure


class TestMakingDbTableLinear(TestMakingDbTableSmall, TestMakingDbTableLarge):

    def setUp(self, is_subtest=False):
        super().setUp(is_subtest)
        self.table_class = LinearHashTable
        self.max_load_factor = 0.5


class TestMakingDbTableChaining(TestMakingDbTableSmall, TestMakingDbTableLarge):

    def setUp(self, is_subtest=False):
        super().setUp(is_subtest)
        self.table_class = ChainingHashTable

        # this will induce the test methods to do a variation with n_slots = n_items // 2
        self.max_load_factor = 2


class BaseCameraStreamTests(BaseTestMethods):

    def process_stream_test(self, n_items, n_sighted, n_matches, db_table_size, results_table_size):
        """ Note: The condensed_str of results is used when results_table_size > 100 """
        self.setUp(is_subtest=True)
        # get expected db table
        base_file = self.base_filename(n_items, n_sighted, n_matches)
        test_file_name = TEST_FOLDER + base_file
        database_list, sightings, matches = utilities.read_dataset(
            test_file_name)
        expected_db_part = ''
        template = '{}expected_db_linear_{}-{}.txt'
        txtless_basefile = base_file[:-4]  # strips the .txt
        expected_db_file_name = template.format(TEST_FOLDER,
                                                txtless_basefile,
                                                db_table_size)

        expected_db_table_str = utilities.read_expected(expected_db_file_name)

        # get expected results table
        template = '{}expected_results_table_{}-{}-{}.txt'
        txtless_basefile = base_file[:-4]  # strips the .txt
        expected_results_file_name = template.format(TEST_FOLDER,
                                                     txtless_basefile,
                                                     db_table_size,
                                                     results_table_size)
        expected_results_table_str = utilities.read_expected(
            expected_results_file_name)

        # get db table and results table
        database, results = process_camera_sightings(database_list,
                                                     sightings,
                                                     db_table_size,
                                                     results_table_size)

        self.assertEqual(str(database), expected_db_table_str)

        # expected results for tables larger than 100 will be in condensed form.
        if results_table_size <= 100:
            self.assertEqual(str(results), expected_results_table_str)
        else:
            self.assertEqual(results.condensed_str(),
                             expected_results_table_str)
        return True


class SmallProcessCameraTests(BaseCameraStreamTests):

    def test_2000_small_process_camera_sightings(self):
        settings = [(5, 10, 2, 10, 2),
                    (5, 10, 5, 10, 2),
                    (10, 10, 2, 20, 5),
                    (10, 10, 5, 20, 5),
                    ]
        passed = False
        for n_items, n_sighted, n_matches, db_size, results_size in settings:
            with self.subTest(n_items=n_items, n_sighted=n_sighted, n_matches=n_matches):
                passed = self.process_stream_test(n_items,
                                                  n_sighted,
                                                  n_matches,
                                                  db_size,
                                                  results_size)
            if not passed:
                break  # stop after the first subtest failure
            #if self.max_load_factor == 2:  # for testing chaining hash table
                #n_slots = n_items // 2
                #with self.subTest(n_items=n_items, n_sighted=n_sighted, n_matches=n_matches):
                #passed = self.generate_db_hash_table_test(n_items, n_sighted, n_matches, n_slots)
                #if not passed:
                #break  # stop after the first subtest failure


class MediumProcessCameraTests(BaseCameraStreamTests):

    def test_2010_medium_process_camera_sightings(self):
        settings = [(100, 10, 5, 200, 5),
                    (100, 100, 10, 200, 50),
                    (100, 2000, 10, 200, 50),
                    (100, 10000, 2000, 200, 50),
                    ]
        passed = False
        for n_items, n_sighted, n_matches, db_size, results_size in settings:
            with self.subTest(n_items=n_items, n_sighted=n_sighted, n_matches=n_matches):
                passed = self.process_stream_test(n_items,
                                                  n_sighted,
                                                  n_matches,
                                                  db_size,
                                                  results_size)
            if not passed:
                break  # stop after the first subtest failure


class LargeProcessCameraTests(BaseCameraStreamTests):

    def test_2020_large_process_camera_sightings(self):
        settings = [(10000, 10000, 2000, 20000, 5000),
                    (10000, 10000, 5000, 20000, 5000),
                    (50000, 10000, 5000, 100000, 5000),
                    (50000, 50000, 5000, 100000, 25000)
                    ]
        passed = False
        for n_items, n_sighted, n_matches, db_size, results_size in settings:
            with self.subTest(n_items=n_items, n_sighted=n_sighted, n_matches=n_matches):
                passed = self.process_stream_test(n_items,
                                                  n_sighted,
                                                  n_matches,
                                                  db_size,
                                                  results_size)
            if not passed:
                break  # stop after the first subtest failure




def all_tests_suite():
    """ Combines test cases from various classes to make a
    big suite of tests to run.
    You can comment out tests you don't want to run and uncomment
    tests that you do want to run :)
    """
    suite = unittest.TestSuite()
    test_loader = unittest.defaultTestLoader.loadTestsFromTestCase

    suite.addTest(test_loader(TinyTableTestsListTable))
    suite.addTest(test_loader(MediumTableTestsListTable))
    # Note: LargeTableTestsListTable take a while to run (30+ minutes)! 
    # The large tests for proper hash tables (LP and chaining) should be
    # much faster.
    # suite.addTest(test_loader(LargeTableTestsListTable))

    # suite.addTest(test_loader(TinyTableTestsLP))
    # suite.addTest(test_loader(MediumTableTestsLP))
    # suite.addTest(test_loader(LargeTableTestsLP))

    # suite.addTest(test_loader(TinyTableTestsChaining))
    # suite.addTest(test_loader(MediumTableTestsChaining))
    # suite.addTest(test_loader(LargeTableTestsChaining))

    # suite.addTest(test_loader(TestMakingDbTableLinear))
    # suite.addTest(test_loader(TestMakingDbTableChaining))

    suite.addTest(test_loader(SmallProcessCameraTests))
    suite.addTest(test_loader(MediumProcessCameraTests))
    suite.addTest(test_loader(LargeProcessCameraTests))

    return suite




def main():
    """ Makes a test suite and runs it. Will your code pass? """
    test_runner = unittest.TextTestRunner(verbosity=2)
    all_tests = all_tests_suite()
    test_runner.run(all_tests)



if __name__ == '__main__':
    main()
