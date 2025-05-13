import random
from copy import deepcopy
import numpy as np
import builtins
from population import *

def roulette_selection(population: list[League]) -> League:
    """
    Select one League from population using roulette‐wheel selection
    (minimization problem ⇒ weight = 1 / fitness).
    Leagues with invalid fitness (9999) or zero/negative fitness get a tiny weight = less chance.
    """
    # 1) Compute fitness weights
    weights = []
    for league in population:
        f = calculate_fitness(league)
        if f <= 0 or f == 9999:
            weights.append(1e-7)
        else:
            weights.append(1 / f) # inverse fitness because we're minimizing

    # 2) Choose random number in [0, total_weight]
    total_weights = builtins.sum(weights)
    pick = random.uniform(0, total_weights)

    # 3) Check which league it lands on
    cumulative_weights = 0.0
    for league, w in zip(population, weights):
        cumulative_weights += w
        if pick <= cumulative_weights:
            return league

    # In case of rounding error, return the last one (fallback)
    return population[-1]


def tournament_selection(population: list[League], tournament_size: int = 3) -> League:
    """
    Select one League by running a 'tournament' among a random subset.
    The league with the lowest fitness (since we're minimizing) wins.
    """
    # 1) Randomly pick k competitors
    competitors = random.sample(population, k=tournament_size)
    # 2) Choose the best (min fitness)
    winner = min(competitors, key=calculate_fitness)
    return winner

def stochastic_selection(population: list[League], num_parents: int) -> list[League]:
    """
    Stochastic Universal Sampling for a minimization GA.
    Returns a list of num_parents selected Leagues.
    """
    # 1) Compute weights
    weights = []
    for league in population:
        f = calculate_fitness(league)
        if f <= 0 or f == 9999:
            weights.append(1e-7)       # invalid or zero
        else:
            weights.append(1 / f)      # inverse fitness

    total_weight = builtins.sum(weights)
    step = total_weight / num_parents

    # 2) Pick a random start in [0, step)
    start = random.uniform(0, step)
    pointers = [start + i * step for i in range(num_parents)]

    # 3) Sweep the wheel once
    selections = []
    cumulative = 0.0
    idx = 0
    for league, w in zip(population, weights):
        cumulative += w
        # Select for all pointers <= cumulative
        while idx < num_parents and pointers[idx] <= cumulative:
            selections.append(deepcopy(league))
            idx += 1
        if idx >= num_parents:
            break

    # 4) Fallback: if rounding left some pointers unassigned
    while len(selections) < num_parents:
        selections.append(deepcopy(population[-1]))

    return selections