import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os 


def load_fitness_dfs(folder_path="fitness_logs") -> dict:
    fitness_dfs = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            config_label = filename[:-4]  # Remove ".csv" extension
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)
            fitness_dfs[config_label] = df

    return fitness_dfs


def plot_median_fitness_over_gen(fitness_dfs: dict[str, pd.DataFrame]):
    sns.set(style="whitegrid", font_scale=1.2)
    fig, ax = plt.subplots(figsize=(10, 6))
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
