import os
import subprocess


def cluster_network(filepath, saving_folder_path):
    """
    Clusters a network using ClusterONE algorithm and saves the results to a text file.

    Args:
    filepath (str): Path to the input network file.
    saving_folder_path (str): Path to the folder where the clustered results will be saved.

    Raises:
    subprocess.CalledProcessError: If an error occurs while running the Java subprocess.

    Note:
    The function uses the ClusterONE-v1.0.jar file located in the 'clustering_module' directory.
    The output is saved as a text file with the clustered results.
    """
    # Define the absolute path to the ClusterONE JAR file
    absolute_path_jar_file = os.path.join(os.path.abspath("clustering_module"), "ClusterONE-v1.0.jar")

    # Extract details from the filepath
    prefix_list = filepath.split("/")
    organism = prefix_list[-2].split("_")[-2]
    algorithm = "clusterone"

    # Prepare the new filename for the clustered results
    original_name = os.path.basename(filepath)
    file_name, file_ext = os.path.splitext(original_name)
    new_filename = f"{file_name}_{organism}_{algorithm}.txt"

    try:
        # Run the ClusterONE Java subprocess and capture the output
        result = subprocess.run(["java", "-jar", absolute_path_jar_file, filepath], stdout=subprocess.PIPE, text=True)
        output = result.stdout.split("\n")

        # Define the path for saving the clustered results
        saving_path = os.path.join(saving_folder_path, new_filename)

        # Write the clustered results to a text file
        with open(saving_path, 'w') as file:
            for cluster in output:
                if cluster:
                    tuple_cluster = str(tuple(cluster.split("\t")))
                    file.write(f"{tuple_cluster}\n")
    except subprocess.CalledProcessError as e:
        raise subprocess.CalledProcessError(f"Error occurred: {e}")



 