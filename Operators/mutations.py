import random
from copy import deepcopy
from Operators.population import League


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
        #print("Invalid mutation: returning NONE")
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

import random
from copy import deepcopy

def full_position_swap_2teams(league: League, mut_prob: float) -> League | None:
    """
    Mutation: swap all players of one position between two different teams.
    
    Parameters:
      league (League): the parent solution
      mut_prob (float): probability of performing the swap
    
    Returns:
      - A new mutated League if the swap succeeds and still validates,
      - A copy of the original League if no mutation is attempted,
      - None if the swap was attempted but produced an invalid League.
    """
    new_league = deepcopy(league)

    # 1) Maybe skip mutation
    if random.random() > mut_prob:
        return new_league

    # 2) Pick two distinct teams
    idx1, idx2 = random.sample(range(len(new_league.teams)), 2)
    team1, team2 = new_league.teams[idx1], new_league.teams[idx2]

    # 3) Pick a position to swap
    position = random.choice(["GK", "DEF", "MID", "FWD"])

    # 4) Collect all players of that position from each team
    p1_list = [p for p in team1.players if p.position == position]
    p2_list = [p for p in team2.players if p.position == position]

    # If somehow there are none, abort without mutation
    if not p1_list or not p2_list:
        return new_league

    # 5) Swap them: remove all from each, then add the others
    for p in p1_list:
        team1.players.remove(p)
    for p in p2_list:
        team2.players.remove(p)

    # add back
    team1.players.extend(p2_list)
    team2.players.extend(p1_list)

    # 6) Validate teams and league; on failure return None
    try:
        team1.validate_team()
        team2.validate_team()
        new_league.validate_league()
    except ValueError:
        return None

    return new_league
