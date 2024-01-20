import networkx as nx


def calculate_jaccard_index(graph, source, target):
    """
    Calculate the Jaccard index between nodes in a graph.

    Parameters:
    - graph (NetworkX Graph): The input graph.
    - source (str): The source node.
    - target (str): The target node.

    Returns:
    - jaccard (float): The Jaccard index between the neighborhoods of the source and target nodes.
    """
    neighbors1 = set(graph.neighbors(source))
    neighbors2 = set(graph.neighbors(target))

    intersection_size = len(neighbors1.intersection(neighbors2))
    union_size = len(neighbors1) + len(neighbors2) - intersection_size

    jaccard = intersection_size / union_size if union_size != 0 else 0

    return jaccard


def calculate_jc(graph, complement):
    """
    Calculate Jaccard scores for edges in the complement of a graph.

    Parameters:
    - graph (NetworkX Graph): The original graph.
    - complement (NetworkX Graph): The complement graph.

    Returns:
    - ranked_edges (dict): A dictionary containing edges from the complement graph as keys
      and their corresponding Jaccard scores as values. The dictionary is sorted in descending
      order based on the Jaccard scores.
    """
    results = {}

    for edge in complement.edges():
        source, target = edge
        results[edge] = calculate_jaccard_index(graph=graph, source=source, target=target)

    ranked_edges = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

    return ranked_edges
