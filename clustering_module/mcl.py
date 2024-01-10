from markov_clustering import mcl as mcl

import networkx as nx
import sklearn as sk
import numpy as np
from sklearn import cluster
import os


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


def translate_node_ids(clusters, nodes):
    """
    Translate node IDs in clusters to corresponding node names.

    This function takes a list of clusters and a list of node names, translating
    node IDs in clusters to their corresponding node names.

    Args:
        clusters (list): List of clusters, where each cluster is a list of node IDs.
        nodes (list): List of node names.

    Returns:
        list: List of translated clusters, where each cluster is a list of node names.
    """
    translated_clusters = []

    for cluster in clusters:
        translated_cluster = [nodes[node] for node in cluster]
        translated_clusters.append(translated_cluster)

    return translated_clusters


def cluster_network(filepath, saving_folder_path):
    """
    Apply MCL clustering algorithm to a network and save the results.

    This function reads a weighted edgelist file, applies the MCL clustering
    algorithm, and saves the clustering results.

    Args:
        filepath (str): Path to the weighted edgelist file.
        saving_folder_path (str): Path to the folder for saving clustering results.

    Returns:
        None
    """
    # Extract information from the file path for naming purposes
    prefix_list = filepath.split("/")
    organism = prefix_list[-2].split("_")[-2]
    percent = prefix_list[-2].split("_")[-1]
    algorithm = "MCL"

    # Read the weighted edgelist and create a graph
    G = nx.read_weighted_edgelist(filepath, create_using=nx.Graph(), nodetype=str)
    nodeslist = list(G.nodes)

    # Convert the graph to a numpy array
    matrix = nx.to_numpy_array(G)

    # Run MCL clustering algorithm
    result = mcl.run_mcl(matrix)

    # Retrieve clusters
    clusters = mcl.get_clusters(result)

    # Generate a new filename
    original_name = os.path.basename(filepath)
    file_name, file_ext = os.path.splitext(original_name)
    new_filename = f"{file_name}_{organism}_{algorithm}.txt"
    saving_file_path = os.path.join(saving_folder_path, new_filename)

    # Translate node IDs in clusters
    translated_clusters = translate_node_ids(clusters, nodeslist)

    # Save clustering results to a file
    with open(saving_file_path, "w") as f:
        for cluster in translated_clusters:
            if len(cluster) >= 3:
                f.write(str(tuple(cluster)) + "\n")
