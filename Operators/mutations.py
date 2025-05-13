import random
from copy import deepcopy

# REMOVE AND IMPORT League and Player classes from their respective files
def calculate_fitness(league):
    if league is None or not league.is_valid():
        return 9999
    return league.get_standard_deviation_of_average_skills()

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

def single_player_swap_2teams(league: League, mut_prob: float) -> League:
    """
    Mutation: swap one player of the same position between two different teams.
    
    Parameters:
        league (League): the parent solution
        mut_prob (float): probability of performing the swap
    
    Returns:
        League: either a mutated copy or (if no mutation or invalid swap) a copy of the original
    """
    # Always work on a copy
    new_league = deepcopy(league)

    # Roll the dice
    if random.random() > mut_prob:
        return new_league

    # Choose two distinct team indices
    idx1, idx2 = random.sample(range(len(new_league.teams)), 2)
    team1 = new_league.teams[idx1]
    team2 = new_league.teams[idx2]

    # Choose a position to swap
    position = random.choice(["GK", "DEF", "MID", "FWD"])

    # Gather players in that position
    p1_candidates = [p for p in team1.players if p.position == position]
    p2_candidates = [p for p in team2.players if p.position == position]

    # Should always be non-empty if teams are valid
    if not p1_candidates or not p2_candidates:
        # nothing to do
        return new_league

    # Pick one player from each
    p1 = random.choice(p1_candidates)
    p2 = random.choice(p2_candidates)

    # Swap them in the teams' player lists
    i1 = team1.players.index(p1)
    i2 = team2.players.index(p2)
    team1.players[i1], team2.players[i2] = p2, p1

    # Validate both teams and the league; rollback on failure
    try:
        team1.validate_team()
        team2.validate_team()
        new_league.validate_league()
    except ValueError:
        # Invalid mutation
        print("Invalid mutation: returning NONE")
        return None
    return new_league

def single_player_shift_all_teams(league: League, mut_prob: float) -> League | None:
    """
    Mutation: choose a position, pick one player of that position from each team,
    and shift them all one team forward (circularly).

    Returns:
      - A mutated League if the swap succeeds and still validates,
      - A copy of the original League if no mutation is attempted,
      - None if the swap was attempted but produced an invalid League.
    """
    new_league = deepcopy(league)

    # Skip mutation?
    if random.random() > mut_prob:
        return new_league

    # 1) Pick a position
    position = random.choice(["GK", "DEF", "MID", "FWD"])

    # 2) From each team, pick one player of that position
    selected_players = []
    for team in new_league.teams:
        candidates = [p for p in team.players if p.position == position]
        # Shouldn’t happen in a valid team, but guard anyway
        if not candidates:
            return new_league
        selected_players.append(random.choice(candidates))

    # 3) Perform the circular shift:
    #    each team_i loses its selected player and gains the one from team_(i-1)
    for i, team in enumerate(new_league.teams):
        leaving = selected_players[i]
        arriving = selected_players[i - 1]  # Python’s -1 wraps to last team

        # Remove the old player, insert the new one
        team.players.remove(leaving)
        team.players.append(arriving)

    # 4) Validate: if anything’s broken, bail out with None
    try:
        for team in new_league.teams:
            team.validate_team()
        new_league.validate_league()
    except ValueError:
        return None

    return new_league