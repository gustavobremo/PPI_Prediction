from markov_clustering import mcl as mcl

import networkx as nx
import sklearn as sk
import numpy as np
from sklearn import cluster
import os



def get_clusters(clustering_data, name_dict):
    clusters = {}

    for data in clustering_data:
        for i in range(max(data) + 1):
            if i not in clusters:
                clusters[i] = []

        for i, key in enumerate(name_dict):
            clusters[data[i]].append(key)

    return list(clusters.values())


def translate_node_ids(clusters, nodes):
    translated_clusters = []

    for cluster in clusters:
        translated_cluster = [nodes[node] for node in cluster]
        translated_clusters.append(translated_cluster)

    return translated_clusters


def cluster_network(filepath,saving_folder_path):
    prefix_list = filepath.split("/")

    organism = prefix_list[-2].split("_")[-2]
    percent = prefix_list[-2].split("_")[-1]
    algorithm = "MCL"

    # Get graph
    G = nx.read_weighted_edgelist(filepath, create_using = nx.Graph(), nodetype = str)
    nodeslist = list(G.nodes)

    matrix = nx.to_numpy_array(G)
    # Run mcl clustering 
    result = mcl.run_mcl(matrix)
    # Retrieve clusters
    clusters = mcl.get_clusters(result)


    original_name = os.path.basename(filepath)
    file_name, file_ext = os.path.splitext(original_name)
    new_filename = f"{file_name}_{organism}_{algorithm}.txt"
    saving_file_path = os.path.join(saving_folder_path, new_filename)

    
    translated_clusters = translate_node_ids(clusters,nodeslist)

    with open(saving_file_path, "w") as f:
            for cluster in translated_clusters:
                if len(cluster) >= 3:
                    f.write(str(tuple(cluster)) + "\n")