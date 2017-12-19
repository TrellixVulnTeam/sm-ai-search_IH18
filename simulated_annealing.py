# -- File: simulated_annealing.py --
# Author: vzbf32
# Creation Date: 2017-12-18 23:38
# Purpose: This script performs a simulated annealing algorithm on city data to find optimum tours.

import read_tour

tour_data, name, size, cities = read_tour.get_cities("duo_files/AISearchfile535.txt")
print(tour_data, name, size)
[print(cities[x]) for x in range(len(cities))]