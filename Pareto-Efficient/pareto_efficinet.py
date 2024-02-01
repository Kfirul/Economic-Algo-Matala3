from typing import List
import networkx as nx
import math

class Edge:
    def __init__(self, weight, to_node):
        self.weight = weight
        self.to_node = to_node

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
    num_players = len(valuations)

    # Build the graph
    graph = Graph()

    for i in range(num_players):
        player_node = Node(f"Player_{i}")
        graph.add_node(player_node)

    for i in range(num_players):
        for j in range(num_players):
            if i != j:
                weights = []
                for z in range(len(valuations[i])):
                    if allocations[i][z] > 0:
                        weights.append(math.log(valuations[i][z] / valuations[j][z]))

                edge = Edge(min(weights), graph.nodes[j])
                graph.nodes[i].add_edge(edge)

    # Convert the graph to a NetworkX graph
    nx_graph = nx.DiGraph()

    for node in graph.nodes:
        for edge in node.edges:
            nx_graph.add_edge(node.name, edge.to_node.name, weight=edge.weight)

    # Check for negative weight cycles using NetworkX's Bellman-Ford
    negative_cycle = nx.negative_edge_cycle(nx_graph, weight='weight')

    return not negative_cycle  # If no negative weight cycle, return True

# Example usage:
valuations = [[10, 20, 30, 40], [40, 30, 20, 10]]
allocations = [[0, 0.7, 1, 1], [1, 0.3, 0, 0]]

result = is_pareto_efficient(valuations, allocations)
print(result)
