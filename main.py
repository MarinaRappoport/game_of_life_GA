import tkinter
from gui import TimerUpdate, Gui

from board import Board, MAX_BOARD_WIDTH
from genetic_algo import create_random_population, MAX_GENERATIONS, calculate_population_fitness, POPULATION_SIZE, \
    MAX_GENERATIONS_WITHOUT_IMPROVEMENT, ELITISM_SELECTION, crossover, mutate, \
    BOUNDING_BOX_HEIGHT, BOUNDING_BOX_WIDTH, roulette_wheel_parent_selection

# for statistics
STATS_FITNESS_MAX = []
STATS_FITNESS_MIN = []
STATS_FITNESS_AVG = []

MAX_STEPS_TO_EVOLVE = 500


# ------------ MAIN ---------------
def main():
    """Main function to for pattern creation with genetic algorithm"""
    population = create_random_population()
    no_improvements_counter = 0
    best_fitness = 0
    best_chromosome = population[0]
    best_board = Board(best_chromosome, BOUNDING_BOX_WIDTH)
    for generation in range(0, MAX_GENERATIONS):
        population_fitness_sorted, fitness_sum = calculate_population_fitness(population)
        fitness_max = population_fitness_sorted[-1][1]

        # statistics
        STATS_FITNESS_MAX.append(fitness_max)
        STATS_FITNESS_MIN.append(population_fitness_sorted[0][1])
        STATS_FITNESS_AVG.append(fitness_sum / POPULATION_SIZE)

        if fitness_max > best_fitness:
            no_improvements_counter = 1
            best_fitness = fitness_max
            best_chromosome = population_fitness_sorted[-1][0]
            best_board = population_fitness_sorted[-1][2]
        else:
            no_improvements_counter += 1

        print("Generation {} \tBest fitness: {}\tBest pattern max_size: {}\tBest pattern lifespan: {}"
              .format(generation + 1, best_fitness, best_board.max_config_size, best_board.lifespan))
        print("Best chromosome: {}".format(best_chromosome))

        if no_improvements_counter >= MAX_GENERATIONS_WITHOUT_IMPROVEMENT:
            print("{} generations without improvements. Will stop".format(no_improvements_counter))
            break

        # create next population
        population_new = []
        # 1. elitism selection
        for i in range(ELITISM_SELECTION):
            population_new.append(population_fitness_sorted[POPULATION_SIZE - 1 - i][0])

        # 2. crossover
        for _ in range(int(POPULATION_SIZE / 2)):
            parent1 = roulette_wheel_parent_selection(population_fitness_sorted, fitness_sum)
            parent2 = roulette_wheel_parent_selection(population_fitness_sorted, fitness_sum)
            # parent1 = rank_parent_selection(population_fitness_sorted)
            # parent2 = rank_parent_selection(population_fitness_sorted)
            child1, child2 = crossover(parent1, parent2)
            population_new.append(mutate(child1))
            if len(population_new) == POPULATION_SIZE:
                break
            population_new.append(mutate(child2))
            if len(population_new) == POPULATION_SIZE:
                break

        population = population_new

    #  print the winner
    print("Total generations {}".format(generation + 1))
    print("Best chromosome {}".format(best_chromosome))
    best_board.print_pattern()
    print("Evolving the best pattern up to {} steps...".format(MAX_STEPS_TO_EVOLVE))
    best_board.evolve(MAX_STEPS_TO_EVOLVE)
    best_board.print_data()
    board = Board(best_chromosome, BOUNDING_BOX_WIDTH)
    gui = Gui(board, best_board.lifespan, int(MAX_BOARD_WIDTH / 2))
    tkinter.Button(text="Start", command=lambda: TimerUpdate(gui)).pack()
    gui.window.mainloop()

    #  print stats to files
    file_name = "bb{}X{}_population{}".format(BOUNDING_BOX_HEIGHT, BOUNDING_BOX_WIDTH, POPULATION_SIZE)
    with open('{}_max.txt'.format(file_name), 'w') as f:
        for n in STATS_FITNESS_MAX:
            f.write("{}\n".format(n))
    with open('{}_min.txt'.format(file_name), 'w') as f:
        for n in STATS_FITNESS_MIN:
            f.write("{}\n".format(n))
    with open('{}_avg.txt'.format(file_name), 'w') as f:
        for n in STATS_FITNESS_AVG:
            f.write("{}\n".format(n))


if __name__ == "__main__":
    main()
