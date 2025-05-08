import random

# This is the example of a valid dataset from class
focus_loss = [[0, 10.2, 16, 4, 6, 12, 7.5, 9],
          [10.2, 0, 4.3, 8, 11, 2.2, 3, 11.5],
          [16, 4.3, 0, 9, 3, 6, 7, 5],
          [4, 8, 9, 0, 11, 10.5, 5, 2],
          [6, 11, 3, 11, 0, 9.8, 4, 10],
          [12, 2.2, 6, 10.5, 9.8, 0, 8, 8],
          [7.5, 3, 7, 5, 4, 8, 0, 10.1],
          [9, 11.5, 5, 2, 10, 8, 10.1, 0]]


# This function generates random focus loss, with the necessary conditions for the list of list to be valid
def random_focus_gen(size = 8, seed = None):
    """
    Returns a list of lists, representing the focus loss between rooms
    --------
    Parameters:
    size : integer
           Size of the list of lists, in this case it has a predefined value of 8, so 8x8 matrix
    Returns:
    8x8 matrix,representing the focus loss between rooms
    """

    if seed is not None:
        random.seed(seed)

    # Creating a placeholder list, with the correct size, because the indexes will be used later
    data = [[0] * size for _ in range(size)]

    # The while is used because the process will need to be repeated if the sum of one list is higher than 100%
    while True:
        max_focus = 0  # We will need to know what was the biggest focus loss between rooms, because of the A to C case

        for i in range(size):    # Iterating through each list in the matrix
            # Iterating through each element in a list, and also guaranteeing that when i = j, the value is 0
            for j in range(i + 1, size):
                value = round(random.uniform(0, 20), 1)    # Generating a random value, and rounding it to one decimal
                # place. 20 is an arbitrary number, and as the maximum for each row must be 100, it seemed the most reasonable

                data[i][j] = value
                data[j][i] = value   # The matrix needs to be symmetric
                max_focus = max(max_focus, value)    # Getting the maximum value found so far

        min_focus = max_focus * 1.04    # Multiplying the max value found by 4%

        # Making sure that the focus loss between A and C is at least 4% bigger than the maximum focus loss between other two rooms:
        data[0][2] = round(random.uniform(min_focus, min_focus + 20), 1)
        data[2][0] = data[0][2]   # The matrix must be symmetrical

        #Checking that none of the rows has a sum greater than 100, if it does, the loop is repeated, if not, we terminate
        if all(sum(row) <= 100 for row in data):
            break

    return data
