
import networkx as nx
import sklearn as sk
from sklearn.cluster import AffinityPropagation
import numpy as np
from sklearn import cluster
import os



def graph_to_edge_matrix(G):
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
    clusters = {}

    for data in clustering_data:
        for i in range(max(data) + 1):
            if i not in clusters:
                clusters[i] = []

        for i, key in enumerate(name_dict):
            clusters[data[i]].append(key)

    return list(clusters.values())


def save_clusters(clusters, file, org, percent, clustering,saving_folder_path):
    original_name = os.path.basename(file)
    file_name, file_ext = os.path.splitext(original_name)
    new_filename = f"{file_name}_{org}_{clustering}_clusters.txt"
    
    saving_file_path = os.path.join(saving_folder_path, new_filename)
    print(saving_file_path)
    
    with open(saving_file_path, "w") as f:
        for c in clusters:
            if len(c) >= 3:
                f.write(str(tuple(c)) + "\n")


def cluster_network(filepath,saving_folder_path):
    prefix_list = filepath.split("/")

    organism = prefix_list[-2].split("_")[-2]
    percent = prefix_list[-2].split("_")[-1]
    algorithm = "ap"

    G = nx.read_weighted_edgelist(filepath, create_using = nx.Graph(), nodetype = str)
    edge_mat = graph_to_edge_matrix(G)

    results = []
    algorithms = {}

    algorithms['affinity'] = cluster.AffinityPropagation(damping=0.6)

    # Fit all models
    for model in algorithms.values():
        model.fit(edge_mat[0])
        results.append(list(model.labels_))
    
    clust_data = get_clusters(results,edge_mat[1])

    save_clusters(clust_data,filepath,organism,percent,algorithm,saving_folder_path)

    
