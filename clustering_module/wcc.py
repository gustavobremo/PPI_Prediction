import networkx as nx
import os


def clust_coef(G, nodes=None, weight=None):
    """
    Calculate clustering coefficients for nodes in a graph.

    This function calculates clustering coefficients for specified nodes in a graph.

    Args:
        G (networkx.Graph): The input graph.
        nodes (list or None): List of nodes for which to calculate clustering coefficients.
                             If None, calculate for all nodes.
        weight (str or None): Attribute name for edge weights. If None, unweighted.

    Returns:
        dict: Dictionary mapping nodes to their clustering coefficients.
    """
    if nodes is None:
        nodes = G.nodes()
    c = nx.clustering(G, nodes, weight)
    return c


def clustCoef_clusterin(G, weight="weight"):
    """
    Perform clustering of nodes in a graph based on clustering coefficients.

    This function performs clustering of nodes in a graph based on their clustering
    coefficients. It iteratively identifies nodes with the highest coefficient,
    adds them to a cluster, and continues until all nodes are clustered.

    Args:
        G (networkx.Graph): The input graph.
        weight (str): Attribute name for edge weights.

    Returns:
        list: List of clusters, where each cluster is a list of node names.
    """
    if nx.is_weighted(G):
        weight_attribute = weight
    else:
        weight_attribute = None

    clusters = []
    nodes_remaining = list(G.nodes())

    while nodes_remaining:
        v_cc = clust_coef(G, nodes_remaining, weight_attribute)
        sorted_coef = sorted(v_cc.items(), key=lambda item: item[1], reverse=True)
        v = sorted_coef[0][0]
        first_neigh_v = list(G.neighbors(v)) + [v]
        nodes_remaining = list(set(nodes_remaining) - set(first_neigh_v))
        clusters.append(first_neigh_v)

    return clusters


def cluster_network(file_path, saving_folder_path):
    """
    Apply a clustering algorithm to a network and save the results.

    This function reads a weighted edgelist file, applies a clustering algorithm,
    and saves the clustering results.

    Args:
        file_path (str): Path to the weighted edgelist file.
        saving_folder_path (str): Path to the folder for saving clustering results.

    Returns:
        None
    """
    try:
        # Read the weighted edgelist and create a graph
        G = nx.read_weighted_edgelist(file_path, create_using=nx.Graph(), nodetype=str)

        # Apply clustering algorithm
        clusters = clustCoef_clusterin(G)
        clusters.sort(key=len, reverse=True)

        # Extract information from file_path for naming purposes
        prefix_list = file_path.split("/")
        organism = prefix_list[-2].split("_")[-2]
        original_name = os.path.basename(file_path)
        file_name, file_ext = os.path.splitext(original_name)
        algorithm = "wcc"

        # Generate a new filename
        new_filename = f"{file_name}_{organism}_{algorithm}{file_ext}"
        saving_file_path = os.path.join(saving_folder_path, new_filename)

        # Write clusters to the file
        with open(saving_file_path, "w") as output_file:
            for cluster in clusters:
                if len(cluster) >= 3:
                    output_file.write(str(tuple(cluster)) + "\n")

    except FileNotFoundError:
        print(f"File not found: {file_path}")
