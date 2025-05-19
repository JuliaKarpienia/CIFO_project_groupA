#System libraries
import sys
import os
from copy import deepcopy
from inspect import getsource
import pandas as pd
from pathlib import Path
from datetime import datetime
from filelock import FileLock
from itertools import product
from tqdm import tqdm


# Project libraries
from mutations import single_player_swap_2teams, single_player_shift_all_teams, full_position_swap_2teams
from crossovers import crossover_swap_whole_position, crossover_swap_extreme_player
from selection import roulette_selection, tournament_selection, stochastic_selection
from population import *


sys.path.append(os.path.abspath(".."))

def get_best_ind(population):
    fitness_list = [calculate_fitness(team) for team in population if team is not None]
    return population[fitness_list.index(min(fitness_list))]


def run_algorithm(
        filepath=r"..\Data\players(in).csv",
        POP_SIZE=50,
        max_gen=100,
        elitism=True,
        verbose=False,
        mutation = single_player_swap_2teams,
        mut_prob=0.2,
        #Options: single_player_swap_2teams, /
        # single_player_shift_all teams, /
        # full_position_swap_2teams
        crossover = crossover_swap_whole_position,
        xo_prob=0.8,
        #Options: crossover_swap_whole_position, /
        # preset_team_mix_crossover
        selection_algorithm = tournament_selection,
        #Options: roulette_selection, /
        # tournament_selection, /
        # stoachastic_seleciton
):
    # 1. Initialize a population with N individuals
    players = load_players_from_csv(filepath)
    population = generate_population(players, POP_SIZE)

    # 2. Repeat until termination condition
    for gen in range(1, max_gen + 1):
        if verbose:
            print(f'-------------- Generation: {gen} --------------')

        # 2.1. Create an empty population P'
        new_population = []

        # 2.2. If using elitism, insert best individual from P into P'
        if elitism:
            new_population.append(deepcopy(get_best_ind(population)))
        
        # 2.3. Repeat until P' contains N individuals
        while len(new_population) < len(population):
            # 2.3.1. Choose 2 individuals from P using a selection algorithm
            first_ind = selection_algorithm(population)
            second_ind = selection_algorithm(population)

            #if verbose:
                #print(f'Selected individuals:\n{first_ind}\n{second_ind}')

            # 2.3.2. Choose an operator between crossover and replication
            # 2.3.3. Apply the operator to generate the offspring
            if random.random() < xo_prob:
                offspring1, offspring2 = crossover(first_ind, second_ind)
                if verbose:
                    print(f'Applied {crossover}')
            else:
                offspring1, offspring2 = deepcopy(first_ind), deepcopy(second_ind)
                if verbose:
                    print(f'Applied replication')
            
            if verbose:
                print(f'Offspring:\n{offspring1}\n{offspring2}')
            
            # 2.3.4. Apply mutation to the offspring
            first_new_ind = mutation(offspring1, mut_prob)
            # 2.3.5. Insert the mutated individuals into P'
            new_population.append(first_new_ind)

            if verbose:
                print(f'First mutated individual: {first_new_ind}')
            
            if len(new_population) < len(population):
                second_new_ind = mutation(offspring2, mut_prob)
                new_population.append(second_new_ind)
                if verbose:
                    print(f'Second mutated individual: {first_new_ind}')
        
        # 2.4. Replace P with P'
        population = new_population
        
        # 2.5 . Calculate fitness for each individual in P
        # fitness_list = []
        # for team in population:
            # team.calculate_fitness()
            # fitness_list.append(team.fitness)
        
        # best_ind = min(fitness_list)
        # if verbose:
            # print(f'Final best individual in generation: {best_ind}')

    # 3. Return the best individual in P
    # return best_ind
        if verbose:
            print(f'Final best individual in generation: {get_best_ind(population)}')

    # 3. Return the best individual in P
    return get_best_ind(population)

def log_run_results(
    run_params: dict,
    best_fitness: float,
    csv_path: str = "ga_runs.csv"
) -> None:
    """
    Append one row (hyper-parameters + best_fitness + timestamp) to a CSV file.
    Creates the file with a header the first time it is called.

    Parameters
    ----------
    run_params    : dict   {parameter_name: value}
    best_fitness  : float  best fitness found in the run
    csv_path      : str    path to the CSV log file
    """
    # 1) Build a one-row DataFrame
    row = {**run_params,
           "best_fitness": best_fitness,
           "timestamp": datetime.now()}
    df_new = pd.DataFrame([row])

    # 2) Make sure the folder exists
    csv_path = Path(csv_path)
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    # 3) Simple file lock so parallel runs do not collide
    lock_path = csv_path.with_suffix(csv_path.suffix + ".lock")
    with FileLock(lock_path):
        file_exists = csv_path.is_file()
        mode = "a" if file_exists else "w"
        df_new.to_csv(
            csv_path,
            mode=mode,
            header=not file_exists,   # write header only once
            index=False
        )

def run_algorithm(
    filepath=r"../Data/players(in).csv",
    log_path="ga_runs.csv",
    POP_SIZE=50,
    max_gen=100,
    elitism=True,
    verbose=False,
    mutation=single_player_swap_2teams,
    mut_prob=0.2,
    crossover=crossover_swap_whole_position,
    xo_prob=0.8,
    selection_algorithm=tournament_selection
):

    players = load_players_from_csv(filepath)
    population = generate_population(players, POP_SIZE)

    for gen in range(1, max_gen + 1):
        if verbose:
            print(f'-------------- Generation: {gen} --------------')

        new_population = []

        # Elitism
        if elitism:
            try:
                best_ind = deepcopy(get_best_ind(population))
                if best_ind is not None:
                    new_population.append(best_ind)
            except Exception as e:
                if verbose:
                    print(f"Elitism skipped due to error: {e}")

        # Main GA loop
        while len(new_population) < len(population):
            first_ind = selection_algorithm(population)
            second_ind = selection_algorithm(population)

            if not first_ind or not second_ind:
                if verbose:
                    print("Selection returned None. Skipping.")
                continue

            # Crossover or replication
            if random.random() < xo_prob:
                try:
                    offspring_pair = crossover(first_ind, second_ind)
                    if not offspring_pair or len(offspring_pair) != 2:
                        raise ValueError("Crossover failed or returned invalid offspring.")
                    offspring1, offspring2 = offspring_pair
                    if verbose:
                        print(f'Applied {crossover}')
                except Exception as e:
                    if verbose:
                        print(f"Crossover failed: {e}. Using replication instead.")
                    offspring1, offspring2 = deepcopy(first_ind), deepcopy(second_ind)
            else:
                offspring1, offspring2 = deepcopy(first_ind), deepcopy(second_ind)
                if verbose:
                    print(f'Applied replication')

            # Mutation
            try:
                first_new_ind = mutation(offspring1, mut_prob)
                if first_new_ind is not None:
                    new_population.append(first_new_ind)
                    if verbose:
                        print(f'First mutated individual added.')
            except Exception as e:
                if verbose:
                    print(f"Mutation failed for first offspring: {e}")

            if len(new_population) < len(population):
                try:
                    second_new_ind = mutation(offspring2, mut_prob)
                    if second_new_ind is not None:
                        new_population.append(second_new_ind)
                        if verbose:
                            print(f'Second mutated individual added.')
                except Exception as e:
                    if verbose:
                        print(f"Mutation failed for second offspring: {e}")

        population = new_population

        if verbose:
            try:
                print(f'Final best individual in generation {gen}: {get_best_ind(population)}')
            except Exception as e:
                print(f"Could not evaluate best individual: {e}")
    
    best_ind = get_best_ind(population)
    best_fitness = calculate_fitness(best_ind)
    print(f'Final best individual: {best_ind}')
    print(f'Best fitness: {best_fitness}')

    # Log results
    run_params = {
    "POP_SIZE": POP_SIZE,
    "max_gen": max_gen,
    "elitism": elitism,
    "mut_prob": mut_prob,
    "xo_prob": xo_prob,
    "mutation": mutation.__name__,
    "crossover": crossover.__name__,
    "selection_algorithm": selection_algorithm.__name__
}
    log_run_results(run_params, best_fitness, csv_path="ga_runs.csv")

    return best_ind, best_fitness

def run_grid_search():
    # Define the parameter grid
    param_grid = {
        "POP_SIZE": [50, 100],
        "max_gen": [50, 100],
        "mut_prob": [0.1, 0.2, 0.3],
        "xo_prob": [0.7, 0.8, 0.9,],
        "mutation": [single_player_swap_2teams, single_player_shift_all_teams, full_position_swap_2teams],
        "crossover": [crossover_swap_whole_position, crossover_swap_extreme_player],
        "selection_algorithm": [roulette_selection, tournament_selection]
    }

    # Generate all combinations of parameters
    keys = list(param_grid.keys())
    values = (param_grid[key] for key in keys)
    param_combinations = list(product(*values))
    total_runs = len(param_combinations)

    # Progress bar using tqdm
    #print(f"Total combinations to run: {total_runs}")
    for i, params in enumerate(tqdm(param_combinations, desc="Grid Search Progress", unit="run")):
        run_params = dict(zip(keys, params))
        #print(f"\nRunning combination {i+1}/{total_runs}:")
        #for k, v in run_params.items():
            #print(f"  {k}: {v.__name__ if callable(v) else v}")
        run_algorithm(**run_params)



    
