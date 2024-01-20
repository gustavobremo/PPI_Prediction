import networkx as nx


def resource_allocation(graph, source, target):
    """
    Calculate Resource Allocation score between two nodes in a graph.

    Parameters:
    - graph (NetworkX Graph): The input graph.
    - node1 (str): The first node.
    - node2 (str): The second node.

    Returns:
    - ra_score (float): The Resource Allocation score between the two nodes.
    """
    neighbors_node1 = set(graph.neighbors(source))
    neighbors_node2 = set(graph.neighbors(target))

    common_neighbors = neighbors_node1.intersection(neighbors_node2)

    ra_score = (
        sum(1 / graph.degree(neighbor) for neighbor in common_neighbors) if common_neighbors else 0
    )

    return ra_score


def calculate_ra(graph, complement):
    """
    Calculate Resource Allocation scores for edges in the complement of a graph.

    Resource Allocation (RA) is a measure of the shared resources between two nodes in a network.
    The RA score between two nodes is calculated as the sum of the inverse degrees of their common neighbors.

    Parameters:
    - graph (NetworkX Graph): The original graph.
    - complement (NetworkX Graph): The complement graph.

    Returns:
    - ranked_edges (dict): A dictionary containing edges from the complement graph as keys
      and their corresponding Resource Allocation scores as values. The dictionary is sorted
      in descending order based on the Resource Allocation scores.


    Note:
    - The Resource Allocation score for an edge is calculated as the sum of the inverse degrees
      of the common neighbors of the source and target nodes.
    """
    results = {}

    for edge in complement.edges():
        source, target = edge
        results[edge] = resource_allocation(graph=graph, source=source, target=target)

    ranked_edges = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

    return ranked_edges
