# Importing the necessary libraries
import time
from operators.crossovers import *
from operators.mutators import *
from operators.selectors import *
from base.individual import *
from algorithm.algorithm import GA
import itertools
from base.data import *


# Defining parameters for the Grid Search
pop_size_values = [50, 100]
p_m_values = [0.1, 0.2, 0.35, 0.8, 0.9]
p_c_values = [0.1, 0.2, 0.35, 0.8, 0.9]
crossover_operators = [pmx_crossover, improved_cycle_crossover, ordered_crossover, fog_crossover, slide_crossover]
mutation_operators = [inverted_exchange_mutation, twors_mutation, reverse_sequence_mutation,
                      partial_shuffle_mutation]
gens_values = [100, 150, 200]

exec_dict = {}    # Dictionary to hold the combinations and their respective values

# Seeds to be used, to guarantee that the results can be replicated
seeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

# ----------------------------------------------- GRID SEARCH -------------------------------------------------------
for iteration_seed in range(1, len(seeds) + 1):
    fl = random_focus_gen(seed=iteration_seed)
    fit_foc_loss = calculate_pop_fit(fl)
    # Initializing variables that will be used in the Grid Search
    best_solution = None
    best_fitness = float('inf')  # Initializing with infinity, so that we can never find a higher value
    best_parameters = None
    best_execution_time = float('inf')

    for pop_size, p_m, p_c, crossover_op, mutation_op, gens \
            in itertools.product(pop_size_values, p_m_values, p_c_values, crossover_operators, mutation_operators,
                                 gens_values):
        # Measure execution time for the current combination
        start_time = time.time()

        # Run the genetic algorithm with the current parameters in the iteration
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
                                        path=None,
                                        seed=iteration_seed)

        end_time = time.time()
        execution_time = end_time - start_time   #Calculating the execution time for each combination

        # Find the best solution and fitness value in the current population
        min_fitness = min(fitness_scores)
        min_index = fitness_scores.index(min_fitness)
        solution = population[min_index]

        # Check if the current solution is the best so far
        if min_fitness < best_fitness:
            best_fitness = min_fitness
            best_solution = solution
            best_parameters = (pop_size, p_m, p_c, crossover_op, mutation_op, gens)

        # Check, in the case where fitness is repeated, if it has a better execution time
        elif min_fitness == best_fitness and execution_time < best_execution_time:
            best_solution = solution
            best_parameters = (pop_size, p_m, p_c, crossover_op, mutation_op, gens)
            best_execution_time = execution_time

        print(f"Run {iteration_seed}. Combination: {pop_size}, {p_m}, {p_c}, {crossover_op}, {mutation_op}, {gens}")
        print(f"Run {iteration_seed}.Execution Time: {execution_time:.2f} seconds")

    # Printing at each run, the best values found for that dataset
    print(f"Run {iteration_seed}. Best Solution: {best_solution}")
    print(f"Run {iteration_seed}. Best Fitness Score: {best_fitness}")
    print(f"Run {iteration_seed}. Best Parameters: {best_parameters}")
    print(f"Run {iteration_seed}. Best Parameters: {best_execution_time}")

    # Storing the values in a dictionary, so that they can be compared later
    if iteration_seed not in exec_dict:
        exec_dict[iteration_seed] = []

    exec_dict[iteration_seed].extend([best_parameters, best_fitness, best_solution, best_execution_time])

    print(exec_dict)  # Printing the execution dictionary, so that we can compare the results for each run


'''
Result of our Grid Search
exec_dict_final = 
            {1: [(50, 0.1, 0.35, slide_crossover, partial_shuffle_mutation, 100), 16.7, [0, 1, 4, 6, 2, 3, 5, 7], 0.14105820655822754], 
             2: [(50, 0.1, 0.8, slide_crossover, reverse_sequence_mutation, 100), 14.0, [4, 1, 0, 6, 5, 3, 2, 7], 0.14087557792663574], 
             3: [(50, 0.2, 0.35, slide_crossover, reverse_sequence_mutation, 100), 26.1, [3, 4, 0, 1, 6, 5, 2, 7], 0.1405487060546875], 
             4: [(50, 0.8, 0.8, slide_crossover, reverse_sequence_mutation, 100), 28.9, [1, 0, 3, 4, 6, 2, 5, 7], 0.10961651802062988], 
             5: [(50, 0.1, 0.9, improved_cycle_crossover, reverse_sequence_mutation, 100), 27.9, [1, 0, 4, 2, 6, 5, 3, 7], 0.08118581771850586], 
             6: [(50, 0.2, 0.1, slide_crossover, partial_shuffle_mutation, 100), 33.8, [0, 5, 1, 3, 2, 6, 4, 7], 0.0941464900970459], 
             7: [(50, 0.1, 0.9, fog_crossover, reverse_sequence_mutation, 100), 14.2, [0, 4, 2, 5, 6, 1, 3, 7], 0.09306764602661133], 
             8: [(50, 0.1, 0.35, slide_crossover, partial_shuffle_mutation, 100), 22.9, [1, 2, 6, 3, 0, 5, 4, 7], 0.09416723251342773], 
             9: [(50, 0.1, 0.9, fog_crossover, inverted_exchange_mutation, 100), 27.0, [3, 0, 5, 1, 2, 6, 4, 7], 0.09417605400085449], 
             10: [(50, 0.1, 0.35, improved_cycle_crossover, inversion_mutation, 100), 30.5, [0, 4, 5, 1, 2, 3, 6, 7], 0.09316897392272949], 
             11: [(50, 0.1, 0.9, fog_crossover, inverted_exchange_mutation, 100), 28.4, [2, 6, 1, 4, 0, 3, 5, 7], 0.0785977840423584], 
             12: [(50, 0.1, 0.1, ordered_crossover, partial_shuffle_mutation, 100), 26.6, [0, 4, 1, 3, 2, 6, 5, 7], 0.09399580955505371], 
             13: [(50, 0.1, 0.35, slide_crossover, reverse_sequence_mutation, 100), 23.7, [3, 4, 1, 2, 6, 0, 5, 7], 0.09403085708618164], 
             14: [(50, 0.1, 0.2, slide_crossover, partial_shuffle_mutation, 100), 31.6, [0, 6, 3, 2, 5, 1, 4, 7], 0.09116125106811523], 
             15: [(50, 0.2, 0.9, slide_crossover, reverse_sequence_mutation, 100), 19.3, [2, 3, 1, 6, 0, 5, 4, 7], 0.09403753280639648]}
'''
