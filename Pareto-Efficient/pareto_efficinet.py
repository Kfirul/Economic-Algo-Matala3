import networkx as nx
import math
from typing import List

#Part A
def create_exchange_graph(valuations: List[List[float]], allocations: List[List[float]]) -> nx.DiGraph:
    """
    Build a directed graph representing the allocation scenario.

    Args:
    - valuations (List[List[float]]): The valuation matrix where valuations[i][j] represents the value of item j for player i.
    - allocations (List[List[float]]): The allocation matrix where allocations[i][j] represents the amount of item j allocated to player i.

    Returns:
    - nx.DiGraph: Directed graph representing the allocation scenario.
    """
    num_players = len(valuations)
    nx_graph = nx.DiGraph()

    for i in range(num_players):
        for j in range(num_players):
            if i != j:
                min_weight = float('inf')
                index = -1
                for z in range(len(valuations[i])):
                    if allocations[i][z] > 0:
                        new_ratio = math.log(valuations[i][z] / valuations[j][z])
                        if new_ratio < min_weight:
                            min_weight = new_ratio
                            index = z

                nx_graph.add_edge(f"Player_{i}", f"Player_{j}", weight=min_weight, item=index)

    return nx_graph
#
def is_pareto_efficient(valuations: List[List[float]], allocations: List[List[float]]) -> bool:
    """
       Check if a given allocation is Pareto efficient.

       Args:
       - valuations (List[List[float]]): The valuation matrix where valuations[i][j] represents the value of item j for player i.
       - allocations (List[List[float]]): The allocation matrix where allocations[i][j] represents the amount of item j allocated to player i.

       Returns:
       - bool: True if the allocation is Pareto efficient, False otherwise.

       Examples:
       >>> valuations1 = [[10, 20, 30, 40], [40, 30, 20, 10]]
       >>> allocations1 = [[0, 0.7, 1, 1], [1, 0.3, 0, 0]]
       >>> is_pareto_efficient(valuations1, allocations1)
       True

       >>> valuations2 = [[3, 1, 6], [6, 3, 1], [1, 6, 3]]
       >>> allocations2 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
       >>> is_pareto_efficient(valuations2, allocations2)
       False
       """
    nx_graph = create_exchange_graph(valuations, allocations)

    # Check for negative weight cycles using NetworkX's Bellman-Ford
    negative_cycle = nx.negative_edge_cycle(nx_graph, weight='weight')

    return not negative_cycle  # If no negative weight cycle, return True

#Part B


    def find_positive_allocation_resources(player_allocation: List[float], epsilon: float) -> List[int]:
        return [resource_idx for resource_idx, allocation in enumerate(player_allocation) if allocation >= epsilon]

    def transfer_resources(improved_allocation: List[List[float]], player: int, resource: int, transfer_amount: float,
                           next_player: int) -> None:
        improved_allocation[player][resource] -= transfer_amount
        improved_allocation[next_player][resource] += transfer_amount

    def improve_pareto(valuations: List[List[float]], current_allocation: List[List[float]]) -> List[List[float]]:
        """
           Improve a given allocation to achieve Pareto efficiency.

           Args:
           - valuations (list[list[float]]): List of valuations for each player.
           - allocation (list[list[float]]): Current allocation matrix.

           Returns:
           - list[list[float]]: Improved Pareto efficient allocation.

           Examples:
           >>> improve_pareto([[10, 20, 30, 40], [40, 30, 20, 10]], [[0.1, 1, 0.5, 1], [0.9, 0, 0.5, 0]])
           [[0.0, 0.5, 1.0, 1], [1.0, 0.5, 0.0, 0]]

           >>> improve_pareto([[3, 6, 1], [6, 1, 3], [1, 3, 6]], [[0, 1, 0], [1, 0, 0], [0, 0, 1]])
           [[0, 1, 0], [1, 0, 0], [0, 0, 1]]

           >>> improve_pareto([[1, 3, 6], [3, 6, 1], [6, 1, 3]], [[0, 1, 0], [1, 0, 0], [0, 0, 1]])
           [[0, 0.0, 1.0], [0.0, 1.0, 0], [1.0, 0, 0.0]]

           """

        num_players = len(valuations)

        improved_allocation = [row.copy() for row in current_allocation]
        epsilon = 0.1


        while not is_pareto_efficient(valuations, improved_allocation):

            for i in range(num_players):
                positive_resources = find_positive_allocation_resources(improved_allocation[i], epsilon)

                if positive_resources:
                    min_valuation_resource = min(positive_resources,
                                                 key=lambda resource_idx: valuations[i][resource_idx])
                    transfer_amount = min(epsilon, improved_allocation[i][min_valuation_resource])

                    transfer_resources(improved_allocation, i, min_valuation_resource, transfer_amount,
                                       (i + 1) % num_players)

            return improved_allocation


if __name__ == "__main__":
    import doctest
    doctest.testmod()
