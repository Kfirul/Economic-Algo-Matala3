from typing import List
import networkx as nx
import math

from networkx import NetworkXUnbounded


class Edge:
    def __init__(self, weight, to_node, item):
        self.weight = weight
        self.to_node = to_node
        self.item = item

class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)

class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)

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
    num_players = len(valuations)

    # Build the graph
    graph = Graph()

    for i in range(num_players):
        player_node = Node(f"Player_{i}")
        graph.add_node(player_node)

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

                edge = Edge(min_weight, graph.nodes[j], index)
                graph.nodes[i].add_edge(edge)

    # Convert the graph to a NetworkX graph
    nx_graph = nx.DiGraph()

    for node in graph.nodes:
        for edge in node.edges:
            nx_graph.add_edge(node.name, edge.to_node.name, weight=edge.weight)

    # Check for negative weight cycles using NetworkX's Bellman-Ford
    negative_cycle = nx.negative_edge_cycle(nx_graph, weight='weight')
    # find_improve_pareto_efficient(neg_cycle_bellman_ford(nx_graph, list(graph.nodes)[0].name),valuations,allocations)

    if negative_cycle is not None:
        print("Negative cycle detected.")
        print(neg_cycle_bellman_ford(nx_graph, list(graph.nodes)[0].name))

    return not negative_cycle  # If no negative weight cycle, return True


def neg_cycle_bellman_ford(graph, src):
    dist = {node: float('inf') for node in graph.nodes}
    parent = {node: None for node in graph.nodes}
    dist[src] = 0

    # Relax all edges |V| - 1 times.
    for _ in range(len(graph.nodes) - 1):
        for u, v, data in graph.edges(data=True):
            if dist[u] + data['weight'] < dist[v]:
                dist[v] = dist[u] + data['weight']
                parent[v] = u

    # Check for negative-weight cycles
    cycle_node = None
    for u, v, data in graph.edges(data=True):
        if dist[u] + data['weight'] < dist[v]:
            # Store one of the vertices of the negative weight cycle
            cycle_node = v
            break

    if cycle_node is not None:
        cycle_nodes = set()
        v = cycle_node
        while v is not None and v not in cycle_nodes:
            cycle_nodes.add(v)
            v = parent[v]

        return list(cycle_nodes)



def find_improve_pareto_efficient(cycle_nodes, valuations, allocations):
    node, min_value = find_smallest_value(cycle_nodes, valuations, allocations)

    epsilon = 0.1  # You can adjust this value based on your requirements
    current_node = node
    current_index = cycle_nodes.index(current_node)

    # Iterate through the cycle until a Pareto-efficient allocation is achieved
    while not is_pareto_efficient(valuations, allocations):
        for i in range(0, len(cycle_nodes)):
            next_node = cycle_nodes[(current_index + 1) % len(cycle_nodes)]

            # Calculate the epsilon/allocation ratio
            epsilon_ratio = epsilon / allocations[cycle_nodes.index(current_node)][find_edge_to_next_node(current_node, cycle_nodes, current_index).item]

            # Update the allocation from the current node to the next node
            allocations[cycle_nodes.index(current_node)][find_edge_to_next_node(current_node, cycle_nodes, current_index).item] -= epsilon_ratio
            allocations[cycle_nodes.index(next_node)][find_edge_to_next_node(current_node, cycle_nodes, current_index).item] += epsilon_ratio

            # Move to the next node in the cycle
            current_node = next_node
            current_index = cycle_nodes.index(current_node)

    print(valuations)
    print(allocations)



def find_smallest_value(cycle_nodes, valuations, allocations):
    # Initialize variables to store the minimum value and the corresponding node
    min_value = float('inf')
    min_node = None

    # Iterate over the nodes in the negative weight cycle
    for node in cycle_nodes:
        # Calculate the value using a custom function
        current_value = custom_function(node, valuations, allocations, cycle_nodes, cycle_nodes.index(node))

        # Update the minimum value and corresponding node if the current value is smaller
        if current_value < min_value:
            min_value = current_value
            min_node = node

    return min_node.name, min_value


# Define a custom function that calculates the value based on node, valuations, and allocations
def custom_function(node, valuations, allocations, cycle_nodes, index):
    # Access the relevant information for the calculation
    node_name = node.name  # Retrieve the node name

    # Find the edge corresponding to the next node in the cycle
    edge_to_next_node = find_edge_to_next_node(node, cycle_nodes, index)

    # Get the index of the item associated with the edge
    item_index = edge_to_next_node.item

    # Access valuation and allocation values
    valuation_value = valuations[cycle_nodes.index(node)][item_index]
    allocation_value = allocations[cycle_nodes.index(node)][item_index]

    # Example: Minimize the product of valuation and allocation for each node
    return valuation_value * allocation_value



def find_edge_to_next_node(node, cycle_nodes, index):
    # Handle wrapping around to the beginning of the cycle_nodes list
    next_index = (index + 1) % len(cycle_nodes)

    # Iterate over the edges of the current node
    for edge in node.edges:
        # Check if the next node in the cycle is the target of the current edge
        if edge.to_node == cycle_nodes[next_index]:
            return edge  # Return the edge if found




if __name__ == "__main__":
    valuations = [[3,1,6], [6,3,1], [1,6,3]]
    allocations = [[1,0,0], [0,1,0], [0,0,1]]

    result = is_pareto_efficient(valuations, allocations)
    print(result)
