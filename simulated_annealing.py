# -- File: simulated_annealing.py --
# Author: vzbf32
# Creation Date: 2017-12-18 23:38
# Purpose: This script performs a simulated annealing algorithm on city data to find optimum tours.

import copy
import read_tour
import random
import sys
import math
from time import time
import os
import errno


class TourManager:
    # Holds our cities 1,...,n
    destination_cities = []

    # Holds our city distances in a 2D array
    cities2d = [[]]

    def add_city(self, city):
        """
        Adds a destination city.
        :param city:
        :return:
        """
        self.destination_cities.append(city)

    def get_city(self, index):
        """
        Returns a city.
        :param index:
        :return:
        """
        return self.destination_cities[index]

    def number_of_cities(self):
        return len(self.destination_cities)

    def set_cities2d(self, list2d):
        TourManager.cities2d = list2d

    def reset(self):
        TourManager.cities2d = [[]]


class Tour:
    def __init__(self, tour=None):
        """
        Initialises our tour.
        :param tour:
        """
        # Holds our list of cities.
        self.tour = []
        # Cache
        self.fitness = 0
        self.distance = 0

        if tour is not None:
            self.tour = copy.copy(tour)
        else:
            # Construct a blank tour
            tm = TourManager()
            for i in range(tm.number_of_cities()):
                self.tour.append(None)

    def generate_individual(self):
        """
        Creates a random individual.
        :return:
        """
        # Loop through all our destination cities and add them to our tour
        tm = TourManager()
        for city_index in range(tm.number_of_cities()):
            self.set_city(city_index, tm.get_city(city_index))
        # Randomly reorder the tour
        random.shuffle(self.tour)

    def get_city(self, tour_position):
        """
        Gets a city from the tour
        :param tour_position:
        :return:
        """
        return self.tour[tour_position]

    def set_city(self, tour_position, city):
        """
        Sets a city in a certain position within a tour.
        :param tour_position:
        :param city:
        :return:
        """
        self.tour[tour_position] = city
        # If the tour's been altered, we need to reset the fitness and distance
        self.fitness = 0
        self.distance = 0

    def get_fitness(self):
        """
        Gets the tour's fitness
        :return:
        """
        if self.fitness == 0:
            self.fitness = 1.0 / self.get_distance()
        return self.fitness

    def get_distance(self):
        """
        Gets the total distance of the tour.
        :return:
        """
        if self.distance == 0:
            tour_distance = 0
            # Loop through our tour's cities
            for city_index in range(self.tour_size()):
                tm = TourManager()
                tour_distance += tm.cities2d[self.get_city(city_index)][self.get_city((city_index+1)%self.tour_size())]
            self.distance = tour_distance
        return self.distance

    def tour_size(self):
        """
        Get number of cities on our tour.
        :return:
        """
        # print(len(self.tour))
        return len(self.tour)

    def contains_city(self, city):
        """
        Check if the tour contains a city.
        :param city:
        :return:
        """
        return city in self.tour

    def __str__(self):
        return str(self.tour)

    def get_raw_tour(self):
        return self.tour

    def get_tour(self):
        return self.tour


class SimulatedAnnealing:
    def acceptance_probability(self, energy, new_energy, temperature):
        """
        Calculate the acceptance probability.
        :param energy:
        :param new_energy:
        :param temperature:
        :return:
        """
        # If the new solution is better, accept it
        if new_energy < energy:
            return 1.0

        # If the new solution is worse, calculate an acceptance probability
        return math.exp( (energy - new_energy) / temperature)

    def __init__(self, file_name):

        # Read our city distances from file and store them in TourManager
        # (True, name, size, cities)
        tm = TourManager()
        tm.reset()
        success, name, size, cities2d = read_tour.get_cities(file_name)
        if not success:
            print("UNSUCCESSFUL")
            print(success)
            print(name)
            print(size)
            print(cities2d)
            quit()
        else:
            # print(cities2d)
            tm.set_cities2d(cities2d)

        # Generate a list of city numbers
        for i in range(1, size+1):
            tm.add_city(i)

        # Set initial temp
        temp = 10000

        cooling_rate = float(sys.argv[4])

        #####
        # Simulate a load of times
        #####
        best_distance = 100000000
        best_solution = []
        best_output = ""
        num_simulations = int(sys.argv[3])
        t_00 = time()
        for j in range(num_simulations):

            if j % (num_simulations/10) == 0:
                print("Completed: " + str(int(100*j/num_simulations)) + "% of this simulation")

            # Initialise initial solution
            current_solution = Tour()
            current_solution.generate_individual()

            # Set as current best
            best = Tour(current_solution.get_tour())

            # Loop until system has cooled
            while temp > 1:
                # Create new neighbour tour
                new_solution = Tour(current_solution.get_tour())

                # Get random positions in the tour
                tour_pos_1 = int(new_solution.tour_size() * random.random())
                tour_pos_2 = int(new_solution.tour_size() * random.random())

                # Get the cities at selected positions in the tour
                city_swap_1 = new_solution.get_city(tour_pos_1)
                city_swap_2 = new_solution.get_city(tour_pos_2)

                # Swap them
                new_solution.set_city(tour_pos_2, city_swap_1)
                new_solution.set_city(tour_pos_1, city_swap_2)

                # Get energy of solutions
                current_energy = current_solution.get_distance()
                neighbour_energy = new_solution.get_distance()

                # Decide if we should accept the neighbour
                if self.acceptance_probability(current_energy, neighbour_energy, temp) > random.random():
                    current_solution = Tour(new_solution.get_tour())

                # Keep track of the best solution found
                if current_solution.get_distance() < best.get_distance():
                    best = Tour(current_solution.get_tour())

                # Cool system
                temp *= 1 - cooling_rate

            if best.get_distance() < best_distance:
                best_distance = best.get_distance()
                best_solution = best.get_raw_tour()
                # Make output string
                output = "NAME = " + name + ",\nTOURSIZE = " + str(size) + ",\nLENGTH = " + str(
                    best_distance) + ",\n"
                for i in range(len(best_solution)):
                    output += str(best_solution[i]) + ","

                # Remove the final comma
                output = output[:-1]

                best_output = output

        t_11 = time()

        print("-----")
        print("BEST DISTANCE:", best_distance)
        print("BEST SOLUTION:", best_solution)
        print("TIME TAKEN:", str(round(t_11 - t_00, 3)) + " seconds")
        print("BEST OUTPUT:")
        print(best_output)
        print("-----")

        output_file_name = sys.argv[2]

        if not os.path.exists(os.path.dirname(output_file_name)):
            try:
                os.makedirs(os.path.dirname(output_file_name))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(output_file_name, "w") as f:
            f.write(best_output)
            f.close()


if __name__ == "__main__":
    sa = SimulatedAnnealing(sys.argv[1])



