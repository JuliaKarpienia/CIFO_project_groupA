def binary_standard_mutation(representation: str | list, mut_prob):
    """
    Applies standard binary mutation to a binary string or list representation.

    This function supports both binary strings (e.g., "10101") and binary lists 
    (e.g., [1, 0, 1, 0, 1]) containing either string characters ("0", "1") or 
    integers (0, 1). Each gene in the representation is independently flipped 
    with a given mutation probability, while preserving the original data type 
    of the genes.

    Parameters:
        representation (str or list): The binary representation to mutate.
        mut_prob (float): The probability of flipping each gene.

    Returns:
        str or list: A new mutated representation of the same type as the input.

    Raises:
        ValueError: If the input contains elements other than 0, 1, "0", or "1".
    """

    # Initialize new representation as a copy of current representation
    new_representation = deepcopy(representation)

    if random.random() <= mut_prob:
        # Strings are not mutable. Let's convert temporarily to a list
        if isinstance(representation, str):
            new_representation = list(new_representation)

        for char_ix, char in enumerate(representation):
            if char == "1":
                new_representation[char_ix] = "0"
            elif char == 1:
                new_representation[char_ix] = 0
            elif char == "0":
                new_representation[char_ix] = "1"
            elif char == 0:
                new_representation[char_ix] = 1
            else:
                raise ValueError(f"Invalid character {char}. Can not apply binary standard mutation")
    
        # If representation was a string, convert list back to string
        if isinstance(representation, str):
            new_representation = "".join(new_representation)

    return new_representation

def swap_mutation(representation, mut_prob):
    """
    Applies swap mutation to a solution representation with a given probability.

    Swap mutation randomly selects two different positions (genes) in the 
    representation and swaps their values. This operator is commonly used for 
    permutation-based representations but works for any list or string.

    The function preserves the type of the input representation: if the input is 
    a string, the output will also be a string; if it's a list, the output will 
    remain a list.

    Parameters:
        representation (str or list): The solution to mutate.
        mut_prob (float): The probability of performing the swap mutation.

    Returns:
        str or list: A new solution with two genes swapped, of the same type as the input.
    """

    # Strings are not mutable. Let's convert to list first
    if isinstance(representation, str):
        new_representation = deepcopy(list(representation))
    elif isinstance(representation, list):
        new_representation = deepcopy(representation)

    if random.random() <= mut_prob:
        first_idx = random.randint(0, len(representation) - 1)

        # To guarantee we select two different positions
        second_idx = first_idx
        while second_idx == first_idx:
            second_idx = random.randint(0, len(representation) - 1)

        new_representation[first_idx] = representation[second_idx]
        new_representation[second_idx] = representation[first_idx]


    # If representation was a string, convert list back to string
    if isinstance(representation, str):
        new_representation = "".join(new_representation)
    
    return new_representation