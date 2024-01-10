import os

from clustering_module import ap, clusterone, imhrc, mcl, wcc


def get_reduced_networks_folders(data_folder):
    """
    Get a list of folders in the specified directory.

    Args:
        data_folder (str): Path to the directory containing folders.

    Returns:
        list: List of folder names in the specified directory.
    """
    # Get a list of folders in the directory
    folders = [
        folder
        for folder in os.listdir(data_folder)
        if os.path.isdir(os.path.join(data_folder, folder))
    ]

    return folders


def create_cluster_filepath(clustering_algorithm):
    """
    Create a filepath for saving clustering results based on the clustering algorithm.

    Args:
        clustering_algorithm (str): The clustering algorithm.

    Returns:
        str: The path for saving clustering results.
    """
    # Define the parent folder for clustered networks
    foldername = "clustered_networks"

    # Create a path specific to the clustering algorithm
    working_path = os.path.join(foldername, clustering_algorithm)

    # Ensure the path exists, or create it
    os.makedirs(working_path, exist_ok=True)

    return working_path


def main():
    """
    Execute clustering algorithms on reduced networks in a specified folder.

    This function iterates over available clustering algorithms and applies them
    to reduced networks in the specified data folder. The results are saved in
    folders corresponding to each clustering algorithm.

    Args:
        None

    Returns:
        None
    """
    # Define clustering functions and corresponding algorithms
    clustering_functions = {
        "ap": ap.cluster_network,
        "imhrc": imhrc.cluster_network,
        "clusterone": clusterone.cluster_network,
        "mcl": mcl.cluster_network,
        "wcc": wcc.cluster_network,
    }

    # List of available clustering algorithms
    clustering_algorithms = list(clustering_functions.keys())

    # Data folder path
    data_folder = "data/A"

    # Get a list of reduced network folder names
    reduced_network_folder_names = get_reduced_networks_folders(data_folder)

    # Iterate over clustering algorithms
    for clustering_algorithm in clustering_algorithms:
        # Create a path for saving clustering results
        cluster_folder_path = create_cluster_filepath(clustering_algorithm)

        # Iterate over reduced network folders
        for folder_name in sorted(reduced_network_folder_names):
            # Change to the current directory
            os.chdir(".")

            # Create a path for saving clustering results for the current network folder
            saving_folder_path = os.path.join(cluster_folder_path, folder_name)
            os.makedirs(saving_folder_path, exist_ok=True)

            # Get a list of reduced network files in the current folder
            reduced_networks_file_list = [
                network
                for network in os.listdir(os.path.join(data_folder, folder_name))
                if network.endswith(".txt")
            ]

            # Iterate over reduced network files
            for reduced_network_filename in sorted(reduced_networks_file_list):
                # Create a full file path for the current reduced network file
                file_path = os.path.join(data_folder, folder_name, reduced_network_filename)

                # Apply the selected clustering algorithm to the current network file
                clustering_functions[clustering_algorithm](file_path, saving_folder_path)

                break
            break


main()
