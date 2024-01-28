import time
from random import randint
from typing import List


def egalitarian_allocation(values1: List[float], values2: List[float]):
    """
    Calculate the egalitarian allocation of items between two players based on their values.

    Args:
        values1 (List[float]): List of values representing the utility of items for Player 0.
        values2 (List[float]): List of values representing the utility of items for Player 1.

    Returns:
        None: Prints the allocation results.

    Examples:
        >>> values1 = [1.0, 4.0, 3.0]
        >>> values2 = [6.0, 4.0, 6.0]
        >>> egalitarian_allocation(values1, values2)
        Player 0 gets items 1, 2 with value of 7.0
        Player 1 gets items 0 with value of 6.0
    """
    # Initialize variables
    start = [0, 0, [], []]
    situations = [[start]]
    pessimistic_value = find_pessimistic_value(start.copy(), values1, values2)

    # Populate situations
    for i in range(len(values1)):
        new_situations = []
        for j in range(len(situations[i])):
            old_situation = situations[i][j]
            new_situation1 = [
                old_situation[0] + values1[i],
                old_situation[1],
                old_situation[2] + [i],
                old_situation[3]
            ]
            new_situation2 = [
                old_situation[0],
                old_situation[1] + values2[i],
                old_situation[2],
                old_situation[3] + [i]
            ]

            new_situations.extend([new_situation1, new_situation2])
            # pruning2(new_situations, values1, values2, new_situation1, i, pessimistic_value)
            # pruning2(new_situations, values1, values2, new_situation2, i, pessimistic_value)
            pruning1(new_situations)


        situations.append(new_situations)

    min_max_value = max(situations[len(values1)], key=lambda situation: min(situation[0:2]))

    items_player_0 = ', '.join(map(str, min_max_value[2]))
    items_player_1 = ', '.join(map(str, min_max_value[3]))

    print(f"Player 0 gets items {items_player_0} with value of {min_max_value[0]}")
    print(f"Player 1 gets items {items_player_1} with value of {min_max_value[1]}")


def pruning1(situations):
    i = 0
    while i < len(situations) - 1:
        j = i + 1
        while j < len(situations):
            if situations[i][0:2] == situations[j][0:2]:
                situations.pop(j)
            else:
                j += 1
        i += 1


def pruning2(situations: list[list[float]], values1: list[float], values2: list[float], situation,index, pessimistic_value):

   opt_situation = situation.copy()
   if find_optimize_value(opt_situation, values1, values2, index+1) < pessimistic_value:
       situations.pop(situations.index(situation))


def find_pessimistic_value(situation, values1: List[float], values2: List[float]):
    for i in range(0, len(values1)):

        # Randomly decide which player receives the item
        chosen_player = randint(0, 1)

        # Update the situation based on the chosen player
        if chosen_player == 0:
            situation[0] += values1[i]
        else:
            situation[1] += values2[i]

    return min(situation[0], situation[1])


def find_optimize_value(situation, values1: List[float], values2: List[float], index):
    if index == len(values1):
        return

    for i in range(index, len(values1)):
        situation[0] += values1[i]
        situation[1] += values2[i]


    return min(situation[0], situation[1])


if __name__ == "__main__":
    import doctest
    doctest.testmod()


