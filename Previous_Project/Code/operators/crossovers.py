from base.individual import *
import random


def absent_room_case(p1):
    """
    Returns the a parent, in the case where one parent has room C and the other does not have room C inside, after
    altering the value to correspond to the second parent. So, if p1 has a 2, it's changed to a 99 and vice-versa.
    This function is only applied if p1 has room C and p2 does not, or the opposite case.

    Parameters:
    --------
        p1 : list
                  List representing the first parent.
    Returns:
    --------
        list
            Parent after making sure that it has the same rooms as the other parent
    """
    for room in range(len(p1)):
        if p1[room] == 2:           # Case when p1 has room C but p2 does not
            p1[p1.index(2)] = 99
        elif p1[room] == 99:        # Case when p2 does not have room C but p2 does
            p1[p1.index(99)] = 2
    return p1


def pmx_crossover(p1, p2):
    """
    Returns the offspring after applying a partially mapped crossover (in the nested function).

    Parameters:
    --------
        parent1 : list
                List representing the first parent.
        parent2 : list
                  List representing the second parent.
    Returns:
    --------
        list
            Offspring obtained using partially mapped crossover.
    """
    def pmx(o_p1, o_p2, crossover_start, crossover_end):

        # Creating a copy of the parents, so that no permanent changes are done to them
        parent1 = o_p1[:]
        parent2 = o_p2[:]

        offspring = [None] * len(parent1)   # Initializing the offspring

        # Handle the case where one parent has a value of 2 and the other 99, since the values need to match, for the mapping part
        if (2 in parent1 and 99 in parent2) or (99 in parent1 and 2 in parent2):
            parent1 = absent_room_case(parent1)

        # Assigning values from x between the crossover points to offspring
        offspring[crossover_start:crossover_end] = parent1[crossover_start:crossover_end]

        # Getting values not present in offspring after copying right values from parent1
        #remaining_bits = set(parent2[crossover_start:crossover_end]) - set(parent1[crossover_start:crossover_end])
        remaining_bits = [x for x in parent2 if x not in offspring]

        # Mapping process:
        for elem in remaining_bits:
            temp = elem
            index = parent2.index(parent1[parent2.index(temp)])  # Getting the correct value of p2
            while offspring[index] is not None:  # Finding an empty position in offspring
                temp = index  # Getting the index element to be mapped
                index = parent2.index(parent1[temp])  # Finding the next corresponding element of parent1 in parent2
            offspring[index] = elem  # Assigning said empty position the value

        for i in range(len(offspring)):
            if offspring[i] is None:
                offspring[i] = parent2[i]  # Checking if there are any values left, if so, copying them to the offspring

        return offspring

    cross_start, cross_end = sorted(random.sample(range(len(p1)), 2))  # Getting two random crossover points

    # Calling the function to generate the offspring, with the parents in opposite positions, so that the offspring are
    # different from each other, guaranteeing diversity
    off1 = pmx(p1, p2, cross_start, cross_end)  # Calling the inner function
    off2 = pmx(p2, p1, cross_start, cross_end)

    # Getting the correct format of the offspring, with 7 (room H) at the end
    off1.append(7)
    off2.append(7)

    return off1, off2


def improved_cycle_crossover(p1, p2):
    """
    Returns the offspring after applying an improved cycle crossover

    Parameters:
    --------
        p1 : list
                  List representing the first parent.
        p2 : list
                  List representing the second parent.
    Returns:
    --------
        list
            Offspring generated using improved cycle crossover
    """
    def imx(o_parent1, o_parent2):

        # Creating a copy of the parents, so that no permanent changes are done to them
        parent1 = o_parent1[:]
        parent2 = o_parent2[:]

        offspring = [None] * len(parent1)  # Initializing an offspring with the correct length

        # Making sure that the values match for the cases where we have 99 in one parent and 2 in the other
        if (2 in parent1 and 99 in parent2) or (99 in parent1 and 2 in parent2):
            parent1 = absent_room_case(parent1)      # Temporarily altering the value 2 or 99 in parent1

        # Set the first number of the offspring to be the 1st of parent2
        offspring[0] = parent2[0]
        index = 1

        valid = True
        # First cycle
        while None in offspring and valid:
            if offspring[index] is None:
                next_number = parent2[parent1.index(offspring[index - 1])]  # Getting the next value in the cycle
                if next_number not in offspring:  # Seeing if the value is not already in the offspring
                    offspring[index] = next_number
                else:
                    valid = False  # Terminating the cycle if we find a value that is already in the offspring
            index = (index + 1) % len(parent1)

        # Confirming if there are any empty places in the offspring after the first cycle is over
        if None in offspring:
            last_index = offspring[offspring.index(parent1[0])]
            if last_index == parent1[0]:  # The last index in the offspring needs to be equal to the first index in parent1

                # Complete the offspring using the remaining bits from parents
                remaining_bits = [x for x in parent2 if x not in offspring]
                for i in range(len(offspring)):
                    if offspring[i] is None:
                        offspring[i] = remaining_bits.pop(0)  # Assigning the remaining bits to the offspring
        return offspring

    # Calling the function to generate the offspring, with the parents in opposite positions, so that the offspring are
    # different from each other, guaranteeing diversity
    offspring1 = imx(p1, p2)
    offspring2 = imx(p2, p1)

    # Appending room H to the end
    offspring1.append(7)  # Appending room H at the end
    offspring2.append(7)

    return offspring1, offspring2


def ordered_crossover(p1, p2):
    """
    Returns the offspring after applying an ordered crossover.

    Parameters:
    --------
        parent1 : list
                  List representing the first parent.
        parent2 : list
                  List representing the second parent.
    Returns:
    --------
        list
            offspring generated using ordered crossover.
    """
    def ox(o_p1, o_p2, crossover_start, crossover_end):

        # Creating a copy of the parents, so that no permanent changes are done to them
        parent1 = o_p1[:]
        parent2 = o_p2[:]

        # Case where one parent has a value of 2 and the other 99: need to be the same values, so we temporarily replace
        # one of them
        if (2 in parent1 and 99 in parent2) or (99 in parent1 and 2 in parent2):
            parent1 = absent_room_case(parent1)    # Temporarily altering the value 2 or 99 in parent1

        offspring = [None] * len(parent1)  # Initializing the offspring with the correct length

        # Copying the values between crossover points to the offspring:
        offspring[crossover_start:crossover_end] = parent1[crossover_start:crossover_end]

        # Getting the remaining bits, starting from the end of the crossover points, from p2
        remaining_bits = [parent2[(crossover_end + i) % len(parent2)]  # %len(p2) is to avoid the index getting out of bounds
                             for i in range(len(parent2))
                             if parent2[(crossover_end + i) % len(parent2)] not in offspring]

        ind = crossover_end

        for i in range(len(parent1)):
            if offspring[ind] is None:  # Appending the remaining bits to offspring, starting at the crossover end
                offspring[ind] = remaining_bits.pop(0)

            ind = (ind + 1) % len(parent1)  # Updating the index and using %len(p1) so that it does not get out of bounds,
            # when it reaches the last value, it returns to the first index

        return offspring

    cross_start, cross_end = sorted(random.sample(range(len(p1)), 2))  # Getting 2 random crossover points

    # Calling the function to generate the offspring, with the parents in opposite positions, so that the offspring are
    # different from each other, guaranteeing diversity
    offspring1 = ox(p1, p2, cross_start, cross_end)
    offspring2 = ox(p2, p1, cross_start, cross_end)

    # Appending room H to the end
    offspring1.append(7)
    offspring2.append(7)

    return offspring1, offspring2


def fog_crossover(p1, p2):
    """
    Returns the offspring after applying a fog crossover (created by us). It chooses a random point. After that point,
    the rooms on parent one are copied to the offspring, but one position to the right. The remaining bits are assigned
    to the offspring in the order they are found on parent2.

    Parameters:
    --------
        p1 : list
            List representing the first parent.
        p2 : list
            List representing the second parent.
    Returns:
    --------
        list
            Offspring obtained using fog crossover.
    """
    def fx(o_p1, o_p2):
        # Creating a copy of the parents, so that no permanent changes are done to them
        parent1 = o_p1[:]
        parent2 = o_p2[:]

        # Case where one parent has a value of 2 and the other 99: need to be the same values, so we temporarily replace
        # one of them
        if (2 in parent1 and 99 in parent2) or (99 in parent1 and 2 in parent2):
            parent1 = absent_room_case(parent1)    # Temporarily altering the value 2 or 99 in parent1

        offspring = [None] * len(parent1)   # Initializing the offspring

        # Sliding all positions from the breaking point one position to the right, from parent1
        offspring[break_index + 1:] = parent1[break_index:len(parent1) - 1]  # Leaving the last one out, because
        # otherwise it would be out of bounds

        # Checking what are the remaining rooms not in the offspring, in the order of parent2
        remaining_bits = [x for x in parent2 if x not in offspring]

        for i in range(len(remaining_bits)):
            if offspring[i] is None:
                offspring[i] = remaining_bits[i]   # Adding the remaining bits to the offspring

        return offspring

    # Since the break_index needs to be the same for both offspring, it's generated randomly here
    break_index = random.randint(0, len(p1) - 1)

    # Calling the function to generate the offspring, with the parents in opposite positions, so that the offspring are
    # different from each other, guaranteeing diversity
    offspring1 = fx(p1, p2)
    offspring2 = fx(p2, p1)

    # Appending room H to the end
    offspring1.append(7)
    offspring2.append(7)

    return offspring1, offspring2


def slide_crossover(p1, p2):
    """
    Returns the offspring after applying a slide crossover (created by us). Similar to fog crossover.
    A breaking point is chosen. The rooms up to that point on parent1 are put at the end of the offspring. The remaining
    bits are assigned to the offspring on the order they are found in parent2.

    Parameters:
    --------
        p1 : list
            List representing the first parent.
        p2 : list
            List representing the second parent.
    Returns:
    --------
        list
            Offspring obtained using slide crossover.
    """
    def slide(o_p1, o_p2):

        # Creating a copy of the parents, so that no permanent changes are done to them
        parent1 = o_p1[:]
        parent2 = o_p2[:]

        # Case where one parent has a value of 2 and the other 99: need to be the same values, so we temporarily replace
        # one of them
        if (2 in parent1 and 99 in parent2) or (99 in parent1 and 2 in parent2):
            parent1 = absent_room_case(parent1)    # Temporarily altering the value 2 or 99 in parent1

        offspring = [None] * len(parent1)     # Initializing the offspring with the correct length

        # Sliding all positions up to the break poin to the end of the offspring, from parent1
        offspring[len(offspring) - break_index:] = parent1[:break_index]

        # Checking what are the remaining rooms not in the offspring, in the order of parent2
        remaining_bits = [x for x in parent2 if x not in offspring]

        for i in range(len(remaining_bits)):
            if offspring[i] is None:
                offspring[i] = remaining_bits[i]   # Adding the remaining bits to the offspring

        return offspring

    # Since the break_index needs to be the same for both offspring, it's generated randomly here
    break_index = random.randint(0, len(p1) - 1)

    # Calling the function to generate the offspring, with the parents in opposite positions, so that the offspring are
    # different from each other, guaranteeing diversity
    offspring1 = slide(p1, p2)
    offspring2 = slide(p2, p1)

    # Getting the correct format of the offspring, with 7 (room H) at the end
    offspring1.append(7)
    offspring2.append(7)

    return offspring1, offspring2
