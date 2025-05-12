
import random
from copy import deepcopy
import pandas as pd
import math

def load_players_from_csv(filepath):

    df = pd.read_csv(filepath)
    
    players = []
    for _, row in df.iterrows():
        player = {
            "name": row['Name'],
            "position": row['Position'],
            "skill":int(row['Skill']),
            "cost": float(row['Salary (€M)'])
        }
        players.append(player)
    return players


def create_initial_population(players, population_size=50, salary_cap=750):
    
    population = []

    GKs = [p for p in players if p['position'] == 'GK']
    DEFs = [p for p in players if p['position'] == 'DEF']
    MIDs = [p for p in players if p['position'] == 'MID']
    FWDs = [p for p in players if p['position'] == 'FWD']

    for _ in range(population_size):
        valid = False
        while not valid:
            used_player_names = set()
            teams = []
            random.shuffle(GKs)
            random.shuffle(DEFs)
            random.shuffle(MIDs)
            random.shuffle(FWDs)

            for _ in range(5):
                
                team_gk = [p for p in GKs if p['name'] not in used_player_names][:1]
                team_defs = [p for p in DEFs if p['name'] not in used_player_names][:2]
                team_mids = [p for p in MIDs if p['name'] not in used_player_names][:2]
                team_fwds = [p for p in FWDs if p['name'] not in used_player_names][:2]
                
                team = team_gk + team_defs + team_mids + team_fwds
                
                
                if len(team) != 7:
                    break 

                for player in team:
                    used_player_names.add(player['name'])
                
                teams.append(team)

            if len(teams) == 5:
                over_budget = False
                for team in teams:
                    team_cost = sum(p['cost'] for p in team)
                    if team_cost > salary_cap:
                        over_budget = True
                        break
                
                if not over_budget:
                    valid = True
                    population.append(deepcopy(teams))

    return population

def calculate_fitness(individual):
    """
    Fitness = standard deviation of average skill levels of the 5 teams.
    Lower standard deviation = better balance.
    """
    team_averages = []

    for team in individual: 
        total_skill = sum(player['skill'] for player in team)
        average_skill = total_skill/len(team)
        team_averages.append(average_skill)

    overall_average = sum(team_averages)/len(team_averages)

    variance =  sum((avg - overall_average) ** 2 for avg in team_averages) / len(team_averages)
    std_deviation = math.sqrt(variance)

    

    return std_deviation