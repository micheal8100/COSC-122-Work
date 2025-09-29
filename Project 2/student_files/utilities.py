""" Use read_dataset to get data from a test file """
from classes2 import NumberPlate


def basic_db_list(plate_strings):
    """ Takes a list of strings and makes a list of tuples
    containing (number_plate, flag) pairs.
    Each number_plate will be a NumberPlate made from the strings.
    The flags will all be str(plate)+'_flag'

    This function will be helpful for simple testing :)

    >>> example = basic_db_list(['ABC123', 'DEF123', 'BAD321'])
    >>> print(example)
    [('ABC123', 'ABC123_flag'), ('DEF123', 'DEF123_flag'), ('BAD321', 'BAD321_flag')]
    """
    result = []
    for plate_str in plate_strings:
        plate = NumberPlate(plate_str)
        record = (plate, str(plate) + '_flag')
        result.append(record)
    return result


def read_timestamped_block(lines, index):
    plate_list = []
    num_lines = len(lines)
    done = False
    while index < num_lines and not done:
        current_line = lines[index]
        if current_line != '\n':
            plate, timestamp = current_line.strip().split(';')
            record = (NumberPlate(plate), timestamp)
            plate_list.append(record)
            #print(record)
            index += 1
        else:
            done = True
    return plate_list, index


def read_db_block(lines, index):
    """ Makes a list of all the (plate,flag) tuples starting from
    the line with the given index, up until a blank line
    is reached - the blank line indicates the end of the
    section of plate date.
    Returns the list of number plates along with the index
    of the blank line
    """
    plate_list = []
    num_lines = len(lines)
    done = False
    while index < num_lines and not done:
        current_line = lines[index]
        if current_line != '\n':
            plate, flag = current_line.strip().split(':')
            record = (NumberPlate(plate), flag)
            plate_list.append(record)
            #print(record)
            index += 1
        else:
            done = True
    return plate_list, index


def read_sightings_block(lines, index):
    """ Makes a list of all the (plate, timestamp) tuples starting from
    the line with the given index, up until a blank line
    is reached - the blank line indicates the end of the
    section of plates.
    Timestamps are iso formatted strings, eg, 20180202T13:13:10
    Returns the list of records along with the index
    of the blank line
    """
    return read_timestamped_block(lines, index)


def read_matches_block(lines, index):
    """ Makes a list of all the (plate, timestamp) tuples starting from
    the line with the given index, up until a blank line
    is reached - the blank line indicates the end of the
    section of plates.
    Timestamps are iso formatted strings, eg, 20180202T13:13:10
    Returns the list of records along with the index
    of the blank line
    """
    return read_timestamped_block(lines, index)


def read_dataset(filename):
    """ Returns the db_list, sightings and flagged_and_sighted lists
    from a test data file.
    """
    with open(filename, encoding='utf-8') as infile:
        lines = infile.readlines()
    i = 0
    _, raw_n_db = lines[i].split('=')
    n_db = int(raw_n_db)
    db_list, end_index = read_db_block(lines, i + 1)
    assert len(db_list) == n_db

    i = end_index + 1  # skip the blank line
    _, raw_sightings = lines[i].split('=')
    num_sightings = int(raw_sightings)
    sightings, end_index = read_sightings_block(lines, i + 1)
    assert len(sightings) == num_sightings

    i = end_index + 1  # skip the blank line
    _, values = lines[i].split('=')
    raw_num_unique, raw_total_num_sighted = values.split(',')
    num_unique = int(raw_num_unique)
    total_num_sighted = int(raw_total_num_sighted)
    matches, _ = read_matches_block(lines, i + 1)
    assert len(matches) == total_num_sighted
    unique = set([plate for plate, _ in matches])
    assert len(unique) == num_unique

    return db_list, sightings, matches


def read_expected(expected_file_name):
    """ Reads the whole expected file into a string and returns it """
    with open(expected_file_name) as expected_file:
        expected = expected_file.read()
    return expected


if __name__ == '__main__':
    example_db_list = basic_db_list(['ABC123', 'DEF123', 'BAD321'])
    print('Basic db list example:')
    print(example_db_list)
    print('\n' * 4)
    print('Basic reading data file example:')
    db_list, sighted_list, in_both = read_dataset('./test_data/5s-10-5-a.txt')
    print('db list=', db_list)
    print()
    print('sighted list=', sighted_list)
    print()
    print('flagged in both=', in_both)
