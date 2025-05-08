# Importing the necessary libraries
from operators.crossovers import *
from operators.mutators import *
from operators.selectors import *
from base.individual import *
from algorithm.algorithm import *
import numpy as np
import matplotlib.pyplot as plt
import statistics
import itertools

# Dataset from project example
focus_loss = [[0, 10.2, 16, 4, 6, 12, 7.5, 9],
              [10.2, 0, 4.3, 8, 11, 2.2, 3, 11.5],
              [16, 4.3, 0, 9, 3, 6, 7, 5],
              [4, 8, 9, 0, 11, 10.5, 5, 2],
              [6, 11, 3, 11, 0, 9.8, 4, 10],
              [12, 2.2, 6, 10.5, 9.8, 0, 8, 8],
              [7.5, 3, 7, 5, 4, 8, 0, 10.1],
              [9, 11.5, 5, 2, 10, 8, 10.1, 0]]

# Parameters to be used, most are fixed and obtained by the general grid search. We are only studying the performance of
# each combination of crossovers and mutation operators in these plots
pop_size = 50
p_m = 0.1
p_c = 0.9
gens = 200
crossover_operators = [pmx_crossover, improved_cycle_crossover, ordered_crossover, fog_crossover, slide_crossover]
mutation_operators = [twors_mutation, reverse_sequence_mutation, inverted_exchange_mutation,
                      partial_shuffle_mutation]
fit_foc_loss = calculate_pop_fit(focus_loss)

# Initializing everything needed
medians = []  # List to store median fitnesses later
convergence_list = []  # List to store convergence values for each run
list_for_plots = []  # Initializing list to store all convergence values from all combinations and runs


##################################################################################################################
# ------------------------- Convergence plots for Crossover and Mutation Operators -------------------------------

for crossover_op, mutation_op in itertools.product(crossover_operators, mutation_operators):
    convergence_list = []
    for counter in range(1, 16):
        population, fitness_scores, convergence = GA(create_population=create_pop,
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
                                                     path=None, return_convergence=True)

        convergence_list.append(convergence)  # Appending each convergence list
        print(f"Operator: {crossover_op} {mutation_op}")
        print(f"Run: {counter}")
    list_for_plots.append(convergence_list)  # Appending each list of convergences, in the proper order


pointer = 0  # It's going to be used to access to each combination of parameters
for crossover_op in crossover_operators:
    for mutation_op in mutation_operators:
        transposed_lists = zip(*list_for_plots[pointer])  # Getting the transposed of each matrix inside list_for_
        # plots, so that we are then able to access the median for each generation across all the runs of the algorithm

        # Calculate the median for each generation, across all the runs and combinations
        medians = [statistics.median(elements) for elements in transposed_lists]

        generations = np.arange(1, gens + 1)  # Getting an array with all generations

        # Creating the convergence plots
        plt.figure()
        plt.title(f'Convergence Plot: {crossover_op.__name__}, {mutation_op.__name__}')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.plot(generations, medians, label='Median')
        plt.legend()
        plt.show()

        pointer += 1  # Increasing the pointer at each loop, so that we can access the next combination of parameters
        # on the next iteration
