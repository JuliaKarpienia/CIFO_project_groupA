import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os 
from pathlib import Path
from scipy.stats import friedmanchisquare
import scikit_posthocs as sp

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

    fig = plt.figure(figsize=(22, 20))
    gs = fig.add_gridspec(nrows=2, ncols=1, height_ratios=[9, 1]) 

    ax = fig.add_subplot(gs[0])
    handles, labels = [], []

    for config_name, df in fitness_dfs.items():
        median_fitness = df.median(axis=0)
        x = range(df.shape[1])

        line, = ax.plot(x, median_fitness.values, label=config_name)
        handles.append(line)
        labels.append(config_name)

    ax.set_title("Median Fitness Across Generations")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.grid(True)


    legend_ax = fig.add_subplot(gs[1])
    legend_ax.axis('off')  
    legend_ax.legend(
        handles,
        labels,
        loc='center',
        ncol=4,  
        frameon=True,
        fontsize='small'
    )

    plt.tight_layout()
    plt.show()


def plot_median_fitness_by_operator(folder_path="fitness_logs"):
    crossover_medians = {}
    mutation_medians = {}
    selection_medians = {}

    for file in Path(folder_path).glob("*.csv"):
        config_name = file.stem
        df = pd.read_csv(file)
        median_curve = df.median(axis=0).values

      
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
    

def plot_top_configs(summary_path="ga_summary.csv",
                     fitness_log_folder="fitness_logs",
                     top_n=5,
                     metric="median_fitness"):
    """
    Plot convergence curves of top configurations based on a selected metric.

    Parameters:
    - summary_path (str): Path to ga_summary.csv
    - fitness_log_folder (str): Path to folder with individual convergence .csvs
    - top_n (int): Number of top configurations to plot
    - metric (str): One of 'median_fitness', 'mean_fitness', 'std_fitness', 'min_fitness', 'max_fitness'
    """

    assert metric in ["median_fitness", "mean_fitness", "std_fitness", "min_fitness", "max_fitness"], \
        f"Invalid metric '{metric}'."

    summary_df = pd.read_csv(summary_path)

    if metric == "std_fitness":
        top_configs = summary_df.nsmallest(top_n, metric)  
    else:
        top_configs = summary_df.nsmallest(top_n, metric)  

    plt.figure(figsize=(20, 10))
    handles, labels = [], []

    for _, row in top_configs.iterrows():
        config_label = (
            f"POP={row['POP_SIZE']} "
            f"XO={row['xo_prob']} "
            f"mut_prob={row['mut_prob']} "
            f"mutation={row['mutation']} "
            f"crossover={row['crossover']} "
            f"selection_alg={row['selection_algorithm']} "
            f"elitism={row['elitism']}"
        )

        filepath = Path(fitness_log_folder) / f"{config_label}.csv"
        if filepath.exists():
            df = pd.read_csv(filepath)
            curve = df.median(axis=0) if metric == "median_fitness" else df.mean(axis=0)
            line, = plt.plot(curve.values, label=config_label, linewidth=2)
            handles.append(line)
            labels.append(config_label)
        else:
            print(f"Missing file: {filepath}")

    plt.title(f"{metric.replace('_', ' ').capitalize()} of Top {top_n} Configurations")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.grid(True)
    plt.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, -0.2),
               ncol=1 if top_n <= 3 else 2, fontsize="small", frameon=True)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.3)
    plt.show()


def plot_best_fitness_boxplot(fitness_folder="fitness_logs", title="Best Fitness Distribution (Per Run)"):
    data = []

    for file in Path(fitness_folder).glob("*.csv"):
        config_label = file.stem
        df = pd.read_csv(file)


        best_per_run = df.min(axis=1).values

        for value in best_per_run:
            data.append({
                'value': value,
                'group': config_label
            })

    df_long = pd.DataFrame(data)


    sns.set_theme(style="whitegrid", palette="pastel", font_scale=1.2)

    plt.figure(figsize=(14, 8))
    ax = sns.boxplot(x='group', y='value', data=df_long, width=0.5, linewidth=2.5, fliersize=4)

    plt.title(title, fontsize=16)
    plt.ylabel("Best Fitness Found in Run", fontsize=14)
    plt.xlabel("Configuration", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()



# Statistical tests 


# Running friedman test on best fitness from each run
def run_friedman_test_on_best_fitness(fitness_dfs: dict):
    """
    Run Friedman test across all loaded configurations using the best (lowest) fitness
    achieved in each run, not just the last generation.
    """
    best_fitnesses = []
    labels = []

    for config_label, df in fitness_dfs.items():
        if df.shape[0] != 30:
            print(f"Skipping {config_label}: only {df.shape[0]} runs (expected 30)")
            continue
        
        # Get the best (min) fitness from each run 
        best_per_run = df.min(axis=1)
        best_fitnesses.append(best_per_run)
        labels.append(config_label)


    # Run the Friedman test
    stat, p_value = friedmanchisquare(*best_fitnesses)

    print("\nFriedman Test Results:")
    print(f"Test Statistic: {stat:.4f}")
    print(f"P-value:        {p_value:.4f}")
    if p_value < 0.05:
        print("Significant difference detected between configurations (reject H₀)")
    else:
        print("No significant difference detected (fail to reject H₀)")

    return labels, best_fitnesses

## Post hoc  - nemenyi test

def run_posthoc_nemenyi_from_best_fitness(labels, best_fitnesses):
    """
    Perform post-hoc Nemenyi test using results from Friedman test (best fitness per run).
    """

    # Convert to DataFrame: rows = runs, columns = configurations
    df_scores = pd.DataFrame({label: scores for label, scores in zip(labels, best_fitnesses)})

    # Run Nemenyi post-hoc test
    posthoc = sp.posthoc_nemenyi_friedman(df_scores.values)

    # Label the matrix
    posthoc.index = labels
    posthoc.columns = labels

    print("\nPost-hoc Nemenyi Test (p-values):")
    print(posthoc.round(4))

    return posthoc

def plot_posthoc_heatmap(posthoc_df, title="Post-hoc Nemenyi Test (p-values)"):
    plt.figure(figsize=(10, 8))
    sns.heatmap(posthoc_df, annot=True, cmap="coolwarm", fmt=".3f", linewidths=0.5)
    plt.title(title)
    plt.tight_layout()
    plt.show()


def summarize_significant_wins(posthoc_df: pd.DataFrame, alpha=0.05):
    """
    Create a summary DataFrame showing how many configurations each one significantly outperforms.
    
    Parameters:
    - posthoc_df: DataFrame of p-values from a post-hoc Nemenyi test
    - alpha: significance threshold

    Returns:
    - summary DataFrame sorted by number of wins
    """
    summary = pd.DataFrame(index=posthoc_df.index, columns=["Significant Wins"])

    for config in posthoc_df.index:
        significant_wins = (posthoc_df.loc[config] < alpha).sum()
        summary.loc[config, "Significant Wins"] = significant_wins

    summary["Significant Wins"] = summary["Significant Wins"].astype(int)
    return summary.sort_values(by="Significant Wins", ascending=False)



