# -- File: genetic_algorithm.py --
# Author: vzbf32
# Creation Date: 2017-12-18 23:40
# Purpose: This script performs a genetic algorithm on city data to find optimum tours.

import read_tour
import random

tour_data, name, size, cities = read_tour.get_cities("duo_files/AISearchfile012.txt")
# print(tour_data, name, size, cities)


# The below code is adapted from
# http://www.theprojectspot.com/tutorial-post/creating-a-genetic-algorithm-for-beginners/3
# accessed 2017-12-19


class Population:
    # individuals = []

    def __init__(self, population_size: int, initialise: bool):
        """
        Create a population.
        :param population_size: Size of population
        :param initialise: Whether to initialise the population
        """
        self.individuals = [None for i in range(population_size)]
        # Loop and create individuals
        if initialise:
            for i in range(self.size()):
                new_individual = Individual()
                new_individual.generate_individual()
                self.save_individual(i, new_individual)
        #[print(self.individuals[i]) for i in range(len(self.individuals))]

    def get_individual(self, index):
        return self.individuals[index]

    def get_fittest(self):
        """

        :rtype: Individual
        """
        fittest = self.individuals[0]
        # Loop through individuals to find fittest
        for i in range(self.size()):
            if fittest.get_fitness() <= self.get_individual(i).get_fitness():
                fittest = self.get_individual(i)
        return fittest

    def size(self):
        """
        Get population size
        :return: population size
        """
        return len(self.individuals)

    def save_individual(self, index: int, indiv):
        """
        Saves an individual to the population.
        :param index: Index to save to
        :param indiv: Individual to save
        :return:
        """
        self.individuals[index] = indiv


class Individual:
        DEFAULT_GENE_LENGTH = 64
        #genes = [None for i in range(DEFAULT_GENE_LENGTH)]
        # Cache
        #fitness = 0

        def __init__(self):
            self.genes = [None for i in range(self.DEFAULT_GENE_LENGTH)]
            self.fitness = 0

        def generate_individual(self):
            """
            Create a random individual.
            :return:
            """
            for i in range(self.size()):
                gene = int(round(random.random()))
                self.genes[i] = gene

        def set_default_gene_length(self, length):
            """
            Use this if you want to create individuals with different gene lengths.
            :param length:
            :return:
            """
            self.DEFAULT_GENE_LENGTH = length

        def get_gene(self, index):
            return self.genes[index]

        def set_gene(self, index, value):
            self.genes[index] = value
            fitness = 0

        def size(self):
            return len(self.genes)

        def get_fitness(self):
            f = FitnessCalc()
            if self.fitness == 0:
                self.fitness = f.get_fitness(self)
            return self.fitness

        def __str__(self):
            gene_string = ""
            for i in range(self.size()):
                gene_string += str(self.get_gene(i))
            return gene_string


class FitnessCalc:
    solution = [0 for i in range(64)]

    def set_solution(self, new_solution):
        """
        Set a candidate solution as list of 1s and 0s
        :param new_solution:
        :return:
        """
        if type(new_solution) == list:
            self.solution = new_solution
        elif type(new_solution) == str:
            for i in range(len(new_solution)):
                character = new_solution[i:i+1]
                if character == "0" or character == "1":
                    # self.solution[i] = int(character)
                    FitnessCalc.solution[i] = int(character)
                else:
                    # self.solution[i] = 0
                    FitnessCalc.solution[i] = 0

    def get_fitness(self, individual):
        """
        Calculate an individual's fitness by comparing it to our candidate solution
        :param individual:
        :return:
        """
        fitness = 0
        # Loop through our individual's genes and compare them to our candidate's genes
        for i in range(min(individual.size(), len(self.solution))):
            if individual.get_gene(i) == self.solution[i]:
                fitness += 1
        return fitness

    def get_max_fitness(self):
        max_fitness = len(self.solution)
        return max_fitness


class Algorithm:
    UNIFORM_RATE = 0.5
    MUTATION_RATE = 0.015
    TOURNAMENT_SIZE = 5
    ELITISM = True

    def evolve_population(self, pop):
        """
        Evolve a population
        :param pop: The population to evolve
        :return:
        """
        new_population = Population(pop.size(), False)

        # Keep our best individual
        if self.ELITISM:
            new_population.save_individual(0, pop.get_fittest())

        # Crossover population
        # elitism_offset = -1
        if self.ELITISM:
            elitism_offset = 1
        else:
            elitism_offset = 0

        # Loop over the population size and create new individuals with crossover
        for i in range(elitism_offset, pop.size()):
            indiv1 = self.tournament_selection(pop)
            indiv2 = self.tournament_selection(pop)
            new_indiv = self.crossover(indiv1, indiv2)
            new_population.save_individual(i, new_indiv)

        # Mutate population
        for j in range(elitism_offset, new_population.size()):
            # print(new_population.get_individual(j))
            # new_population.save_individual(j, self.mutate(new_population.get_individual(j)))
            # print(new_population.get_individual(j))
            self.mutate(new_population.get_individual(i))

        return new_population

    def crossover(self, indiv1, indiv2):
        """
        Crossover individuals
        :param indiv1:
        :param indiv2:
        :return:
        """
        new_sol = Individual()
        # Loop through genes
        for i in range(indiv1.size()):
            # Crossover
            if random.random() <= self.UNIFORM_RATE:
                new_sol.set_gene(i, indiv1.get_gene(i))
            else:
                new_sol.set_gene(i, indiv2.get_gene(i))
        return new_sol

    def mutate(self, indiv):
        """
        Mutate an individual.
        :param indiv:
        :return:
        """
        # Loop through genes
        for i in range(indiv.size()):
            if random.random() <= self.MUTATION_RATE:
                # Create random gene
                gene = int(round(random.random()))
                indiv.set_gene(i, gene)
        # print("Mutated to", indiv)
        # return indiv

    def tournament_selection(self, pop: Population) -> Individual:
        """
        Select individuals for crossover.
        :param pop:
        :return:
        """
        # Create a tournament population
        tournament = Population(self.TOURNAMENT_SIZE, False)
        # For each place in the tournament, get a random individual
        for i in range(self.TOURNAMENT_SIZE):
            random_id = int(random.random() * pop.size())
            tournament.save_individual(i, pop.get_individual(random_id))
        # Get the fittest
        fittest = tournament.get_fittest()
        return fittest


class GA:
    def __init__(self):
        # Set a candidate solution
        f = FitnessCalc()
        f.set_solution("1111000000000000000000000000000000000000000000000000000000001111")

        # Create an initial population
        my_pop = Population(50, True)

        # Evolve our population until we reach an optimum solution
        generation_count = 0
        a = Algorithm()
        while my_pop.get_fittest().get_fitness() < f.get_max_fitness():
            generation_count += 1
            print("Generation:", generation_count, "Fittest:", my_pop.get_fittest().get_fitness(), "Genes:", my_pop.get_fittest())
            my_pop = a.evolve_population(my_pop)
        print("Solution found!")
        print("Generation:", generation_count)
        print("Genes:", my_pop.get_fittest())


# If we are running this module directly
if __name__ == "__main__":
    ga = GA()
