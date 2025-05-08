import random


# Defining a function that performs a roulette wheel selection
def roulette_selection(population, fits):
    """
    Returns an individual from the population, after applying a roulette wheel selection
    --------
    Parameters:
        population : list
                    Matrix composed of individuals from a population
        fits : list
                List with values of fitness from all individuals in the population
    Returns:
        individual
                Individual chosen after performing the selection
    """
    sum_of_fits = sum(fits)  # Getting the total sum of fitness

    # Calculating the probabilities of each individual to be chosen
    probabilities = [1 - fitness / sum_of_fits for fitness in fits]
    # Returning the chosen individual, using the probabilities as weights, meaning that the higher the fitness
    # associated with an individual, the more likely it is for him to be chosen
    return random.choices(population, weights=probabilities)[0]

