import ap_cluster as ap
import os

def get_reduced_networks_folders(data_folder):
    # Get a list of folders in the directory
    folders = [folder for folder in os.listdir(data_folder) if os.path.isdir(os.path.join(data_folder, folder))]

    return folders

def create_cluster_filepath(clustering_algortihm):

    # Define foldername variable
    foldername = "clustered_networks"

    if not os.path.exists(foldername):
        os.mkdir(foldername)
        working_path = os.path.join(foldername,clustering_algortihm)
        os.mkdir(working_path)
        return working_path
    else:
        print("Folders already exist. Delete them and start again")
    


def main():
    clustering_algortihms = ["ap"]
    # Define foldername variable
    data_folder = "data/A"

    reduced_network_foldernames = get_reduced_networks_folders(data_folder)

    for clustering_algortihm in clustering_algortihms:

        cluster_filepath = create_cluster_filepath(clustering_algortihm)

        for foldername in sorted(reduced_network_foldernames):
            reduced_networks_file_list = os.listdir(os.path.join(data_folder,foldername))
            for reduced_network_filename in sorted(reduced_networks_file_list):
                file_path = os.path.join(data_folder,foldername,reduced_network_filename)
                print(file_path)
            break

main()