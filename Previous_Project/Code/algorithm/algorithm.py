import csv
import random
from copy import deepcopy
import numpy as np


def GA(create_population,
       evaluate_population,
       maximization,
       gens,
       pop_size,
       selector,
       mutator,
       crossover_operator,
       p_c,
       p_m,
       elitism,
       verbose,
       log,
       path,
       seed=None,
       return_convergence=False):    # Return converge will only be used to plot convergence

    """
    Returns the offspring after applying an improved cycle crossover

    Parameters:
    --------
        create_population : function
                    function that will create a population
        evaluate_population : function
                    function that will return the fitness of a population
        maximization : Boolean
                    Boolean value to indicate if it's a maximization (True) or minimization (False) problem.
        gens : integer
                    Number of generations for the algorithm
        pop_size : integer
                    Number indicating the size of a population
        selector : function
                    function to select individuals from the population
        mutator : function
                    function that performs mutation on an individual
        crossover_operator : function
                    function that performs crossover on two parents
        p_c : float
                    Number between 0 and 1 that indicates the probability of crossover happening
        p_m : float
                    Number between 0 and 1 that indicates the probability of crossover happening
        elitism : Boolean
                    Boolean that indicates if there should be elitism in the algorithm
        verbose : Boolean
                    Indicates if there should be information printed (True), or not (False), on each generation and
                    final solution
        log : Boolean
                    Indicates if the values at each generation should be stored in a csv file
        path : string
                    Path of the location of the csv file that will store fitness values of each generation
        seed : integer, default None
                    If indicated, it will help set the random.seed value, so that results can be replicated
        return_convergence : Boolean, default False
                    Indicates if fitness values at each iteration should be return. They can later be used for
                    convergence plots

    Returns:
    --------
        pop, fit_pop
            Lists with population and its fitness values
        convergence
            Only if return_convergence is True
            List with best fitness at each generation
    """

    if return_convergence:
        convergence = []     # Initializing the list to store convergence, in the case that it is needed

    if seed is not None:     # Adding a seed, if needed
        random.seed(seed)

    # Making sure that a path is provided if we want to log the results
    if log and path == None:
        raise Exception('If log is True then a valid path should be provided')

    # Creating the first population
    pop = create_population(population_size=pop_size)

    # Calculating population fitness
    fit_pop = evaluate_population(pop)

    for it in range(gens):

        off_pop = []   # Initializing the offspring list

        while len(off_pop) < len(pop):     # Repeating the process until we have a population of offspring of the same
            # size as the original

            p1, p2 = selector(pop, fit_pop), selector(pop, fit_pop)    # Selecting the parents

            if random.random() < p_c:   # See if a crossover is applied
                o1, o2 = crossover_operator(p1[:-1], p2[:-1])    # Getting the offspring from the crossover operator
                # We do not provide room H to the crossover operator since it always needs to be at the end
            else:
                o1, o2 = deepcopy(p1), deepcopy(p2)    # If crossover is not applied, copying parents to next population

            # Not providing the last room, as it needs to always be 7 (room H)
            o1, o2 = mutator(o1[:-1], p_m), mutator(o2[:-1], p_m)    # Applying mutation operator

            off_pop.extend([o1, o2])    # Adding the offspring to the new population

        if elitism:    # Passing the best individuals to the next generation, to avoid losing them, if elitism = True
            if maximization:
                off_pop[-1] = pop[np.argmax(fit_pop)]
            else:
                off_pop[-1] = pop[np.argmin(fit_pop)]

        pop = off_pop  # Replacing the old population with the new one

        fit_pop = evaluate_population(pop)    # Evaluating the new population

        if verbose:   # Print the best fitness at each generation if verbose

            if maximization:   # Case for maximization problem
                print(f'     {it}       |       {max(fit_pop)}      ')
                print('-' * 32)

            else:       # Case of minimization problem, which is our case
                print(f'     {it}       |       {min(fit_pop)}      ')
                print('-' * 32)

        if log:  # Storing the best results at each generation if log = True
            if maximization:
                with open(path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([it, max(fit_pop)])
            else:
                with open(path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([it, min(fit_pop)])

        if return_convergence:    # If convergence, appending the best fitness at each generation
            if maximization:
                convergence.append(max(fit_pop))
            else:
                convergence.append(min(fit_pop))

    if verbose:
        print('Final solution:', pop[fit_pop.index(min(fit_pop))])
        print('Best fitness:', min(fit_pop))

    if return_convergence:
        return pop, fit_pop, convergence
    else:
        return pop, fit_pop
