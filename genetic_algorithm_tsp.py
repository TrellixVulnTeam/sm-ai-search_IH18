# -- File: genetic_algorithm.py --
# Author: vzbf32
# Creation Date: 2017-12-19 20:04
# Purpose: This script performs a genetic algorithm on city data to find optimum tours.

import random
import read_tour
from time import time
import sys

class TourManager:
    # Holds our cities
    destination_cities = []

    # Holds our cities in a 2D array
    cities2d = [[]]

    def add_city(self, city: int):
        """
        Adds a destination city.
        :param city:
        :return:
        """
        self.destination_cities.append(city)

    def get_city(self, index: int):
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
            self.tour = tour
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


class Population:
    def __init__(self, population_size, initialise):
        """
        Construct a population.
        :param population_size:
        :param initialise:
        """
        # Holds population of tours
        self.tours = [None for i in range(population_size)]
        # If we need to initialise a population of tours, do so
        if initialise:
            # Loop and create individuals
            for i in range(self.population_size()):
                new_tour = Tour()
                new_tour.generate_individual()
                self.save_tour(i, new_tour)

    def save_tour(self, index, tour):
        """
        Saves a tour.
        :param index:
        :param tour:
        :return:
        """
        self.tours[index] = tour

    def get_tour(self, index):
        """
        Gets a tour.
        :param index:
        :return:
        """
        return self.tours[index]

    def get_fittest(self):
        """
        Gets the best tour in the population.
        :return:
        """
        fittest = self.tours[0]
        # Loop through individuals to find the fittest
        for i in range(1, self.population_size()):
            if fittest.get_fitness() <= self.get_tour(i).get_fitness():
                fittest = self.get_tour(i)
        return fittest

    def population_size(self):
        """
        Returns population size.
        :return:
        """
        return len(self.tours)


class GA:
    # GA Parameters
    MUTATION_RATE   = 0.3
    TOURNAMENT_SIZE = 5
    ELITISM         = True

    def evolve_population(self, pop):
        """
        Evolves a population over one generation.
        :param pop:
        :return:
        """
        new_population = Population(pop.population_size(), False)

        # Keep our best individual if elitism is enabled
        elitism_offset = 0
        if self.ELITISM:
            new_population.save_tour(0, pop.get_fittest())
            elitism_offset = 1

        # Crossover population
        # Loop over new population's size and create individuals from current population
        for i in range(elitism_offset, new_population.population_size()):
            # Select parents
            parent1 = self.tournament_selection(pop)
            parent2 = self.tournament_selection(pop)
            # Crossover parents
            child = self.crossover(parent1, parent2)
            # Add child to new population
            new_population.save_tour(i, child)

        # Mutate the population a bit to add some new genetic material
        for i in range(elitism_offset, new_population.population_size()):
            self.mutate(new_population.get_tour(i))

        return new_population

    def crossover(self, parent1, parent2):
        """
        Applies crossover to a set of parents and creates offspring
        :param parent1:
        :param parent2:
        :return:
        """
        # Create a new child tour
        child = Tour()

        # Get start and end sub tour positions for parent1's tour
        start_pos = int(random.random() * parent1.tour_size())
        end_pos = int(random.random() * parent1.tour_size())

        # Loop and add the sub tour from parent1 to our child
        for i in range(child.tour_size()):
            # If our start position is less than the end position
            if start_pos < end_pos and i > start_pos and i < end_pos:
                child.set_city(i, parent1.get_city(i))
            # Else if our start position is larger
            elif start_pos > end_pos:
                if not (i < start_pos and i > end_pos):
                    child.set_city(i, parent1.get_city(i))

        # Loop through parent2's city tour
        for i in range(parent2.tour_size()):
            # If child doesn't have the city, add it
            if not child.contains_city(parent2.get_city(i)):
                # Loop to find a spare position in the child's tour
                for j in range(child.tour_size()):
                    if child.get_city(j) is None:
                        child.set_city(j, parent2.get_city(i))
                        break

        return child

    def mutate(self, tour):
        """
        Mutate a child using swap mutation.
        :param tour:
        :return:
        """
        for tour_pos_1 in range(tour.tour_size()):
            # Apply mutation rate
            if random.random() < self.MUTATION_RATE:
                # Get a second random position in the tour
                tour_pos_2 = int(tour.tour_size() * random.random())

                # Get the cities at target position in tour
                city1 = tour.get_city(tour_pos_1)
                city2 = tour.get_city(tour_pos_2)

                # Swap them around
                tour.set_city(tour_pos_2, city1)
                tour.set_city(tour_pos_1, city2)

    def tournament_selection(self, pop):
        """
        Selects candidate tour for crossover.
        :param pop:
        :return:
        """
        # Create a tournament population
        tournament = Population(self.TOURNAMENT_SIZE, False)
        # For each place in the tournament, get a random candidate tour and add it
        for i in range(self.TOURNAMENT_SIZE):
            random_id = int(random.random() * pop.population_size())
            tournament.save_tour(i, pop.get_tour(random_id))
        # Get the fittest tour
        fittest = tournament.get_fittest()
        return fittest


class TSP_GA:
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
            print(cities2d)
            tm.set_cities2d(cities2d)

        # Generate a list of city numbers
        for i in range(1, size+1):
            tm.add_city(i)


        #####
        # Simulate a load of times
        #####
        best_distance = 1000000
        best_solution = []
        best_output = ""
        num_simulations = 6
        t_00 = time()
        for j in range(num_simulations):
            # Initialise population
            pop = Population(50, True)

            print()
            print()
            print("### SIMULATION NO.", j+1, "for", file_name, "###")
            print("Initial distance:", pop.get_fittest().get_distance())

            t0 = time()

            # Evolve population for N generations
            print("Running...")
            N = 1000
            ga = GA()
            pop = ga.evolve_population(pop)
            for i in range(1,N+1):
                if i % (N/10) == 0:
                    print("Completed: " + str(int(100*i/N)) + "% of this simulation, " + "roughly " + str(int( 100*j/num_simulations )) + "% completed overall")
                    pass
                pop = ga.evolve_population(pop)

            # Print final results

            t1 = time()

            print("Finished")
            print("Final distance:", pop.get_fittest().get_distance())
            print("Solution:")
            solution = pop.get_fittest().get_raw_tour()
            print(solution)
            print("Took " + str(round(t1 - t0, 3)) + " seconds")

            # If we have the best tour so far
            if pop.get_fittest().get_distance() < best_distance:
                best_distance = pop.get_fittest().get_distance()
                best_solution = solution

                # Make output string
                output = "NAME = " + name + ",\nTOURSIZE = " + str(size) + ",\nLENGTH = " + str(pop.get_fittest().get_distance()) + ",\n"
                for i in range(len(solution)):
                    output += str(solution[i]) + ","

                # Remove the final comma
                output = output[:-1]

                print("\n---FILE OUTPUT---")
                print(output)
                print("---END OF FILE---")

                best_output = output

        t_11 = time()
        print()
        print("-----")
        print("BEST DISTANCE:", best_distance)
        print("BEST SOLUTION:", best_solution)
        print("TIME TAKEN:", str(round(t_11 - t_00, 3)) + " seconds")
        print("BEST OUTPUT:")
        print(best_output)
        print("-----")

        # output_file_name = file_name.split("/")[len(file_name.split("/")) - 1]
        output_file_name = sys.argv[2]
        f = open(output_file_name, "w")
        f.write(best_output)
        f.close()


if __name__ == "__main__":
    # list_of_files = [
    #     "duo_files/AISearchfile012.txt",
    #     "duo_files/AISearchfile017.txt",
    #     "duo_files/AISearchfile021.txt",
    #     "duo_files/AISearchfile026.txt"#,
    #     # "duo_files/AISearchfile042.txt",
    #     # "duo_files/AISearchfile048.txt",
    #     # "duo_files/AISearchfile058.txt",
    #     # "duo_files/AISearchfile175.txt",
    #     # "duo_files/AISearchfile180.txt",
    #     # "duo_files/AISearchfile535.txt"
    # ]
    # for x in list_of_files:
    print()
    print()
    print()
    print()
    print("###############################################################")
    print("###############################################################")
    print("###############################################################")
    print("###############################################################")
    print("###### WORKING ON " + sys.argv[1] + " ######")
    print("###############################################################")
    print("###############################################################")
    print("###############################################################")
    print("###############################################################")
    print("GA.MUTATION_RATE =", GA.MUTATION_RATE)
    print("###############################################################")
    print()
    tsp_ga = TSP_GA(sys.argv[1])