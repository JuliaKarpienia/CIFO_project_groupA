import random
import numpy as np
class Player:
    def __init__(self, name, position, skill, cost):
        self.name = name
        self.position = position
        self.skill = skill
        self.cost = cost

    def __str__(self):
        return f"{self.name} ({self.position}) - Skill: {self.skill}, Cost: {self.cost}M"
    
class Team:
    def __init__(self, players):
        self.players = players  # players is a list of Player objects
        self.validate_team()

    def validate_team(self):
        positions = {"GK": 0, "DEF": 0, "MID": 0, "FWD": 0}
        for player in self.players:
            if player.position not in positions:
                raise ValueError(f"Invalid player position: {player.position}")
            positions[player.position] += 1

        # Check the required structure
        if positions["GK"] != 1 or positions["DEF"] != 2 or positions["MID"] != 2 or positions["FWD"] != 2:
            raise ValueError("Each team must have 1 GK, 2 DEF, 2 MID, and 2 FWD.")

        # Check if the team exceeds salary cap
        total_salary = sum(player.cost for player in self.players)
        if total_salary > 750:
            raise ValueError(f"Team salary exceeds the cap: {total_salary}M")

    def get_average_skill(self):
        return sum(player.skill for player in self.players) / len(self.players)

    def __str__(self):
        return "\n".join([str(player) for player in self.players])

class League:
    def __init__(self, teams):
        self.teams = teams
        self.validate_league()
                
    def validate_league(self):
        if len(self.teams) != 5:
            raise ValueError("The league must have exactly 5 teams.")

        player_names = set()
        for team in self.teams:
            # Explicitly call team.validate_team()
            team.validate_team()

            for player in team.players:
                if player.name in player_names:
                    raise ValueError(f"Player {player.name} is already in another team.")
                player_names.add(player.name)


    def is_valid(self):
        try:
            self.validate_league()
            return True
        except ValueError:
            return False

    def get_standard_deviation_of_average_skills(self):
        avg_skills = [team.get_average_skill() for team in self.teams]
        return np.std(avg_skills)

    def __str__(self):
        return "\n\n".join([str(team) for team in self.teams])

def calculate_fitness(league):
    if league is None or not league.is_valid():
        return 9999
    return league.get_standard_deviation_of_average_skills()

def create_valid_team_from_pool(player_pool):
    max_attempts = 100
    for _ in range(max_attempts):
        gks = [p for p in player_pool if p.position == "GK"]
        defs = [p for p in player_pool if p.position == "DEF"]
        mids = [p for p in player_pool if p.position == "MID"]
        fwds = [p for p in player_pool if p.position == "FWD"]

        if len(gks) < 1 or len(defs) < 2 or len(mids) < 2 or len(fwds) < 2:
            raise ValueError("Not enough players in the pool to form a valid team.")

        selected_players = random.sample(gks, 1) + \
                           random.sample(defs, 2) + \
                           random.sample(mids, 2) + \
                           random.sample(fwds, 2)

        try:
            team = Team(selected_players)
            return team
        except ValueError:
            continue

    raise ValueError("Failed to create a valid team after many attempts.")

def create_valid_league(all_players, num_teams=5):
    max_attempts = 100
    for _ in range(max_attempts):
        random.shuffle(all_players)
        available_players = all_players.copy()
        used_names = set()
        teams = []

        try:
            for _ in range(num_teams):
                pool = [p for p in available_players if p.name not in used_names]
                team = create_valid_team_from_pool(pool)
                teams.append(team)
                used_names.update(p.name for p in team.players)
            return League(teams)
        except ValueError:
            continue

    raise ValueError("Failed to create a valid league after many attempts.")

def generate_population(players, num_leagues=5):
    population = []
    for _ in range(num_leagues):
        league = create_valid_league(players)
        population.append(league)
    return population
