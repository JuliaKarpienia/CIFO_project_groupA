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
from Operators.mutations import single_player_swap_2teams, single_player_shift_all_teams, full_position_swap_2teams
from Operators.crossovers import crossover_swap_whole_position, crossover_swap_extreme_player
from Operators.selection import roulette_selection, tournament_selection, stochastic_selection
from Operators.population import *


sys.path.append(os.path.abspath(".."))

def get_best_ind(population):
    fitness_list = [calculate_fitness(team) for team in population if team is not None]
    return population[fitness_list.index(min(fitness_list))]

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
    filepath,
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
    convergence = []

    for gen in range(1, max_gen + 1):
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
                continue

            # Crossover or replication
            if random.random() < xo_prob:
                try:
                    offspring_pair = crossover(first_ind, second_ind)
                    if not offspring_pair or len(offspring_pair) != 2:
                        raise ValueError("Crossover failed or returned invalid offspring.")
                    offspring1, offspring2 = offspring_pair

                except Exception:            
                    offspring1, offspring2 = deepcopy(first_ind), deepcopy(second_ind)
            else:
                offspring1, offspring2 = deepcopy(first_ind), deepcopy(second_ind)
                

            # Mutation
            try:
                first_new_ind = mutation(offspring1, mut_prob)
                if first_new_ind is not None:
                    new_population.append(first_new_ind)
            except:
                pass

            if len(new_population) < len(population):
                try:
                    second_new_ind = mutation(offspring2, mut_prob)
                    if second_new_ind is not None:
                        new_population.append(second_new_ind)
                except:
                    pass

        population = new_population
        best_fitness = calculate_fitness(get_best_ind(population))
        convergence.append(best_fitness)

        if verbose:
            print(f"Gen {gen} best fitness: {best_fitness}")
    
    best_ind = get_best_ind(population)
    final_fitness = calculate_fitness(best_ind)

    return best_ind, final_fitness, convergence


def run_grid_search(param_grid, n_runs=30, max_gen=100, filepath = None, summary_path="ga_summary.csv", output_folder = 'fitness_logs'):
   

    if Path(summary_path).exists():
        Path(summary_path).unlink() 

    keys = list(param_grid.keys())
    values = (param_grid[key] for key in keys)
    param_combinations = list(product(*values))

    Path(output_folder).mkdir(parents=True, exist_ok=True)

    for param_values in tqdm(param_combinations, desc="Grid Search Progress", unit="config"):
        run_params = dict(zip(keys, param_values))
        fitnesses = []
        all_convergences = []

        for _ in range(n_runs):
            _, fitness, convergence = run_algorithm(**run_params, max_gen=max_gen, filepath=filepath)
            fitnesses.append(fitness)
            all_convergences.append(convergence)

        # Stats for csv file 
        stats = {
            "median_fitness": np.median(fitnesses),
            "mean_fitness": np.mean(fitnesses),
            "std_fitness": np.std(fitnesses),
            "min_fitness": np.min(fitnesses),
            "max_fitness": np.max(fitnesses),
        }

        summary_row = {
            **{k: (v.__name__ if callable(v) else v) for k, v in run_params.items()},
            **stats
        }

        df_new = pd.DataFrame([summary_row])
        file_exists = Path(summary_path).is_file()
        mode = "a" if file_exists else "w"
        df_new.to_csv(summary_path, mode=mode, header=not file_exists, index=False)

        # Prepare for convergence plot
        config_label = (
            f"POP={run_params['POP_SIZE']} "
            # f"GEN={run_params['max_gen']} "
            f"XO={run_params['xo_prob']} "
            f"mut_prob={run_params['mut_prob']} "
            f"mutation={run_params['mutation'].__name__} "
            f"crossover={run_params['crossover'].__name__} "
            f"selection_alg={run_params['selection_algorithm'].__name__} "
            f"elitism={run_params['elitism']}"
)
        convergence_df = pd.DataFrame(all_convergences)
        convergence_path = os.path.join(output_folder, f"{config_label}.csv")
        convergence_df.to_csv(convergence_path, index=False)

    print(f"\nSummary saved to: {summary_path}")
