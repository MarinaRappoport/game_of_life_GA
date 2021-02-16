import math
import operator
import random

import numpy as np

from board import Board

# configuration of automate
BOUNDING_BOX_WIDTH = 6
BOUNDING_BOX_HEIGHT = 6
PROBABILITY_OF_LIVE = 0.2

# configuration of genetic algorithm
POPULATION_SIZE = 10
MAX_GENERATIONS = 30
MAX_GENERATIONS_WITHOUT_IMPROVEMENT = 4
MUTATION_PROBABILITY = 0.8
ELITISM_SELECTION = math.ceil(POPULATION_SIZE * 0.05)

# fintess configuration
LIFESPAN_FITNESS = 1
GROWTH_FITNESS = 1
MAX_GROWTH_FITNESS = 2
STEPS_TO_EVOLVE = 100


# -------------- UTILS ------------------------
def generate_random_chromosome():
    """Creates a random binary chromosome of specific size with probability of 1 = PROBABILITY_OF_LIVE"""
    return np.random.choice(a=[1, 0], size=(BOUNDING_BOX_HEIGHT * BOUNDING_BOX_WIDTH),
                            p=[PROBABILITY_OF_LIVE, 1 - PROBABILITY_OF_LIVE])


def create_random_population():
    """Creates a random population"""
    return [generate_random_chromosome() for _ in range(POPULATION_SIZE)]


def calculate_population_fitness(population):
    """ Calculates fitness for each member of population"""
    fitness_sum = 0
    population_fitness_list = []
    for chromosome in population:
        board, fitness = calculate_fitness(chromosome)
        population_fitness_list.append((chromosome, fitness, board))
        fitness_sum += fitness
    population_fitness_list.sort(key=operator.itemgetter(1))
    return population_fitness_list, fitness_sum


def calculate_fitness(chromosome):
    """Calculates the fitness of a chromosome"""
    board = Board(chromosome, BOUNDING_BOX_WIDTH)
    board.evolve(STEPS_TO_EVOLVE)
    return board, board.lifespan * LIFESPAN_FITNESS + (board.current_config_size - board.init_config_size) * MAX_GROWTH_FITNESS\
           +board.current_config_size * GROWTH_FITNESS


def mutate(chromosome):
    """ mutation function - flip random gen"""
    if random.random() < MUTATION_PROBABILITY:
        point = random.randint(0, len(chromosome) - 1)
        chromosome[point] = 1 if chromosome[point] == 0 else 0
    return chromosome


def crossover(chromosome1, chromosome2):
    """crossover function"""
    point = random.randint(0, len(chromosome1) - 1)
    return np.concatenate((chromosome1[:point], chromosome2[point:]), axis=0), \
           np.concatenate((chromosome2[:point], chromosome1[point:]), axis=0)


def roulette_wheel_parent_selection(population_fitness_sorted, fitness_sum):
    """ found parent for next crossover by roulette wheel selection"""
    n = random.uniform(0, fitness_sum)
    for chromosome, fitness, _ in population_fitness_sorted:
        if n < fitness:
            return chromosome
        n -= fitness


def rank_parent_selection(population_fitness_sorted):
    """ found parent for next crossover by rank selection"""
    rank_list = []
    current_rank = 1
    sum_rank = 0
    for chromosome, fitness, _ in population_fitness_sorted:
        rank_list.append((current_rank, chromosome))
        sum_rank = sum_rank + current_rank
        current_rank += 1
    n = random.uniform(0, sum_rank)
    for rank, chromosome in rank_list:
        if n < rank:
            return chromosome
        n -= rank
