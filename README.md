# CIFO_project_group_A Spring Semester 2024/2025

## Team Members

| Name            | Student Number |
| :-------------- | :------------- |
| Alexandra Pinto | 20211599       |
| Julia Karpienia | 20240514       |
| Steven Carlson  | 20240554       |
| Tim Straub      | 20240505       |

## Sports League Optimization using Genetic Algorithms (GA)

Project Report - [https://docs.google.com/document/d/1tOCk8Ioo5V9RKBLg4EZaCS4yO8WMUBOjNo7iBk_yAMM/edit?usp=sharing](Report Link)

### Problem definition

This project applies GA to solve an optimization problem in a fantasy spots league setting. The goal is to assign 35 players across 5 teams in a way that ensures:

* Balanced teams skill levels
* Valid team formation
* Salary cap compliance.

Each player is defined by their skill rating, salary and position (Goalkeeper, Defender, Midfielder or Forward).

### **Problem Constraints:**

* Each team must consist of: 1 Goalkeeper (GK), 2 Defenders (DEF), 2 Midfielders (MID) and 2 Forwards (FWD)
* Each player must be assigned to only one team
* Each team’s total salary cannot exceed a  750€ million total budget

If solution is not satysfying those constraints then it is then not a valid solution and the fitness value should reflect that

### **Objective**:

The objective is to **minimize** the skill imbalance between teams. To do so, the balanced league that satisfies all constraints and has the lowest standard deviation of average team skill levels is  created.

## Files Description

This repository is organized into several components, including test notebooks, core Python modules, and a main notebook that brings everything together. Below is an overview of each file and its purpose:

### Test Notebooks

These notebooks were used for experimenting with and evaluating the different genetic operators.This notebooks are inside the folder named Tests. After thorough testing, the finalized functions were moved to their respective Python modules.

- `test_crossovers.ipynb` — Experiments with different crossover strategies.
- `test_mutations.ipynb` — Tests and analyzes various mutation techniques.
- `test_selection.ipynb` — Evaluates multiple selection methods.

### Core Python Modules

These `.py` files contain the implementation of the Genetic Algorithm components used throughout the project. This notebooks are inside the folder named Operators.

- `crossovers.py` — Final crossover operator functions.
- `mutations.py` — Final mutation operator functions.
- `selection.py` — Final selection operator functions.
- `population.py` — Functions to initialize and manage the population.
- `genetic_algorithm.py` — Contains the main GA loop, result logging, and grid search functionality.
- `evaluation.py` — Tools to open and analyze grid search results, generate plots, and compute performance metrics and statistical tests.

### Main Notebooks

The main notebooks coordinate the full experimentation pipeline, including hyperparameter tuning through grid search and evaluation of the results. These notebooks are located in the root directory and serve as the central point for executing and analyzing GA configurations.

* `grid_search.ipynb` — This notebook performs a **grid search** over different combinations of genetic algorithm parameters (crossover probabilities, mutation rates, etc.). It uses the final operators and GA implementation to run multiple configurations and logs the performance of each.
* `evaluation_gs1.ipynb` — Contains the  **analysis of the first grid search (GS1)** . It includes convergence plots, best fitness tracking, and summary statistics to evaluate the performance of each configuration. Initial insights are drawn from early experiments and used to guide further tuning.
* `evaluation_gs2.ipynb` — A continuation of the evaluation process, focusing on the  **second, more refined grid search (GS2)** . It also provides a deeper statistical analysis, including Friedman and Nemenyi tests to determine significant performance differences across configurations. The best-performing setup is identified based on both effectiveness and robustness.

## How to Use

1. Clone the repository.
2. Run the notebooks inside `Tests` to understand how individual GA operators work.
3. Use `grid_search.ipynb` to run experiments with various parameter combinations.
4. Analyze the outcomes through `evaluation_gs1.ipynb` and `evaluation_gs2.ipynb`.
