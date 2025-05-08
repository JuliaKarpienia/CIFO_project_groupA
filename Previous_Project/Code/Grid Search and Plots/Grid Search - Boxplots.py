import itertools
from operators.crossovers import *
from operators.mutators import *
from operators.selectors import *
from base.individual import *
from algorithm.algorithm import GA
import numpy as np
from base.data import *
import matplotlib.pyplot as plt

pop_size = 50
p_m = 0.1
p_c = 0.9
crossover_operators = [pmx_crossover, improved_cycle_crossover, ordered_crossover, fog_crossover, slide_crossover]
mutation_operators = [twors_mutation, reverse_sequence_mutation, inverted_exchange_mutation,
                      partial_shuffle_mutation]
gens_values = [100, 200]

# The seeds will be used to make sure that the results can be replicated
seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

##################################################################################################################
# ------------------------------- Box-plots for Crossover and Mutation Operators ---------------------------------

for gens in gens_values:
    # Initializing the necessary variables
    best_solution = None
    best_fitness = float('inf')  # Initializing with infinity, so that we can never find a higher value
    best_parameters = None
    fitness_scores_dict = {}  # Dictionary to store a combination and its corresponding value
    median_fitness_dict = {}  # Dictionary to store the median of fitness values for each combination

    for iteration_seed in range(1, len(seeds) + 1):
        fl = random_focus_gen(seed=iteration_seed)
        fit_foc_loss = calculate_pop_fit(fl)

        for crossover_op, mutation_op in itertools.product(crossover_operators, mutation_operators):
            population, fitness_scores = GA(create_population=create_pop,
                                            evaluate_population=fit_foc_loss,
                                            maximization=False,
                                            gens=gens,
                                            pop_size=pop_size,
                                            selector=roulette_selection,
                                            mutator=mutation_op,
                                            crossover_operator=crossover_op,
                                            p_c=p_c,
                                            p_m=p_m,
                                            elitism=True,
                                            verbose=False,
                                            log=False,
                                            path=None, seed=iteration_seed)

            # Showing each combination at each iteration
            print(f"Run {iteration_seed}. Combination: {crossover_op}, {mutation_op}, {gens}")

            # Find the best solution and fitness value in the current population
            min_fitness = min(fitness_scores)
            min_index = fitness_scores.index(min_fitness)
            solution = population[min_index]

            # Check if the current solution is the best so far
            if min_fitness < best_fitness:
                best_fitness = min_fitness
                best_solution = solution
                best_parameters = (crossover_op, mutation_op)

            # Storing parameter combinations
            param_combination = (crossover_op.__name__, mutation_op.__name__, gens)
            if param_combination not in fitness_scores_dict:  # Checking if the combination is already in the dictionary
                fitness_scores_dict[param_combination] = []
            fitness_scores_dict[param_combination].append(min_fitness)  # Appending the values to the dictionary

    for param_combination, fitness_scores in fitness_scores_dict.items():
        median_fitness = np.median(fitness_scores)
        median_fitness_dict[param_combination] = median_fitness  # Associating to each combination the corresponding median

    parameter_combinations = [str(combination) for combination in median_fitness_dict.keys()]
    # median_fitness_values = [median_fitness_dict[combination] for combination in median_fitness_dict.keys()]

    data = [fitness_scores_dict[combination] for combination in median_fitness_dict.keys()]

    # Creating the box-plots
    plt.figure()
    plt.boxplot(data, labels=parameter_combinations, vert=False)  # Vert = False so that the box-plots are horizontal
    plt.xlabel('Parameter Combination')
    plt.ylabel('Fitness')
    plt.title('Fitness Distribution for Each Parameter Combination')
    plt.xticks(rotation=45)
    plt.show()
