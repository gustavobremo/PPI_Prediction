import math
import os
import random

import networkx as nx


def read_networks():
    """
    Read network files from 'ppi_networks' folder or create the folder if it doesn't exist.

    Returns:
    - networks (list): List of network files with '.txt' extension found in 'ppi_networks' folder.
    """
    try:
        # Define foldername variable
        foldername = "ppi_networks"

        # List all files in the folder that end with ".txt"
        all_files = os.listdir(foldername)

        # Create a list of network files by joining foldername with file names
        networks = [os.path.join(foldername, f) for f in all_files if f.endswith(".txt")]

        return networks  # Return the list of network files
    except:
        # Create the folder if it doesn't exist
        os.mkdir("ppi_networks")

        # Inform about folder creation and prompt for action
        print("Folder not found!")
        print("A new network folder has been created. Please add network txt files and start again.")


def create_training_data_folders(filename, percentage):
    """
    Create folders for storing training data.

    Args:
    - filename (str): The filename used to generate folder names.
    - percentage (int): The percentage used in folder name generation.

    Returns:
    - reduced_network_folder_path_a (str): Path to folder A containing reduced network.
    - reduced_network_folder_path_b (str): Path to folder B containing removed edges.
    """
    root_data_path = "data"
    a_path = os.path.join(root_data_path, "A")
    b_path = os.path.join(root_data_path, "B")

    # Check if root_data_path exists, if not, create necessary folders
    if not os.path.exists(root_data_path):
        os.mkdir(root_data_path)
        os.mkdir(a_path)
        os.mkdir(b_path)

    # Create folder A containing reduced network
    # Generate folder name based on filename and percentage
    foldername_a = "".join(filename.split("/")[1].split("_")[0:2]) + "_" + str(percentage) + "%"
    reduced_network_folder_path_a = os.path.join(a_path, foldername_a)
    os.mkdir(reduced_network_folder_path_a)

    # Create folder B containing removed edges (similar to folder A)
    foldername_b = "".join(filename.split("/")[1].split("_")[0:2]) + "_" + str(percentage) + "%"
    reduced_network_folder_path_b = os.path.join(b_path, foldername_b)
    os.mkdir(reduced_network_folder_path_b)

    return reduced_network_folder_path_a, reduced_network_folder_path_b


def edge_removal(G, percent, number_of_components, i):
    """
    Reduce the graph by removing edges.

    Args:
    - G (networkx.Graph): The input graph.
    - percent (float): Percentage of edges to be removed.
    - number_of_components (int): Number of components expected after edge removal.
    - i (int): Iteration number.

    Returns:
    - Current_graph (networkx.Graph): The final reduced graph.
    - removed_set (networkx.Graph): Set of removed edges.
    """
    nx.freeze(G)
    e = nx.number_of_edges(G)  # Number of edges in the original graph
    bridges = set(nx.bridges(G))  # Get the edges that are bridges
    edgeset = set(G.edges())  # Use sets for faster lookup

    # Removing the bridges from the edge set
    edge_list = edgeset - bridges  # Candidate set

    edge_remove_number = math.floor((percent * e) / 100)  # Total edges to remove

    removed_set = set()  # Contains the final removed set
    Current_graph = G.copy()  # Graph containing the final reduced graph

    while len(removed_set) != edge_remove_number:
        print(
            f"Generating graph {percent}%: {i + 1}... {math.floor(len(removed_set) * 100 / edge_remove_number)}%"
        )

        G_temp = Current_graph.copy()  # Copy the current graph

        random_e = random.sample(edge_list, 1)[0]  # Select a random edge from the candidate set

        G_temp.remove_edges_from([random_e])  # Remove the sampled edge

        total_components = nx.number_connected_components(G_temp)  # Get total components

        if total_components == number_of_components:  # If component numbers remain equal
            removed_set.add(random_e)  # Add edge to removed_set
            edge_list.remove(random_e)  # Remove the edge from the candidate set
            Current_graph = G_temp  # Update current_graph with the reduced graph

    removed_set = nx.Graph(list(removed_set))  # Convert removed edge set to a graph

    return Current_graph, removed_set


def main():
    """
    Perform edge removal and create reduced graphs along with removed edge sets.

    Reads network files, generates reduced graphs, and stores results in output files.
    """
    # Percentage edge removal list
    percentages = [10, 15, 20, 50]

    # Represent the number of graphs generated with removed edges from a single set
    replicates = 10

    network_filenames = read_networks()

    for network_filename in network_filenames:
        G = nx.read_weighted_edgelist(network_filename, create_using=nx.Graph(), nodetype=str)
        # Freezing original graph
        nx.freeze(G)
        # Get the number of components
        components = nx.number_connected_components(G)

        for percentage in percentages:
            # Create training data folders
            a_path, b_path = create_training_data_folders(network_filename, percentage)

            for i in range(replicates):
                reduced_network_filename = f"{i + 1}_{percentage}%_reduced_graph.txt"
                removed_edges_filename = f"{i + 1}_{percentage}%_removed_edges.txt"

                reduced_network_filepath = os.path.join(a_path, reduced_network_filename)
                removed_edges_filepath = os.path.join(b_path, removed_edges_filename)

                # Making a copy of the original graph
                G_temp = G.copy()

                # Call "edge_removal" function to remove edges from the graph
                output_graph_and_edges = edge_removal(G_temp, percentage, components, i)

                reduced_graph = output_graph_and_edges[0]
                removed_edges = output_graph_and_edges[1]

                # Store output graph and removed edge set as edgelist output file
                nx.write_weighted_edgelist(reduced_graph, reduced_network_filepath)
                nx.write_weighted_edgelist(removed_edges, removed_edges_filepath)


main()
