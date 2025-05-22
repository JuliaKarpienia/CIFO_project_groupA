from copy import deepcopy
import random
from Operators.population import League

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
    #print(f"Swapping all players at position: {chosen_pos}")

    for t1, t2 in zip(child1.teams, child2.teams):
        # Get players by position from both teams
        p1 = [p for p in t1.players if p.position == chosen_pos]
        p2 = [p for p in t2.players if p.position == chosen_pos]

        # Skip if either team lacks players at the selected position
        if not p1 or not p2:
            #print(f"One of the teams lacks players at {chosen_pos}. Skipping swap for this pair.")
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

def crossover_swap_extreme_player(
    parent1: League,
    parent2: League
) -> tuple[League | None, League | None]:
    """
    Perform a crossover by swapping the most "extreme" player in a single position-block
    between two parent leagues, preserving team structure and avoiding duplicates.

    Steps:
    ------
    1. With probability (1 - cross_prob), skip crossover and return deep copies of the parents.
    2. Randomly select one position: 'GK', 'DEF', 'MID', or 'FWD'.
    3. In each parent league, find the player in that position whose skill deviates most
       from their team's average skill for that position.
    4. Swap those two players in-place between the corresponding teams in two new child leagues.
    5. Validate each child (team structure, unique players, salary cap); return None for any invalid.

    Example:
    --------
    If Parent 1's DEF skill deviations are [3.2, 5.1] and Parent 2's are [2.8, 4.9],
    the defender with deviation 5.1 in Parent 1 and 4.9 in Parent 2 get swapped.

    Parameters:
    -----------
    parent1 : League
        First parent league.
    parent2 : League
        Second parent league.
    cross_prob : float
        Probability of performing the crossover (0.0 to 1.0).

    Returns:
    --------
    tuple : (League | None, League | None)
        A pair of child leagues. Each is either:
          - A valid League with the two extreme players swapped, or
          - None, if the crossover led to an invalid league.
    """

    # 2) Pick position
    position = random.choice(["GK", "DEF", "MID", "FWD"])

    # 3) Find extreme in each parent
    def find_extreme(league):
        best = None  # (team_idx, player, deviation)
        for ti, team in enumerate(league.teams):
            block = [p for p in team.players if p.position == position]
            if not block:
                continue
            avg = sum(p.skill for p in block) / len(block)
            for p in block:
                dev = abs(p.skill - avg)
                if best is None or dev > best[2]:
                    best = (ti, p, dev)
        return best

    ex1 = find_extreme(parent1)
    ex2 = find_extreme(parent2)
    if not ex1 or not ex2:
        return None, None
    ti1, ply1, _ = ex1
    ti2, ply2, _ = ex2

    # 4) Clone parents
    child1, child2 = deepcopy(parent1), deepcopy(parent2)

    # 5) In-place swap in each child to avoid duplicates
    def swap_in_child(child, pA, pB):
        # find pA and pB in child
        locA = next((ti, i)
                    for ti, team in enumerate(child.teams)
                    for i, p in enumerate(team.players)
                    if p.name == pA.name)
        locB = next((ti, i)
                    for ti, team in enumerate(child.teams)
                    for i, p in enumerate(team.players)
                    if p.name == pB.name)
        tiA, iA = locA
        tiB, iB = locB
        child.teams[tiA].players[iA], child.teams[tiB].players[iB] = \
            child.teams[tiB].players[iB], child.teams[tiA].players[iA]

    swap_in_child(child1, ply1, ply2)
    swap_in_child(child2, ply2, ply1)

    # 6) Validate
    def validate(child):
        try:
            for t in child.teams:
                t.validate_team()
            child.validate_league()
            return True
        except ValueError:
            return False

    valid1 = validate(child1)
    valid2 = validate(child2)

    return (child1 if valid1 else None,
            child2 if valid2 else None)

