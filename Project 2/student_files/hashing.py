""" Module containing classes and functions for students to complete.
Read the notes with each question in the submission quiz for more
details on what to submit.
The submission quiz will open around a week before the due date
so you can check your code vs. the quiz server's style checks.
You should be using your own tests to help you debug your code
and the provided tests.py as final checks that your code works
with bigger data sets. Passing tests.py doesn't necessarily
mean that your code works so make sure you don't rely solely
on those tests...

Author: <Micheal combs-calcutt>
Date: <9/29/2025>

"""

import doctest
from classes2 import NumberPlate
from stats import StatCounter




class ListTable:
    """ This is not really a hashtable.
        It stores (plate, value) tuples in a list.
        It uses a simple linear scan through the whole list
        to find a plate.
        When setting a plate's value it scans through the whole list
        to see if the plate is there first. If it is there it updates
        the plate's value, otherwise it appends a (plate, value) tuple
        to the end of the list.
        NOTE:
        Students are required to add code to count comparisons in this class
    """

    def __init__(self, n_slots=0):
        """ Note n_slots is ignored it's there for compatability
        Each (plate, value) record/pair is stored as a tuple.
        Any new records should be simply appended to the data_list.
        The data_list isn't sorted.
        """
        self.data_list = []
        self.n_items = 0
        # n_slots won't be used - it's just here for compatability when testing
        self.n_slots = n_slots
        # NOTE:
        # The following two variables must be updated by your code
        self.n_plate_comparisons = 0   # update whenever number plates are compared
        self.n_plate_hashes = 0   # update whenever hash(number_plate) is called
        # special note for this class no hashes are ever calculated...
        # the variable is left in for compatability with the testing code.

    def __setitem__(self, plate, value):
        """ Called when mylisttable[plate] = value assignment is used.
        Will update the value for the plate if the plate already in the list
        or will append a new record with (plate, flag) to the end of the list.
        >>> table = ListTable()
        >>> plate1 = NumberPlate('ABC123')
        >>> table[plate1] = 'Banana 3'
        >>> plate2 = NumberPlate('BOB456')
        >>> table[plate2] = 'Banana 2'
        >>> plate3 = NumberPlate('JOE234')
        >>> table[plate3] = 'Orange 1'
        >>> print(table)
        List Table:
        0-> ('ABC123', 'Banana 3')
        1-> ('BOB456', 'Banana 2')
        2-> ('JOE234', 'Orange 1')
        <BLANKLINE>
        >>> # update plate2 to have the value 'Banana 1'
        >>> table[plate2] = 'Banana 1'
        >>> print(table)
        List Table:
        0-> ('ABC123', 'Banana 3')
        1-> ('BOB456', 'Banana 1')
        2-> ('JOE234', 'Orange 1')
        <BLANKLINE>
        """
        record = (plate, value)
        i = 0
        updated = False
        while i < len(self.data_list) and not updated:
            current_plate, value = self.data_list[i]
            self.n_plate_comparisons += 1 
            if current_plate == plate:
                self.data_list[i] = record
                updated = True
            i += 1
        if not updated:
            self.data_list.append(record)
            self.n_items += 1

    def __contains__(self, plate):
        """ Called when doing plate in table expressions.
        Will return True if the plate is in the table, otherwise returns False
        >>> table = ListTable()
        >>> plate1 = NumberPlate('ABC123')
        >>> table[plate1] = 'Banana 3'
        >>> plate2 = NumberPlate('BOB456')
        >>> table[plate2] = 'Banana 2'
        >>> plate3 = NumberPlate('JOE234')
        >>> table[plate3] = 'Orange 1'
        >>> print(table)
        List Table:
        0-> ('ABC123', 'Banana 3')
        1-> ('BOB456', 'Banana 2')
        2-> ('JOE234', 'Orange 1')
        <BLANKLINE>
        >>> print(plate1 in table)
        True
        >>> print(plate2 in table)
        True
        >>> print(plate3 in table)
        True
        >>> print(NumberPlate('ZZZ999') in table)
        False
        """
        found = False
        i = 0
        while i < len(self.data_list) and not found:
            current_plate, _ = self.data_list[i]
            #My code
            self.n_plate_comparisons += 1 
            if current_plate == plate:
                found = True
            else:
                i += 1
        return found

    def __getitem__(self, plate):
        """ Returns the value for atable[plate], see examples below.
        >>> table = ListTable()
        >>> plate1 = NumberPlate('ABC123')
        >>> table[plate1] = 'Banana 1'
        >>> plate2 = NumberPlate('BOB456')
        >>> table[plate2] = 'Banana 2'
        >>> plate3 = NumberPlate('JOE234')
        >>> table[plate3] = 'Orange 1'
        >>> print(table)
        List Table:
        0-> ('ABC123', 'Banana 1')
        1-> ('BOB456', 'Banana 2')
        2-> ('JOE234', 'Orange 1')
        <BLANKLINE>
        >>> print(table[plate1])
        Banana 1
        >>> print(table[plate2])
        Banana 2
        >>> print(table[plate3])
        Orange 1
        >>> unknown = NumberPlate('ZZZ999')
        >>> print(table[unknown])
        None
        """
        found = False
        i = 0
        while i < len(self.data_list) and not found:
            current_plate, current_value = self.data_list[i]
            self.n_plate_comparisons += 1 
            if current_plate == plate:
                found = True
            else:
                i += 1
        if not found:
            current_value = None
        return current_value

    def items(self):
        """ Generator that yields all the (plate, value) tuples in the table.
            Note the value could be a flag or a list of time stamps, or any other
            thing that you would like to store in the table...
        """
        for record in self.data_list:
            if record:
                yield record

    def keys(self):
        """ Generator that yields all the plates/keys in the table """
        for record in self.data_list:
            if record:
                plate, _ = record
                yield plate

    def __len__(self):
        """ Returns the number of items stored in the hash table """
        return self.n_items

    def __str__(self):
        result = 'List Table:\n'
        for i, value in enumerate(self.data_list):
            result += f'{i}-> {value}\n'
        return result

    def condensed_str(self):
        """ The list has no gaps so it's already condensed :)
        The only thing different here is the title line...
        """
        result = 'List Table (condensed):\n'
        for i, value in enumerate(self.data_list):
            result += f'{i}-> {value}\n'
        return result
class LinearHashTable:
    """ Your interesting class docstring goes here """

    def __init__(self, n_slots):
        if n_slots <= 0:
            raise ValueError('Come on! A hashtable needs at least 1 slot!')
        self.n_slots = n_slots
        self.table_list = [None] * n_slots  # make empty hash table
        self.n_items = 0
        # NOTE:
        # The following two variables must be updated by your code
        self.n_plate_comparisons = 0   # update whenever number plates are compared
        self.n_plate_hashes = 0   # update whenever hash(number_plate) is called

    def __setitem__(self, plate, value):
        """
        Sets the value for the given plate. Basically stores the (plate, value) tuple
        at the appropriate index in the table_list.

        For example, the following will put a (plate, flag) tuple in the appropriate place
        in the table_list:
        my_table[plate] = flag

        Should raise IndexError('Hashtable is full!') if table is full.
        Note: Whilst you cannot add a new plate to a full table, it is still possible
        to update the value for a plate that is already in the table.
        """
        # ---start student section---
        index = hash(plate) % self.n_slots
        self.n_plate_hashes += 1
        
        for i in range(self.n_slots):
            probe_index = (index + i) % self.n_slots
            entry = self.table_list[probe_index]

            if entry is None:
                # Empty slot found – insert new item
                self.table_list[probe_index] = (plate, value)
                self.n_items += 1
                return
            stored_plate, _ = entry
            self.n_plate_comparisons += 1
            if stored_plate == plate:
                # Plate exists – update value
                self.table_list[probe_index] = (plate, value)
                return
        
        raise IndexError('Hashtable is full!')
        # ===end student section===

    def __contains__(self, plate):
        """ Returns True if the plate is in the table, otherwise False. """
        # ---start student section---
        index = hash(plate) % self.n_slots
        self.n_plate_hashes += 1

        for i in range(self.n_slots):
            probe_index = (index + i) % self.n_slots
            entry = self.table_list[probe_index]

            if entry is None:
                return False

            stored_plate, _ = entry
            self.n_plate_comparisons += 1
            if stored_plate == plate:
                return True

        return False
        # ===end student section===

    def __getitem__(self, plate):
        """ Returns the value associated with the given plate
            or None if the plate isn't in the table.
            Note the value could be a flag or a list of time stamps, or any other
            thing that you would like to store in the table...
            
            For example using the following will invoke this method:
            flag = my_linear_hashtable[plate]
        """
        # ---start student section---
        index = hash(plate) % self.n_slots
        self.n_plate_hashes += 1

        for i in range(self.n_slots):
            probe_index = (index + i) % self.n_slots
            entry = self.table_list[probe_index]
            if entry is None:
                return None
            stored_plate, value = entry
            self.n_plate_comparisons += 1
            if stored_plate == plate:
                return value

        return None
        # ===end student section===

    def items(self):
        """ Generator that yields all the (plate, value) tuples in the table.
        Note the value could be a flag or a list of time stamps, or any other
        thing that you would like to store in the table...
        Usage example:
        for key, value in my_table.items():
            print(key, value)
        """
        for record in self.table_list:
            if record:
                yield record

    def keys(self):
        """ Generator that yields all the plates/keys in the table """
        for record in self.table_list:
            if record:
                plate, _ = record
                yield plate

    def __len__(self):
        """ Returns the number of items stored in the table """
        return self.n_items

    def __str__(self):
        """ Returns a nice version of the table with one slot per line """
        result = 'Linear Hash Table:\n'
        for i, slot_record in enumerate(self.table_list):
            result += f'{i}-> {slot_record}\n'
        return result

    def condensed_str(self):
        """ Similar to the __str__ method by only includes
            slots that are not empty
        """
        result = 'Linear Hash Table (condensed):\n'
        for i, slot_record in enumerate(self.table_list):
            if slot_record:
                result += f'{i}-> {slot_record}\n'
        return result


class ChainingHashTable:
    """ Your interesting class docstring goes here """

    def __init__(self, n_slots):
        self.n_items = 0  # starts out empty
        if n_slots <= 0:
            raise ValueError('Come on! A hashtable needs at least 1 slot!')
        self.n_slots = n_slots  # must provide the number of slots to be used
        # Note: each slot in the table_list contains the list/chain of items
        # that hash to that index. A simple Python list is used for this.
        self.table_list = [[] for _ in range(n_slots)]
        # The following two variables must be updated by your code
        self.n_plate_comparisons = 0   # update whenever number plates are compared
        self.n_plate_hashes = 0   # update whenever hash(number_plate) is called

    def __setitem__(self, plate, value):
        """
        Sets the value for the given plate. Basically stores the (plate, value) tuple
        in the list at the appropriate index in the table_list.
        Note the value could be a flag or a list of time stamps, or any other
        thing that you would like to store in the table...
        
        Each slot in the table_list will contain a list of (plate, value) pairs.
        Using this table to store flags would mean the value for each plate would be a flag string.
        Using this table to store timestamps will mean the value for each plate will be a list
        of timestamps.
        For example, the following will put a (plate, timestamps) tuple in the appropriate place
        in the table_list:
        my_table[plate] = timestamps

        """
        # ---start student section---
        index = hash(plate) % self.n_slots
        self.n_plate_hashes += 1

        # search if plate already exists
        for i, (p, v) in enumerate(self.table_list[index]):
            self.n_plate_comparisons +=1
            if p == plate:
                self.table_list[index][i] = (plate, value)
                return

        # if it doesnt
        self.table_list[index].append((plate, value))
        self.n_items += 1
        # ===end student section===

    def __contains__(self, plate):
        """ Returns True if the plate is in the table, otherwise False. """
        # ---start student section---
        index = hash(plate) % self.n_slots
        self.n_plate_hashes += 1
        # loops though every thing at the index in case of collisions
        for p, _ in self.table_list[index]:
            self.n_plate_comparisons += 1
            if p == plate:
                return True
        return False
        # ===end student section===

    def __getitem__(self, plate):
        """ Returns the value associated with the given plate
            or None if the plate isn't in the table.
            For example using the following will invoke this method:
            flag = my_linear_hashtable[plate]
        """
        # ---start student section---
        index = hash(plate) % self.n_slots
        self.n_plate_hashes += 1
        # loops though every thing at the index in case of collisions
        for p, v in self.table_list[index]:
            self.n_plate_comparisons += 1
            if p == plate:
                return v
        return None
        # ===end student section===

    def items(self):
        """ Generator that yields all the (plate, value) tuples in the table.
        Note the value could be a flag or a list of time stamps, or any other
        thing that you would like to store in the table...
        Usage example:
        for key, value in my_table.items():
            print(key, value)
        """
        for slot_list in self.table_list:
            if slot_list:
                for record in slot_list:
                    yield record

    def keys(self):
        """ Generator that yields all the plates/keys in the table """
        for slot_list in self.table_list:
            if slot_list:
                for record in slot_list:
                    plate, _ = record
                    yield plate

    def __len__(self):
        """ Returns the number of items stored in the hash table"""
        return self.n_items

    def __str__(self):
        """ Returns a nice version of the table with one slot per line """
        result = 'Chaining Hash Table:\n'
        for i, slot_list in enumerate(self.table_list):
            result += f'{i}-> {slot_list}\n'
        return result

    def condensed_str(self):
        """ Similar to the __str__ method by only includes slots that are not empty """
        result = 'Chaining Hash Table (condensed):\n'
        for i, slot_list in enumerate(self.table_list):
            if slot_list:
                result += f'{i}-> {slot_list}\n'
        return result


def generate_db_hash_table(database_list, n_slots, table_class=LinearHashTable):
    """ Makes a hash table of the given class from the (plate, flag) tuples
    in the database_list.
    The key used for storing the values should be the number_plate.
    The items from the database list should be added to the table in
    the order that they are given in the database list.
    For example:
    >>> database_list = [(NumberPlate('AAA321'), 'Alien')]
    >>> database_list.append((NumberPlate('BAA900'), ''))
    >>> table = generate_db_hash_table(database_list, 5)
    >>> print(table)
    Linear Hash Table:
    0-> None
    1-> None
    2-> None
    3-> ('AAA321', 'Alien')
    4-> ('BAA900', '')
    <BLANKLINE>
    """
    db_table = table_class(n_slots)
    # ---start student section---
    for plate, flag in database_list: 
        db_table[plate] = flag
    # ===end student section===
    return db_table


def process_camera_sightings(database_list, sightings, db_table_size, flagged_table_size):
    """
    Makes a LinearHashTable with db_table_size slots and adds all the plates to
    the database with their flags as (plate, flag) tuples. Even plates with
    empty flag strings should be added to the hash database table.

    Then makes a result table that is a ChainingHashTable with flagged_table_size slots.
    The value stored for each plate with be a tuple containing (plate, list_of_timestamps).
    Then the function scans through the sightings (a list of tuples (NumberPlate, timestamp)) 
    and records the timestamps for flagged plates in the results table. NOTE: You only need to 
    record the timestamps for number plates that have a flag in the database (ie, their flag 
    is not just '').

    If a plate is already in the result table then the timestamp should be appended to the list
    of times for that plate.
    If a plate isn't already in the result table then it should be appended to the
    list of (plate, timestamps) tuples held in the list/chain in the slot that the plate
    hashes to.

    Check out the expected_results_table files to get a feel for how the
    results table should look.
    """
    # make the database table using your generate_db_hash_table function
    db_table = generate_db_hash_table(database_list,
                                      db_table_size,
                                      table_class=LinearHashTable
                                      )

    # make an empty chaining hash table to put results in
    results_table = ChainingHashTable(flagged_table_size)
    # make the results table

    # ---start student section---
    for plate, timestamp in sightings:
        if db_table.__contains__(plate):
            flag = db_table[plate]
            if flag != '':
                if results_table.__contains__(plate):
                    results_table[plate].append(timestamp)
                else:
                    results_table.__setitem__(plate,[timestamp])
    # ===end student section===
    # return a tuple containing the db_table and the results table
    return db_table, results_table


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
# NOTE:
# Students don't need to submit any of the following functions
# These are given as a starting point for students' own testing

def trial_hash_table(plate_str_list, table):
    """ Makes plates out of the strings in the list
        then adds the plates to the given table
    """
    for plate_str in plate_str_list:
        plate = NumberPlate(plate_str)
        table[plate] = 'Stolen' + str(plate)
        assert table[plate] == 'Stolen' + str(plate)
    print(table)
    print()
    print(table.condensed_str())


def run_simple_tests():
    """ A nice place for your testing code """
    pass


def example_linearhash_stuff():
    """ This example uses a linear hash table to store
    the flags for some number plates, ie, a small
    database of flags for plates.
    """
    plate = NumberPlate('ABC231')
    flag = 'Overdue fines'
    table = LinearHashTable(11)
    table[plate] = flag        # translates to table.__setitem__(plate, flag)
    print(plate in table)      # translates to table.__contains__(flag)
    print(table[plate])        # translates to table.__getitem__(plate)
    print(table)
    table[plate] = 'new_flag'  # translates to table.__setitem__(plate, 'new_flag')
    # add a new plate and flag to the table
    plate2 = NumberPlate('BBB222')
    table[plate2] = 'BBB222-flag'
    print(table)
    print('\n' * 3)


def example_chaining_stuff():
    """ Example use of the chaining hash table.
    This example uses a chaining hash table to store
    the flags for some number plates, ie, a small
    database of flags for plates.
    """
    plate1 = NumberPlate('BAA754')
    plate2 = NumberPlate('MOO123')
    plate3 = NumberPlate('WOF833')
    plate4 = NumberPlate('EEK003')

    plates = [plate1, plate2, plate3, plate4]

    table = ChainingHashTable(5)
    table[plate1] = 'Sheep'
    table[plate2] = 'Cow'
    table[plate3] = 'Dog'
    table[plate4] = 'Mouse'
    print(table)

    for plate in plates:
        print(f'{plate} in table -> {plate in table}')
    print()
    for plate in plates:
        print(f'Value for {plate} is {table[plate]}')
    print()
    table[plate1] = 'new_flag'  # update the value for plate 1
    plate5 = NumberPlate('BBB222')  # add in a new plate
    table[plate5] = 'BBB222-flag'
    print(table)
    print('plate5 (BBB222) in table:', plate5 in table)


# Students can leave the following out in their submission
if __name__ == '__main__':
    # uncomment the next line to run the ListTable doctests
    doctest.testmod()

    # various examples for you to run and expand upon
    # run_simple_tests()
    # example_linearhash_stuff()
    # example_chaining_stuff()
    pass

