import os
from clustering_module import ap 

def get_reduced_networks_folders(data_folder):
    # Get a list of folders in the directory
    folders = [folder for folder in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, folder))]

    return folders

def create_cluster_filepath(clustering_algorithm):
    foldername = "clustered_networks"
    working_path = os.path.join(foldername, clustering_algorithm)

    os.makedirs(working_path, exist_ok=True)

    return working_path
    


def main():
    clustering_algortihms = ["ap"]
    # Define foldername variable
    data_folder = "data/A"

    reduced_network_foldernames = get_reduced_networks_folders(data_folder)

    for clustering_algortihm in clustering_algortihms:

        cluster_folder_path = create_cluster_filepath(clustering_algortihm)

        for foldername in sorted(reduced_network_foldernames):
  
            saving_folder_path = os.path.join(cluster_folder_path,foldername)
            os.makedirs(saving_folder_path, exist_ok=True)

            reduced_networks_file_list = os.listdir(os.path.join(data_folder,foldername))
            for reduced_network_filename in sorted(reduced_networks_file_list):
                file_path = os.path.join(data_folder,foldername,reduced_network_filename)
                ap.cluster_network(file_path,saving_folder_path)
               
  

main()