import networkx as nx


def shortest_path(graph, source, target):
    """
    Find the original shortest path in a graph.

    Parameters:
        graph (List[Tuple[str, str, dict]]): List of edges with weights.
        source (str): Source node.
        target (str): Target node.

    Returns:
        Tuple[float, List[Tuple[Tuple[str, str], float]]]: Tuple containing the sum of the original shortest path weights
        and a list of edges with their weights in the original shortest path.
    """
    G = nx.Graph()

    for edge in graph:
        G.add_edge(edge[0], edge[1], weight=edge[2]['weight'])

    original_shortest_path = nx.shortest_path(G, source=source, target=target, weight='weight')
    original_shortest_path_weight = sum(G[original_shortest_path[i]][original_shortest_path[i + 1]]['weight']
                                       for i in range(len(original_shortest_path) - 1))

    original_edges = [(original_shortest_path[i], original_shortest_path[i + 1])
                      for i in range(len(original_shortest_path) - 1)]

    original_result = list(zip(original_edges, [G[edge[0]][edge[1]]['weight'] for edge in original_edges]))

    return original_shortest_path_weight, original_result


def vcg_cheapest_path(graph, source, target):
    """
    Find the original shortest path in a graph and iteratively remove each edge, printing the new shortest path
    and the weight difference compared to the original shortest path.

    Parameters:
        graph (List[Tuple[str, str, dict]]): List of edges with weights.
        source (str): Source node.
        target (str): Target node.
     Examples:
        >>> graph = [('A', 'B', {'weight': 2}), ('B', 'C', {'weight': 1}), ('A', 'D', {'weight': 3}),
        ...          ('D', 'C', {'weight': 4}), ('B', 'E', {'weight': 5}), ('C', 'F', {'weight': 2}),
        ...          ('E', 'F', {'weight': 1})]
        >>> source_node = 'A'
        >>> target_node = 'F'
        >>> vcg_cheapest_path(graph, source_node, target_node)
        Original Shortest Path: [(('A', 'B'), 2), (('B', 'C'), 1), (('C', 'F'), 2)]
        Original Shortest Path Weight: 5
        After removing edge ('A', 'B'), New Shortest Path: ['A', 'D', 'C', 'F']
        Weight Difference (considering removed edge): -6
        After removing edge ('B', 'C'), New Shortest Path: ['A', 'B', 'E', 'F']
        Weight Difference (considering removed edge): -4
        After removing edge ('C', 'F'), New Shortest Path: ['A', 'B', 'E', 'F']
        Weight Difference (considering removed edge): -5
    """

    # Get the original shortest path and its sum of weights
    original_shortest_path_weight, original_shortest_path = shortest_path(graph, source, target)
    print("Original Shortest Path:", original_shortest_path)
    print("Original Shortest Path Weight:", original_shortest_path_weight)

    # Iterate through each edge in the shortest path, remove it, and print the new shortest path and the weight difference
    for edge in original_shortest_path:
        # Create a copy of the original graph to avoid modifying it permanently
        G_copy = nx.Graph(graph)

        # Remove the current edge from the copy of the graph
        removed_edge_weight = G_copy[edge[0][0]][edge[0][1]]['weight']
        G_copy.remove_edge(edge[0][0], edge[0][1])

        # Find the new shortest path for the copy of the graph
        new_shortest_path = nx.shortest_path(G_copy, source=source, target=target, weight='weight')
        new_shortest_path_weight = sum(G_copy[new_shortest_path[i]][new_shortest_path[i + 1]]['weight']
                                       for i in range(len(new_shortest_path) - 1))

        # Calculate the weight difference, considering the weight of the removed edge
        weight_difference = original_shortest_path_weight - (new_shortest_path_weight + removed_edge_weight)

        print(f"After removing edge {edge[0]}, New Shortest Path:", new_shortest_path)
        print(f"Weight Difference (considering removed edge):", weight_difference)

if __name__ == "__main__":
    import doctest
    doctest.testmod()