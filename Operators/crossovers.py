from copy import deepcopy
import random
# from Classes import Team, League, Player -- if we agree on changing and using those classes

def crossover_between_teams(league):
    """
    Perform a crossover between two teams within a league. 

    The crossover combines a fixed number of players from each parent team to form two new child teams.
    The crossover process swaps parts of Team 1 and Team 2, where we take the first 4 players from Team 1
    and the last 3 players from Team 2 to form the new teams. The original teams in the league are then replaced
    with the newly formed teams.

    Example:
    --------
    Consider the following teams:

    Team 1:
    - Player A1 (Position: GK)
    - Player A2 (Position: DEF)
    - Player A3 (Position: DEF)
    - Player A4 (Position: MID)
    - Player A5 (Position: MID)
    - Player A6 (Position: FWD)
    - Player A7 (Position: FWD)

    Team 2:
    - Player B1 (Position: GK)
    - Player B2 (Position: DEF)
    - Player B3 (Position: DEF)
    - Player B4 (Position: MID)
    - Player B5 (Position: MID)
    - Player B6 (Position: FWD)
    - Player B7 (Position: FWD)

    Step 1: Select 4 players from Team 1 (A1, A2, A3, A4) and 3 players from Team 2 (B5, B6, B7).

    Step 2: Combine the selected players to create two new teams:
    - New Team 1: 
      - A1 (Position: GK)
      - A2 (Position: DEF)
      - A3 (Position: DEF)
      - A4 (Position: MID)
      - B5 (Position: MID)
      - B6 (Position: FWD)
      - B7 (Position: FWD)

    - New Team 2: 
      - B1 (Position: GK)
      - B2 (Position: DEF)
      - B3 (Position: DEF)
      - B4 (Position: MID)
      - A5 (Position: MID)
      - A6 (Position: FWD)
      - A7 (Position: FWD)

    Step 3: Replace the original teams in the league with the newly created teams.

    Step 4: Return the updated league with the new child teams.

    Parameters:
    -----------
    league : League
        The league object containing multiple teams.

    Returns:
    --------
    League
        A new league object with the crossover teams, or None if the crossover is invalid.
    """
    # Select two random teams from the league
    team1, team2 = random.sample(league.teams, 2)

    print("Attempting crossover between:")
    print("Team 1:")
    for p in team1.players:
        print(f"{p.name} ({p.position})")
    print("Team 2:")
    for p in team2.players:
        print(f"{p.name} ({p.position})")

    # Try fixed crossover point 
    # We choose 4 players from team1 and 3 players from team2 since 
    players1_part = team1.players[:4]
    players2_part = team2.players[4:]

    new_players1 = players1_part + players2_part

    players2_alt_part = team2.players[:4]
    players1_alt_part = team1.players[4:]
    new_players2 = players2_alt_part + players1_alt_part

    try:
        new_team1 = Team(new_players1)
        new_team2 = Team(new_players2)

        # Replace original teams in the league
        child = deepcopy(league)
        child.teams = [t for t in league.teams if t != team1 and t != team2]
        child.teams.extend([new_team1, new_team2])

        print("Successful crossover: 4 players from each parent exchanged.")
        return child

    except ValueError as e:
        print("Invalid crossover:", str(e))
        return None

def crossover_between_leagues(parent1, parent2):
    """
    Perform a crossover between two leagues by swapping one or more teams between them.

    This crossover process selects a random number of teams (1 or 2) from each league and swaps them.
    It uses deep copies of the parent leagues to ensure that the original leagues remain unchanged.

    Example:
    --------
    Consider two parent leagues, Parent 1 and Parent 2, each containing 3 teams:

    Parent 1:
    - Team 1: (Player A1, Player A2, Player A3)
    - Team 2: (Player B1, Player B2, Player B3)
    - Team 3: (Player C1, Player C2, Player C3)

    Parent 2:
    - Team 1: (Player D1, Player D2, Player D3)
    - Team 2: (Player E1, Player E2, Player E3)
    - Team 3: (Player F1, Player F2, Player F3)

    Step 1: Randomly select how many teams to swap (e.g., 2 teams).

    Step 2: Randomly select the indices of the teams to swap (e.g., swap Team 1 and Team 2).

    Step 3: After the swap, the child leagues will look like this:

    Child 1 (after crossover):
    - Team 1: (Player D1, Player D2, Player D3)
    - Team 2: (Player E1, Player E2, Player E3)
    - Team 3: (Player C1, Player C2, Player C3)

    Child 2 (after crossover):
    - Team 1: (Player A1, Player A2, Player A3)
    - Team 2: (Player B1, Player B2, Player B3)
    - Team 3: (Player F1, Player F2, Player F3)

    Parameters:
    -----------
    parent1 : League
        The first parent league to swap teams from.

    parent2 : League
        The second parent league to swap teams from.

    Returns:
    --------
    tuple : (League, League)
        A tuple containing the two child leagues after the crossover. Each child league contains a combination of teams from both parents.
    """
    # Deep copy to avoid changing the original parents
    child1 = deepcopy(parent1)
    child2 = deepcopy(parent2)

    # Choose how many teams to swap 
    num_teams_to_swap = random.randint(1, min(len(child1.teams), len(child2.teams)))

    # Select random team indices to swap
    indices = random.sample(range(len(child1.teams)), num_teams_to_swap)

    print(f"Swapping teams at indices: {indices}")

    for idx in indices:
        child1.teams[idx], child2.teams[idx] = child2.teams[idx], child1.teams[idx]

    # Print changes for verification
    print("\nTeam-level crossover complete.\n")

    return child1, child2