import os
import subprocess
import shutil


def copy_temp_file(filepath):
    """
    Copies a network temp file to the current working directory.

    Args:
    - filepath (str): Path of the file to be copied.

    Returns:
    - str: Path of the copied file in the current working directory.
    """
    try:
        # Source file path (file to be copied)
        source_file = filepath

        # Destination file path (where the file will be copied)
        destination_folder = os.path.abspath(".")  # Replace with the desired destination file path

        # Copy the file from source to destination
        shutil.copy(source_file, destination_folder)

        return os.path.join(destination_folder, os.path.basename(filepath))
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except PermissionError:
        print(f"Error: Permission denied while copying '{filepath}'.")
    except Exception as e:
        print(f"An error occurred: {e}")


# def save_clusters(filepath,temp_filepath,temp_filename,saving_folder_path):

#     # Extract details from the filepath
#     prefix_list = filepath.split("/")
#     organism = prefix_list[-2].split("_")[-2]
#     algorithm = "IMHRC"

#     # Prepare the new filename for the clustered results
#     original_name = os.path.basename(filepath)
#     file_name, file_ext = os.path.splitext(original_name)
#     new_filename = f"{file_name}_{organism}_{algorithm}.txt"

#     cluster_tmp_path = temp_filepath.split("imhrc")[0]

#     # list all txt cusltered network files
#     cluster_folder = "imhrc\\IMHRC"
#     # abspathclusterfolder = os.path.abspath(os.path.join(cluster_tmp_path,cluster_folder))
#     abspathclusterfolder = os.path.abspath(cluster_tmp_path)
#     cluster_file = cluster_folder+temp_filename
#     file_list = [f for f in os.listdir(cluster_tmp_path) if temp_filename in f]

#     clusterfolderpath = abspathclusterfolder+"/"+cluster_folder
#     fileclusterpath = abspathclusterfolder+"/"+file_list[0]

#     shutil.rmtree(clusterfolderpath)

#     cluster_output = []
#     # Open the file in read mode
#     with open(fileclusterpath, 'r') as file:
#         # Read each line using a loop
#         for line in file:
#             cluster = tuple(line.strip().split("\t"))
#             cluster_output.append(cluster)

#     saving_path = os.path.join(saving_folder_path,new_filename)
#     with open(saving_path, 'w') as file:
#         for cluster in cluster_output:
#             file.write(f"{cluster}\n")


#     os.remove(fileclusterpath)
def save_clusters(input_filepath, temp_filepath, temp_filename, output_folder_path):
    # Extract details from the input filepath
    filepath_parts = input_filepath.split("/")
    organism = filepath_parts[-2].split("_")[-2]
    algorithm = "IMHRC"

    # Create a new filename for the clustered results
    original_filename = os.path.basename(input_filepath)
    filename_no_ext, file_extension = os.path.splitext(original_filename)
    new_filename = f"{filename_no_ext}_{organism}_{algorithm}.txt"

    # Extract cluster temporary path
    cluster_tmp_path = temp_filepath.split("imhrc")[0]

    # Find the cluster files
    cluster_folder = "imhrc\\IMHRC"
    abspath_cluster_tmp = os.path.abspath(cluster_tmp_path)
    cluster_file_pattern = cluster_folder + temp_filename
    cluster_files = [f for f in os.listdir(cluster_tmp_path) if temp_filename in f]

    # Define paths
    cluster_folder_path = os.path.join(abspath_cluster_tmp, cluster_folder)
    file_cluster_path = os.path.join(abspath_cluster_tmp, cluster_files[0])

    # Remove temporary cluster folder
    shutil.rmtree(cluster_folder_path)

    # Extract clusters from the file
    cluster_output = []
    with open(file_cluster_path, "r") as file:
        for line in file:
            cluster = tuple(line.strip().split("\t"))
            cluster_output.append(cluster)

    # Save clusters to a new file
    output_path = os.path.join(output_folder_path, new_filename)
    with open(output_path, "w") as file:
        for cluster in cluster_output:
            file.write(f"{cluster}\n")

    # Remove temporary cluster file
    os.remove(file_cluster_path)


def cluster_network(filepath, saving_folder_path):
    """
    Cluster a network file and save the results.

    Args:
    - filepath (str): Path to the network file to be clustered.
    - saving_folder_path (str): Folder path to save the clustered results.

    Returns:
    - None
    """
    abs_filepath = os.path.abspath(filepath)
    root = abs_filepath.split("data")[0]
    working = os.path.join(root, "clustering_module/imhrc")
    clustering_module_path = os.path.join(root, "clustering_module")
    abs_saving_path = os.path.abspath(saving_folder_path)

    os.chdir(working)

    # Create a temp copy of the network to cluster
    temp_filepath = copy_temp_file(abs_filepath)
    temp_filename = temp_filepath.split("/")[-1]

    subprocess.call(["java", "-jar", "IMHRC-V1.jar", temp_filename])

    os.remove(temp_filename)

    save_clusters(filepath, temp_filepath, temp_filename, abs_saving_path)

    os.chdir(root)
