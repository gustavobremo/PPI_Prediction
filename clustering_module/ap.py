import os

import networkx as nx
import numpy as np
import sklearn as sk
from sklearn import cluster
from sklearn.cluster import AffinityPropagation


def graph_to_edge_matrix(G):
    """
    Convert a graph to an edge matrix.

    This function takes a graph and converts it into an edge matrix, where rows
    and columns represent nodes, and the matrix elements indicate the presence
    of edges between nodes.

    Args:
        G (networkx.Graph): The input graph.

    Returns:
        tuple: A tuple containing the edge matrix and a dictionary mapping
               node names to their corresponding matrix indices.
    """
    num_nodes = len(G)
    edge_mat = np.zeros((num_nodes, num_nodes), dtype=int)
    node_indices = {node: i for i, node in enumerate(G.nodes)}

    for node in G.nodes:
        node_int = node_indices[node]
        edge_mat[node_int][node_int] = 1  # Set diagonal elements to 1
        for neighbor in G.neighbors(node):
            neighbor_int = node_indices[neighbor]
            edge_mat[node_int][neighbor_int] = 1

    return edge_mat, node_indices


def get_clusters(clustering_data, name_dict):
    """
    Organize nodes into clusters based on clustering results.

    This function takes clustering results and a dictionary mapping node names
    to their corresponding matrix indices. It organizes nodes into clusters
    based on the clustering results.

    Args:
        clustering_data (list): List of clustering results.
        name_dict (dict): Dictionary mapping node names to matrix indices.

    Returns:
        list: List of clusters, where each cluster is a list of node names.
    """
    clusters = {}

    for data in clustering_data:
        for i in range(max(data) + 1):
            if i not in clusters:
                clusters[i] = []

        for i, key in enumerate(name_dict):
            clusters[data[i]].append(key)

    return list(clusters.values())


def save_clusters(clusters, file, org, percent, clustering, saving_folder_path):
    """
    Save clustering results to a file.

    This function takes a list of clusters and saves them to a file in the
    specified folder. The filename includes information about the original file,
    organism, and clustering algorithm.

    Args:
        clusters (list): List of clusters to be saved.
        file (str): Path to the original file.
        org (str): Organism information.
        percent (str): Percent information.
        clustering (str): Clustering algorithm used.
        saving_folder_path (str): Path to the folder for saving clustering results.

    Returns:
        None
    """
    # Extract information from the file path for naming purposes
    original_name = os.path.basename(file)
    file_name, file_ext = os.path.splitext(original_name)

    # Create a new filename with relevant information
    new_filename = f"{file_name}_{org}_{clustering}.txt"
    saving_file_path = os.path.join(saving_folder_path, new_filename)

    # Write clusters to the file
    with open(saving_file_path, "w") as f:
        for c in clusters:
            if len(c) >= 3:
                f.write(str(tuple(c)) + "\n")


def cluster_network(filepath, saving_folder_path):
    """
    Apply clustering algorithms to a network and save the results.

    This function reads a weighted edgelist file, applies the Affinity
    Propagation clustering algorithm, and saves the clustering results.

    Args:
        filepath (str): Path to the weighted edgelist file.
        saving_folder_path (str): Path to the folder for saving clustering results.

    Returns:
        None
    """
    # Extract information from file path for naming purposes
    prefix_list = filepath.split("/")
    organism = prefix_list[-2].split("_")[-2]
    percent = prefix_list[-2].split("_")[-1]
    algorithm = "ap"

    # Read the weighted edgelist and convert to edge matrix
    G = nx.read_weighted_edgelist(filepath, create_using=nx.Graph(), nodetype=str)
    edge_mat = graph_to_edge_matrix(G)

    # Initialize clustering algorithms
    algorithms = {"affinity": cluster.AffinityPropagation(damping=0.6)}

    results = []

    # Fit all models
    for model in algorithms.values():
        model.fit(edge_mat[0])
        results.append(list(model.labels_))

    # Extract cluster data
    clust_data = get_clusters(results, edge_mat[1])

    # Save clustering results
    save_clusters(clust_data, filepath, organism, percent, algorithm, saving_folder_path)
