import time
from random import randint
from typing import List
import matplotlib.pyplot as plt

def max_mul_values(values1: List[float], values2: List[float]):
    """
    Calculate the allocation of items that maximizes the product of values for each player.

    Args:
        values1 (List[float]): List of values representing the utility of items for Player 0.
        values2 (List[float]): List of values representing the utility of items for Player 1.

    Returns:
        None: Prints the allocation results.

    Examples:
        >>> values1 = [1.0, 4.0, 3.0]
        >>> values2 = [6.0, 4.0, 6.0]
        >>> max_mul_values(values1, values2)
        Player 0 gets items 1, 2 with value of 7.0
        Player 1 gets items 0 with value of 6.0
    """
    # Initialize variables
    start = [1, 1, [], []]
    situations = [[start]]

    # Populate situations
    for i in range(len(values1)):
        new_situations = []
        for j in range(len(situations[i])):
            old_situation = situations[i][j]
            new_situation1 = [
                old_situation[0] * values1[i],
                old_situation[1],
                old_situation[2] + [i],
                old_situation[3]
            ]
            new_situation2 = [
                old_situation[0],
                old_situation[1] * values2[i],
                old_situation[2],
                old_situation[3] + [i]
            ]

            new_situations.extend([new_situation1, new_situation2])
        situations.append(new_situations)

    min_max_value = max(situations[len(values1)], key=lambda situation: min(situation[0:2]))

    items_player0 = ', '.join(map(str, min_max_value[2]))
    items_player1 = ', '.join(map(str, min_max_value[3]))

    items_values_player0, items_values_player1 = find_items(min_max_value, values1, values2)

    print(f"Player 0 gets items {items_player0} with value of {items_values_player0}")
    print(f"Player 1 gets items {items_player1} with value of {items_values_player1}")


def find_items(min_max_value, values1: List[float], values2: List[float]):
    """
    Calculate the total values of items for each player in a given allocation.

    Args:
        min_max_value (List[float]): Allocation information containing indices of items for each player.
        values1 (List[float]): List of values representing the utility of items for Player 0.
        values2 (List[float]): List of values representing the utility of items for Player 1.

    Returns:
        Tuple[float, float]: Total values of items for Player 0 and Player 1, respectively.

    """
    sum0 = sum(values1[i] for i in min_max_value[2])
    sum1 = sum(values2[i] for i in min_max_value[3])

    return sum0, sum1

if __name__ == "__main__":
    import doctest
    doctest.testmod()
