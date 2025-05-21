import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os 
from pathlib import Path
from scipy.stats import friedmanchisquare



# Loading the data from csv files

def load_fitness_logs(folder_path="fitness_logs"):
    """
    Load all .csv files from the given folder and organize them into a dictionary
    where keys are configuration names and values are DataFrames (30xN generations).
    """
    fitness_dfs = {}

    for file in Path(folder_path).glob("*.csv"):
        config_name = file.stem  # filename without extension
        df = pd.read_csv(file)
        fitness_dfs[config_name] = df

    print(f"Loaded {len(fitness_dfs)} configurations from '{folder_path}'")
    return fitness_dfs

# Plots 

def plot_median_fitness_over_gen(fitness_dfs: dict[str, pd.DataFrame]):
    sns.set(style="whitegrid", font_scale=1.2)
    fig, ax = plt.subplots(figsize=(14, 8))
    handles, labels = [], []

    for config_name, df in fitness_dfs.items():
        median_fitness = df.median(axis=0)
        x = range(df.shape[1])  # Numeric generations

        line, = ax.plot(x, median_fitness.values, label=config_name)
        handles.append(line)
        labels.append(config_name)

    ax.set_title("Median Fitness Across Generations")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.grid(True)

    legend = fig.legend(
        handles,
        labels,
        loc='lower center',
        bbox_to_anchor=(0.5, -0.2),
        ncol=2,
        frameon=True,
        borderpad=1
    )

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.25)
    plt.show()



def plot_median_fitness_by_operator(folder_path="fitness_logs"):
    crossover_medians = {}
    mutation_medians = {}
    selection_medians = {}

    for file in Path(folder_path).glob("*.csv"):
        config_name = file.stem
        df = pd.read_csv(file)
        median_curve = df.median(axis=0).values

        # Extract hyperparameters from filename
        parts = config_name.split()
        crossover = [p.split('=')[1] for p in parts if "crossover" in p][0]
        mutation = [p.split('=')[1] for p in parts if "mutation" in p][0]
        selection = [p.split('=')[1] for p in parts if "selection_alg" in p][0]

        crossover_medians.setdefault(crossover, []).append(median_curve)
        mutation_medians.setdefault(mutation, []).append(median_curve)
        selection_medians.setdefault(selection, []).append(median_curve)

    # Convert to median-of-medians
    crossover_curves = {k: pd.DataFrame(v).median(axis=0) for k, v in crossover_medians.items()}
    mutation_curves = {k: pd.DataFrame(v).median(axis=0) for k, v in mutation_medians.items()}
    selection_curves = {k: pd.DataFrame(v).median(axis=0) for k, v in selection_medians.items()}

    # Plot crossover
    plt.figure(figsize=(10, 5))
    for name, curve in crossover_curves.items():
        plt.plot(curve.index, curve.values, label=name)
    plt.title("Median Fitness by Crossover Operator")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(title="Crossover")
    plt.grid(True)
    plt.show()

    # Plot mutation
    plt.figure(figsize=(10, 5))
    for name, curve in mutation_curves.items():
        plt.plot(curve.index, curve.values, label=name)
    plt.title("Median Fitness by Mutation Operator")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(title="Mutation")
    plt.grid(True)
    plt.show()

    # Plot selection
    plt.figure(figsize=(10, 5))
    for name, curve in selection_curves.items():
        plt.plot(curve.index, curve.values, label=name)
    plt.title("Median Fitness by Selection Operator")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(title="Selection")
    plt.grid(True)
    plt.show()


# Statistical tests 

def run_friedman_test_on_final_fitness(fitness_dfs: dict):
    """
    Run Friedman test across all loaded configurations using final generation fitness
    from each run (i.e. last column in each CSV).
    """
    final_fitnesses = []
    labels = []

    for config_label, df in fitness_dfs.items():
        if df.shape[0] != 30:
            print(f"⚠️ Skipping {config_label}: only {df.shape[0]} runs (expected 30)")
            continue
        final_gen_fitness = df.iloc[:, -1]  # last generation column
        final_fitnesses.append(final_gen_fitness)
        labels.append(config_label)

    if len(final_fitnesses) < 2:
        print("Not enough configurations with valid data to run Friedman test.")
        return

    # Run the Friedman test
    stat, p_value = friedmanchisquare(*final_fitnesses)

    print("\nFriedman Test Results:")
    print(f"Test Statistic: {stat:.4f}")
    print(f"P-value:        {p_value:.4f}")
    if p_value < 0.05:
        print("Significant difference detected between configurations (reject H₀)")
    else:
        print("No significant difference detected (fail to reject H₀)")

    return labels, final_fitnesses