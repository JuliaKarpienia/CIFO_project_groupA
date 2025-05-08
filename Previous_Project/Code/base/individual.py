import random


def valid_indiv(individual):
    """
        Function to check if an individual meets the necessary conditions to be valid
        --------
        Parameters:
            individual : list
                        List representing an individual.
        Returns:
            Boolean
                    True if individual is valid, False otherwise
        """
    # Check if each room is visited only once
    for i in [0,1,3,4,5,6,7]:
        if i not in individual:
            return False

    # Checking if there are no repeated individuals
    if len(set(individual)) != len(individual):
        return False

    # Check if the length is 8
    if len(individual) != 8:
        return False

    # Check if Room A is visited before Room F
    if individual.index(0) > individual.index(5):
        return False

    # Check if Room C is not in the list only if Room B is visited right after Room F
    if 99 in individual and individual.index(1) != individual.index(5)+1:
        return False

    # Check if Room H is the last room
    if individual[-1] != 7:
        return False

    return True


def create_indiv():
    """
        Creating an individual in the population
        --------
        Returns:
            list
                Individual of length 8, representing a path with rooms from A to H, in number format, starting in 0 until 7
        """

    individual = list(range(0, 7))
    # Shuffle the first 7 rooms (Room H needs to be the last one, so we do not shuffle it)
    random.shuffle(individual)
    individual.append(7)  #Appending 7 (room H) at the end

    if individual.index(1) == individual.index(5)+1:   # Checking if room B is seen right after room F
        # Set room C as optional
        if random.choice([True, False]):
            individual[individual.index(2)] = 99
            # population_set.append(sol_i)
    return individual


def create_pop(population_size):
    """
        Function to create the population
        --------
        Parameters:
            population_size : integer
                              Size of the population
        Returns:
            list
                List of lists, with each list representing an individual
        """
    population = []   # Initializing an empty list, where we will put our individuals to form a population

    while len(population) < population_size:  # Making sure it has the necessary size
        individual = create_indiv()
        if valid_indiv(individual):   # Confirming that only valid individuals are part of the population
            population.append(individual)

    return population


def calculate_individual_fitness(individual, focus_loss):
    """
        Calculates the fitness of an individual, based on the loss of focus from room to room
        --------
        Parameters:
            individual : list
                        List representing a path, with rooms represented as numbers from 0 to 7 (A to H).
            focus_loss : list
                        List with our data, that has the losses of focus from room to room.
        Returns:
            list
                Fitness of an individual, in percentage
        """
    fitness_score = 0   # This is the initial fitness score of any solution, as it cannot be higher than 100%

    for room in range(len(individual) - 1):
        room1 = individual[room]       # Defining the first room
        room2 = individual[room + 1]   # Getting the next room
        if room1 == 99:  # If room1 is 99, it means C is not in the list, so we do not need to calculate that focus loss
            continue     # so we move to the next iteration

        if room2 == 99:   # If the second room is 99, meaning that C is not accessed, we need to skip to the next room
            if room + 2 < len(individual):    # Checking if there are any rooms after the current room2
                room2 = individual[room + 2]  # Updating room2 with the correct value, as 99 needs to be skipped
            else:
                break   # Breaking out of the loop because there are no more rooms to consider after the current room2

        fitness_score += focus_loss[room1][room2]   # Subtracting the loss of focus in each iteration

    if not valid_indiv(individual):  # If we have a valid individual, we do not want it to continue in the next generations
        fitness_score = 150           # So a very high fitness is attributed

    return round(fitness_score, 1)


def calculate_pop_fit(focus_loss):
    """
    Calculates the fitness of each individual in the population.
    --------
    Parameters:
        focus_loss : list
                    List with our data, that has the losses of focus from room to room.
    Returns:
        list
            Fitness for each element in the population.
    """

    # Using a nested functions to avoid passing focus loss as a parameter for the GA
    def inner_calculate_pop_fit(population):

        fitness_scores = []   # Initializing hte list that will store the fitness values
        for individual in population:
            fitness_score = calculate_individual_fitness(individual, focus_loss)   # Calculating each individual fitness
            fitness_scores.append(fitness_score)   # Appending each score to the list with all the fitness values in the population
        return fitness_scores

    return inner_calculate_pop_fit

