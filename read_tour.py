# -- File: read_tour.py --
# Author: vzbf32
# Creation Date: 2017-12-18 21:20
# Purpose: This script loads tour text files, as required for the assignment, and stores them in a suitable data format.

# Import `re` for regex when we parse the file
# Import `os` for reading the file
import re
import os

def get_cities(file_path):
    """
    Parses a search file and returns the distance between cities.
    :param file_path: String. The path of the file to parse
    :return: A tuple `(True, name, size, cities)` where `cities` is a two-dimensional array if successful, otherwise
             a tuple `(False, error_string, None, None)` if unsuccessful
    """
    # Open and read the text file
    if not os.path.exists(file_path):
        return False, "File not found", None, None
    data_file = open(file_path, "r")
    data_text = data_file.read()
    data_file.close()

    # Split elements into a list by comma
    data_split = [x.strip() for x in data_text.split(",")]

    # Clean list - only city values. Anything not a digit or a comma should be removed
    city_split = [re.sub("[^0-9,]", "", y) for y in data_split[2:]]

    # Check the first element is "NAME = xxx"
    if not data_split[0].startswith("NAME = "):
        return False, "Did not start with NAME = "
    # Check the second element is "SIZE = xxx"
    elif not data_split[1].startswith("SIZE = "):
        return False, "Second element did not have SIZE = "
    # Assuming the input data is properly formatted
    else:
        name = data_split[0][7:]
        size = int(data_split[1][7:])

        # Initialise the cities array. e.g. for size 5 it will look like this:
        # [ [0, 0, 0, 0, 0, 0],
        #   [0, 0, 0, 0, 0, 0],
        #   [0, 0, 0, 0, 0, 0],
        #   [0, 0, 0, 0, 0, 0],
        #   [0, 0, 0, 0, 0, 0],
        #   [0, 0, 0, 0, 0, 0] ]
        # The first row and first column will remain full of zeros so that we can access city[x][y] as the distance
        # from city x to city y
        # The diagonals will also remain zero because the distance from any city to itself is zero
        cities = [[0 for j in range(size + 1)] for i in range(size + 1)]

        # Counter is used for accessing values in city_split
        counter = 1

        # Iterate through all the pairs of (0,1), (0,2), ..., (0,n-1), (1,2), (1,3), ..., (1,n-1), ..., (n-2,n-1)
        for i in range(size - 1):
            for j in range(i + 1, size):
                # We use i+1 and j+1 to transform our iterator counters to
                # (1,2), (1,3), ..., (1,n), (2,3), (2,4), ..., (2,n), ..., (n-1,n)

                # print((i+1,j+1), counter, int(city_split[counter-1]))

                cities[i + 1][j + 1] = int(city_split[counter - 1])
                cities[j + 1][i + 1] = int(city_split[counter - 1])

                counter += 1

    return True, name, size, cities


# If we're running this module directly
if __name__ == "__main__":
    filename = "duo_files/AISearchtestcase.txt"
    # filename = "duo_files/AISearchfile012.txt"
    tour_data, name, size, cities = get_cities(filename)
    print(tour_data, name, size)
    [print(cities[x]) for x in range(len(cities))]
