import networkx as nx


def preferential_attachment(graph, source, target):
    """
    Calculate Preferential Attachment score between two nodes in a graph.

    Parameters:
    - graph (NetworkX Graph): The input graph.
    - node1 (str): The first node.
    - node2 (str): The second node.

    Returns:
    - pa_score (int): The Preferential Attachment score between the two nodes.
    """
    degree_node1 = graph.degree(source)
    degree_node2 = graph.degree(target)

    pa_score = degree_node1 * degree_node2
    return pa_score


def calculate_pa(graph, complement):
    """
    Calculate Preferential Attachment scores for edges in the complement of a graph.

    Preferential Attachment (PA) is a measure of how likely new connections are to form
    to nodes that already have a high degree.

    Parameters:
    - graph (NetworkX Graph): The original graph.
    - complement (NetworkX Graph): The complement graph.

    Returns:
    - ranked_edges (dict): A dictionary containing edges from the complement graph as keys
      and their corresponding Preferential Attachment scores as values. The dictionary is sorted
      in descending order based on the Preferential Attachment scores.

    """
    results = {}

    for edge in complement.edges():
        source, target = edge
        results[edge] = preferential_attachment(graph=graph, source=source, target=target)

    ranked_edges = dict(sorted(results.items(), key=lambda item: item[1], reverse=True))

    return ranked_edges
