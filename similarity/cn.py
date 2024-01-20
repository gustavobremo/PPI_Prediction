import networkx as nx


def calculate_paths_of_length_2(graph):
    """
    Calculate all paths of length 2 between nodes in a graph.

    A path of length 2 is defined as a sequence of two consecutive edges in the graph.

    Parameters:
    - graph (NetworkX Graph): The input graph.

    Returns:
    - paths (dict): A dictionary containing edges from the graph as keys, and lists of paths
      of length 2 as values. Each path is represented as a tuple of three nodes: (node, neighbor, second_neighbor).
    """
    paths = {}
    for node in graph.nodes():
        for neighbor in graph.neighbors(node):
            for second_neighbor in graph.neighbors(neighbor):
                if second_neighbor != node and not graph.has_edge(node, second_neighbor):
                    edge = (node, second_neighbor)
                    if edge not in paths:
                        paths[edge] = []
                    paths[edge].append((node, neighbor, second_neighbor))
    return paths


def calculate_cn(graph, complement):
    """
    Calculate the Common Neighbors (CN) score for edges in the complement of a graph.

    The Common Neighbors score is determined by counting the number of paths of length 2
    (common neighbors) between nodes in the complement of the given graph.

    Parameters:
    - graph (NetworkX Graph): The original graph.
    - complement (NetworkX Graph): The complement graph.

    Returns:
    - ranked_edges (dict): A dictionary containing edges from the complement graph as keys
      and their corresponding CN scores as values. The dictionary is sorted in descending
      order based on the CN scores.
    """
    results = {}
    all_paths = calculate_paths_of_length_2(graph)

    for edge in complement.edges():
        if edge in all_paths:
            results[edge] = len(all_paths[edge])

    ranked_edges = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

    return ranked_edges
