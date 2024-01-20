import os

import networkx as nx

from similarity import cn, jc, l3, pa, ra


def get_folders(path):
    folders = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
    return folders


def get_complement(filepath):
    G = nx.read_weighted_edgelist(filepath, create_using=nx.Graph(), nodetype=str)
    # Get the complement of the graph
    complement_G = nx.complement(G)

    return G, complement_G


def viewdict(filepath, dictionary):
    print(filepath)
    for keys, values in dictionary.items():
        print(keys, values)
    print("\n")


def rank_edges():
    data_path_a = "data/A"
    data_path_b = "data/B"
    data_folders = sorted(get_folders(data_path_a))

    # Define similarity functions and corresponding algorithms
    similarity_functions = {
        "cn": cn.calculate_cn,
        "jc": jc.calculate_jc,
        "pa": pa.calculate_pa,
        "ra": ra.calculate_ra,
        "l3": l3.calculate_l3,
    }

    # List of available clustering algorithms
    similarity_algorithms = list(similarity_functions.keys())

    for similarity_algorithm in similarity_algorithms:
        for folder in data_folders:
            folder_path = os.path.join(data_path_a, folder)
            a_reduced_graph_files = os.listdir(folder_path)

            for file_path in sorted(a_reduced_graph_files):
                graph_full_path = os.path.join(folder_path, file_path)
                graph, complement_graph = get_complement(graph_full_path)

                print(similarity_algorithm, graph_full_path)

                ranked_edges = similarity_functions[similarity_algorithm](graph, complement_graph)

                viewdict(graph_full_path, ranked_edges)

                # break
            break
        break


rank_edges()