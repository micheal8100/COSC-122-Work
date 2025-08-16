""" Use read_data_set to get data from a test file """

from classes import NumberPlate



def read_plate_block(lines, index):
    """ Makes a list of all the plates starting from
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
            for item in current_line.strip().split(' '):
                plate_list.append(NumberPlate(item))
            index += 1
        else:
            done = True
    return plate_list, index


def read_dataset(filename):
    """ Returns the stolen_list, sightings and sighted_stolen_list
    from a test data file.
    """
    with open(filename, encoding='utf-8') as infile:
        lines = infile.readlines()
    i = 0
    _, raw_num_stolen = lines[i].split('=')
    num_stolen = int(raw_num_stolen)
    stolen_list, end_index = read_plate_block(lines, i + 1)
    assert len(stolen_list) == num_stolen

    i = end_index + 1  # skip the blank line
    _, raw_sightings = lines[i].split('=')
    num_sightings = int(raw_sightings)
    sightings, end_index = read_plate_block(lines, i + 1)
    assert len(sightings) == num_sightings

    i = end_index + 1  # skip the blank line
    _, raw_sighted_stolen = lines[i].split('=')
    num_sighted_stolen = int(raw_sighted_stolen)
    sighted_stolen_list, _ = read_plate_block(lines, i + 1)
    assert len(sighted_stolen_list) == num_sighted_stolen
    return stolen_list, sightings, sighted_stolen_list
