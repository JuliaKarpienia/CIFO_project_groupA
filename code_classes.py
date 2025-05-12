import random
from copy import deepcopy
import pandas as pd
import math

class Player:
    def __init__(self, name, position, skill, cost):
        self.name = name
        self.position = position
        self.skill = skill
        self.cost = cost

    def __repr__(self):
        return f"{self.name} ({self.position}) Skill: {self.skill} Salary: €{self.cost}M"


class Team:
    def __init__(self, players=None):
        self.players = players if players else []

    def total_cost(self):
        return sum(player.cost for player in self.players)

    def position_counts(self):
        counts = {"GK": 0, "DEF": 0, "MID": 0, "FWD": 0}
        for player in self.players:
            counts[player.position] += 1
        return counts

    def is_valid(self, salary_cap=750):
        counts = self.position_counts()
        return (
            counts["GK"] == 1 and
            counts["DEF"] == 2 and
            counts["MID"] == 2 and
            counts["FWD"] == 2 and
            self.total_cost() <= salary_cap
        )

    def __repr__(self):
        return "\n".join(str(player) for player in self.players) + f"\nTotal Team Salary: €{self.total_cost()}M"


class League:
    def __init__(self, teams=None):
        self.teams = teams if teams else []

    def is_valid(self):
        return len(self.teams) == 5 and all(team.is_valid() for team in self.teams)

    def __repr__(self):
        return "\n\n".join(f"Team {i+1}:\n{team}" for i, team in enumerate(self.teams))



# Functions
def load_players_from_csv(filepath):
    df = pd.read_csv(filepath)
    players = []

    for _, row in df.iterrows():
        player = Player(
            name=row['Name'],
            position=row['Position'],
            skill=int(row['Skill']),
            cost=float(row['Salary (€M)'])
        )
        players.append(player)

    return players


def create_initial_population(players, population_size=50, salary_cap=750):
    population = []

    GKs = [p for p in players if p.position == 'GK']
    DEFs = [p for p in players if p.position == 'DEF']
    MIDs = [p for p in players if p.position == 'MID']
    FWDs = [p for p in players if p.position == 'FWD']

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
                team_players = []

                team_gk = [p for p in GKs if p.name not in used_player_names][:1]
                team_defs = [p for p in DEFs if p.name not in used_player_names][:2]
                team_mids = [p for p in MIDs if p.name not in used_player_names][:2]
                team_fwds = [p for p in FWDs if p.name not in used_player_names][:2]

                team_players = team_gk + team_defs + team_mids + team_fwds

                if len(team_players) != 7:
                    break

                for player in team_players:
                    used_player_names.add(player.name)

                team = Team(team_players)
                teams.append(team)

            if len(teams) == 5:
                league = League(teams)
                if league.is_valid():
                    valid = True
                    population.append(deepcopy(league))

    return population


def calculate_fitness(league):
    """
    Fitness = standard deviation of average skill levels of the 5 teams.
    Lower standard deviation = better balance.
    """
    if not league.is_valid():
        return 9999  # penalty for invalid league, it can be usefull during crossovers and mutations

    team_averages = []
    for team in league.teams:
        total_skill = sum(player.skill for player in team.players)
        average_skill = total_skill / len(team.players)
        team_averages.append(average_skill)

    overall_average = sum(team_averages) / len(team_averages)
    variance = sum((avg - overall_average) ** 2 for avg in team_averages) / len(team_averages)
    std_deviation = math.sqrt(variance)

    return std_deviation
