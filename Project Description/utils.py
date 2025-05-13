import random
from copy import deepcopy

def single_player_swap_2teams(representation, mut_prob):
    """
    Randomly swap two players on different teams of the exact same position. 
    Assumes Forward 1 is different from Forward 2, etc.

    Parameters:
        representation (2D numpy array): The solution to mutate.
        mut_prob (float): The probability of performing the swap mutation.

    Returns:
        A 2D numpy array: A new solution with two players of the same position swapped.
    """

   
    new_representation = deepcopy(representation)

    if random.random() <= mut_prob:
        #Select a random team
        team1_index = random.randint(0, 4)

        #Select a different random team
        team2_index = random.randint(0, 4)
        while team2_index == team1_index:
            team2_index = random.randint(0, 4)
        
        #Select a random position on the team
        position_list = [0, 1, 2, 3, 4, 5, 6]
        position = random.choice(position_list)

        #Perform the swap muatation
        new_representation[team1_index][position], new_representation[team2_index][position] = \
        new_representation[team2_index][position], new_representation[team1_index][position]
    
    return new_representation



def full_position_swap_2teams(representation, mut_prob):
    """
    Randomly swap all players of a position between two teams. 
    For example, swap both forwards between two teams.
    If position is 'GK', this is equivalent to the sinlge player swap mutation.

    Parameters:
        representation (2D numpy array): The solution to mutate.
        mut_prob (float): The probability of performing the swap mutation.

    Returns:
        A 2D numpy array: A new solution with two players of the same position swapped.
    """

   
    new_representation = deepcopy(representation)

    if random.random() <= mut_prob:
        #Select a random team
        team1_index = random.randint(0, 4)

        #Select a different random team
        team2_index = random.randint(0, 4)
        while team2_index == team1_index:
            team2_index = random.randint(0, 4)
        
        #Select a random position on the team
        position_list = ['GK', 'DEF', 'MID', 'FWD']
        position_initial = random.choice(position_list)

        if position_initial == 'GK':
            position = 0
            
            #Perform the swap muatation
            new_representation[team1_index][position], new_representation[team2_index][position] = \
            new_representation[team2_index][position], new_representation[team1_index][position]
        
        elif position_initial == 'DEF':
            position1, position2 = 1, 2

            #Perform the swap muatation for all players of the position
            new_representation[team1_index][position1], new_representation[team2_index][position1] = \
            new_representation[team2_index][position1], new_representation[team1_index][position1]

            new_representation[team1_index][position2], new_representation[team2_index][position2] = \
            new_representation[team2_index][position2], new_representation[team1_index][position2]
        
        elif position_initial == 'MID':
            position1, position2 = 3, 4

            #Perform the swap muatation for all players of the position
            new_representation[team1_index][position1], new_representation[team2_index][position1] = \
            new_representation[team2_index][position1], new_representation[team1_index][position1]

            new_representation[team1_index][position2], new_representation[team2_index][position2] = \
            new_representation[team2_index][position2], new_representation[team1_index][position2]
        
        elif position_initial == 'FWD':
            position1, position2 = 5, 6
            #Perform the swap muatation for all players of the position

            new_representation[team1_index][position1], new_representation[team2_index][position1] = \
            new_representation[team2_index][position1], new_representation[team1_index][position1]

            new_representation[team1_index][position2], new_representation[team2_index][position2] = \
            new_representation[team2_index][position2], new_representation[team1_index][position2]
    
    return new_representation


def single_player_shift_all_teams(representation, mut_prob):
    """
    Choose a random position and shift each player of that position to the next team.
    Assumes Forward 1 is different from Forward 2, etc.

    Parameters:
        representation (2D numpy array): The solution to mutate.
        mut_prob (float): The probability of performing the swap mutation.

    Returns:
        A 2D numpy array: A new solution with two players of the same position swapped.
    """

   
    new_representation = deepcopy(representation)

    if random.random() <= mut_prob:
        #Select a random position on the team
        position_list = [0, 1, 2, 3, 4, 5, 6]
        position = random.choice(position_list)

        team1_index = 0
        team2_index = 1
        team3_index = 2
        team4_index = 3
        team5_index = 4

        #Perform the shift muatation
        new_representation[team1_index][position], new_representation[team2_index][position], new_representation[team3_index][position], \
        new_representation[team4_index][position], new_representation[team5_index][position] = \
        new_representation[team2_index][position], new_representation[team3_index][position], new_representation[team4_index][position], \
        new_representation[team5_index][position], new_representation[team1_index][position]
    
    return new_representation

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