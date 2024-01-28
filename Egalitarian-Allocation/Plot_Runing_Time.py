import time
from random import randint
from typing import List
import matplotlib.pyplot as plt

def plot_running_time(max_length: int):
    values_lengths = list(range(1, max_length + 1))

    # Lists to store running times for each scenario
    running_times_p1 = []
    # running_times_p2 = []
    # running_times_both = []
    running_times_none = []

    for length in values_lengths:
        # Generate values1 and values2
        values1 = [1.0] * length
        values2 = [2.0] * length

        # Run scenarios and measure running time
        start_time = time.time()
        egalitarian_allocation(values1, values2,False,False)
        end_time = time.time()
        running_times_none.append(end_time - start_time)

        start_time = time.time()
        egalitarian_allocation(values1, values2,True,False)
        end_time = time.time()
        running_times_p1.append(end_time - start_time)

        # start_time = time.time()
        # egalitarian_allocation(values1, values2,False,True)
        # end_time = time.time()
        # running_times_p2.append(end_time - start_time)
        #
        # start_time = time.time()
        # egalitarian_allocation(values1, values2,True,True)
        # end_time = time.time()
        # running_times_both.append(end_time - start_time)

    # Plotting
    plt.plot(values_lengths, running_times_none, label='Without Pruning')
    plt.plot(values_lengths, running_times_p1, label='With Pruning1')
    # plt.plot(values_lengths, running_times_p2, label='With Pruning2')
    # plt.plot(values_lengths, running_times_both, label='With Pruning1 and Pruning2')

    plt.title("Running Time vs Number Of Items")
    plt.xlabel("Number Of Items")
    plt.ylabel("Running Time (seconds)")
    plt.legend()
    plt.show()


def egalitarian_allocation(values1: List[float], values2: List[float],do_pruning1,do_pruning2):

    # Initialize variables
    start = [0, 0, [], []]
    situations = [[start]]
    pessimistic_value,pessimistic_situation = find_pessimistic_value(start.copy(), values1, values2)

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
            if do_pruning2:
                pruning2(new_situations, values1, values2, new_situation1, i, pessimistic_value)
                pruning2(new_situations, values1, values2, new_situation2, i, pessimistic_value)

            if do_pruning1:
                pruning1(new_situations)
        if len(new_situations) == 0:
            situations.append([pessimistic_situation])
        else:
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


def pruning2(situations: list[list[float]], values1: list[float], values2: list[float], situation, index, pessimistic_value):
    opt_situation = situation.copy()  # Create a copy of the situation
    if find_optimize_value(opt_situation.copy(), values1, values2, index+1) <= pessimistic_value:
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

    return min(situation[0], situation[1]), situation


def find_optimize_value(situation, values1: List[float], values2: List[float], index):
    for i in range(index, len(values1)):
        situation[0] += values1[i]
        situation[1] += values2[i]

    return min(50, situation[1])


if __name__ == "__main__":
    max_length_to_test = 20
    plot_running_time(max_length_to_test)
