import random


def twors_mutation(individual, p_m):
    """
    Returns the offspring after applying an twors mutation. Two random points are selected, and the numbers in
    those positions are switched.

    Parameters:
    --------
        individual : list
                  List representing the individual.
    Returns:
    --------
        list
            Offspring obtained using inversion mutation.
    """

    if random.random() < p_m:  # Determining if the mutation is applied

        # Select two random positions within the individual
        pos1, pos2 = sorted(random.sample(range(len(individual)), 2))

        # Swap the values in those positions
        individual[pos1], individual[pos2] = individual[pos2], individual[pos1]

    # Getting the correct format of the offspring, with 7 (room H) at the end
    individual.append(7)
    return individual


def reverse_sequence_mutation(individual, p_m):
    """
    Returns the offspring after applying a reverse sequence mutation. We select two random positions and invert the
    elements in between.

    Parameters:
    --------
        individual : list
                  List representing the individual.
    Returns:
    --------
        list
            Offspring obtained using reverse sequence mutation.
        """
    if random.random() < p_m:  # Determining if the mutation is applied

        # Select two random positions within the individual
        start_pos, end_pos = sorted(random.sample(range(len(individual)), 2))

        # Reverse the order of the rooms between the selected positions
        reversed_substring = individual[start_pos:end_pos + 1][::-1]

        # Updating the individual with the changes
        individual[start_pos:end_pos + 1] = reversed_substring

    # Getting the correct format of the offspring, with 7 (room H) at the end
    individual.append(7)
    return individual


# Similar to reverse_sequence_mutation, but with an extra step:
def inverted_exchange_mutation(individual, p_m):
    """
    Returns the offspring after applying an inverted exchange mutation. Two positions are randomly selected and the
    numbers in those positions are inverted. A room is selected from outside the inverted substring and one from inside
    and they are switched.

    --------
        individual : list
                  List representing the individual.
    Returns:
    --------
        list
            Offspring obtained using inverted exchange mutation.
    """
    if random.random() < p_m:  # Determining if the mutation is applied

        # Select two random positions within the individual
        start_pos, end_pos = sorted(random.sample(range(len(individual)), 2))

        # Invert the order of the rooms between the selected positions
        inverted_substring = individual[start_pos:end_pos + 1][::-1]

        # Select a room from the inverted substring randomly
        selected_room = random.choice(inverted_substring)

        # Determine the rooms outside the inverted substring
        rooms_outside = [c for c in individual if c not in inverted_substring]

        if rooms_outside:
            replacement_room = random.choice(rooms_outside)
            # Replace the selected room with a random room outside the inverted substring
            inverted_substring[inverted_substring.index(selected_room)] = replacement_room
            individual[individual.index(replacement_room)] = selected_room

        for i in range(start_pos, end_pos + 1):
            individual[i] = inverted_substring[i - start_pos]  # Updating the individual with the individual substring

    # Getting the correct format of the offspring, with 7 (room H) at the end
    individual.append(7)
    return individual


def partial_shuffle_mutation(individual, p_m):
    """
    Returns the offspring after applying a partial shuffle mutation. We select two random points and shuffle the
    elements in between.

    Parameters:
    --------
        individual : list
                  List representing the individual.
    Returns:
    --------
        list
            Offspring obtained using partial shuffle mutation.
        """
    if random.random() < p_m:  # Determining if the mutation is applied

        # Select a random subset of genes within the individual
        start_pos, end_pos = sorted(random.sample(range(len(individual)), 2))

        substring = individual[start_pos:end_pos + 1]

        # Shuffle the order of the selected subset of genes
        random.shuffle(substring)

        # Updating the individual with the changes made
        individual[start_pos:end_pos + 1] = substring

    # Getting the correct format of the offspring, with 7 (room H) at the end
    individual.append(7)
    return individual
