from copy import deepcopy
import random
from population import *

def crossover_swap_whole_position(league1, league2):
    """
    Perform a crossover between two leagues by swapping all players of a randomly selected position (GK, DEF, MID, or FWD)
    between corresponding teams in each league.

    This crossover selects one position and swaps players in that position between matching teams (i.e., Team 1 of League 1 
    with Team 1 of League 2, and so on). If a team does not have any players in the selected position, the swap is skipped 
    for that specific pair of teams.

    Example:
    --------
    Consider two parent leagues, Parent 1 and Parent 2, each containing 3 teams:

    Parent 1:
    - Team 1: GK(A1), DEF(A2, A3), MID(A4, A5), FWD(A6, A7)
    - Team 2: GK(B1), DEF(B2, B3), MID(B4, B5), FWD(B6, B7)
    - Team 3: GK(C1), DEF(C2, C3), MID(C4, C5), FWD(C6, C7)

    Parent 2:
    - Team 1: GK(D1), DEF(D2, D3), MID(D4, D5), FWD(D6, D7)
    - Team 2: GK(E1), DEF(E2, E3), MID(E4, E5), FWD(E6, E7)
    - Team 3: GK(F1), DEF(F2, F3), MID(F4, F5), FWD(F6, F7)

    Step 1: Randomly select a position (e.g., "DEF")

    Step 2: For each pair of teams at the same index, swap their players at that position

    Step 3: After the swap, the child leagues will look like this (assuming position "DEF" was chosen):

    Child 1:
    - Team 1: GK(A1), DEF(D2, D3), MID(A4, A5), FWD(A6, A7)
    - Team 2: GK(B1), DEF(E2, E3), MID(B4, B5), FWD(B6, B7)
    - Team 3: GK(C1), DEF(F2, F3), MID(C4, C5), FWD(C6, C7)
    
    Child 2:
    - Team 1: GK(D1), DEF(A2, A3), MID(D4, D5), FWD(D6, D7)
    - Team 2: GK(E1), DEF(B2, B3), MID(E4, E5), FWD(E6, E7)
    - Team 3: GK(F1), DEF(C2, C3), MID(F4, F5), FWD(F6, F7)

    Parameters:
    -----------
    league1 : League
        The first parent league to perform crossover from.

    league2 : League
        The second parent league to perform crossover from.

    Returns:
    --------
    tuple : (League, League)
        A tuple containing the two child leagues after the crossover. Each child league contains a mix of players at the 
        selected position swapped between corresponding teams.
    """
    # Deep copy leagues to avoid altering the originals
    child1 = deepcopy(league1)
    child2 = deepcopy(league2)

    positions = ['GK', 'DEF', 'MID', 'FWD']
    chosen_pos = random.choice(positions)
    print(f"Swapping all players at position: {chosen_pos}")

    for t1, t2 in zip(child1.teams, child2.teams):
        # Get players by position from both teams
        p1 = [p for p in t1.players if p.position == chosen_pos]
        p2 = [p for p in t2.players if p.position == chosen_pos]

        # Skip if either team lacks players at the selected position
        if not p1 or not p2:
            print(f"One of the teams lacks players at {chosen_pos}. Skipping swap for this pair.")
            continue

        # Make sure the numbers match, swap only as many players as available in both teams
        min_len = min(len(p1), len(p2))

        # Swap equal number of players for the selected position
        for i in range(min_len):
            player1 = p1[i]
            player2 = p2[i]

            # Replace by identity to avoid name conflicts
            def replace_player(team, old_p, new_p):
                team.players = [new_p if p is old_p else p for p in team.players]

            replace_player(t1, player1, player2)
            replace_player(t2, player2, player1)

    return child1, child2


def preset_team_mix_crossover(parent1, parent2):
    """
    Performs a deterministic crossover using a fixed team selection pattern from each parent.
    Ensures that no player appears more than once in the resulting child leagues.

    Pattern:
    Child 1: Teams 1, 3, 5 from parent1; Teams 2, 4 from parent2
    Child 2: Teams 1, 3, 5 from parent2; Teams 2, 4 from parent1

    Parameters:
    -----------
    parent1 : League
        First parent league.
    parent2 : League
        Second parent league.

    Returns:
    --------
    tuple : (League, League)
        Two new child leagues built from the preset team pattern. If duplicates are found,
        it raises an error.
    """

    def build_child(pattern, source1, source2):
        teams = []
        for idx in pattern:
            if idx[0] == 1:
                teams.append(deepcopy(source1.teams[idx[1]]))
            else:
                teams.append(deepcopy(source2.teams[idx[1]]))
        return League(teams)

    # Define the selection pattern: (source_league, team_index)
    pattern_child1 = [(1, 0), (2, 1), (1, 2), (2, 3), (1, 4)]
    pattern_child2 = [(2, 0), (1, 1), (2, 2), (1, 3), (2, 4)]

    child1 = build_child(pattern_child1, parent1, parent2)
    child2 = build_child(pattern_child2, parent1, parent2)

    # Validate for duplicate players
    def validate_unique_players(league, child_name):
        player_names = set()
        for i, team in enumerate(league.teams):
            for player in team.players:
                if player.name in player_names:
                    raise ValueError(
                        f"{child_name} is invalid: Duplicate player {player.name} in team {i+1}."
                    )
                player_names.add(player.name)

    try:
        validate_unique_players(child1, "Child 1")
        validate_unique_players(child2, "Child 2")
    except ValueError as e:
        print("Validation failed:", e)
        return None, None

    print("Preset team mix crossover successful.")
    return child1, child2
