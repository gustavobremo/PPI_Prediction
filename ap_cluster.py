#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:00 2021

@author: gustavobremo

Generat and save subgraph to a new file. 
"""

import networkx as nx
import sklearn as sk
from sklearn.cluster import AffinityPropagation
import numpy as np
from sklearn import cluster
import os


graph_filename = "Ecoli_Cong_Graph_ribosomal"


orga = "Yeast"
percent = "50%"
clustering_algorithm = "AP"

#For the paths files
# data = "yeast_50_red_paths.txt"
# data_file = open(data, "r")
# files = data_file.readlines()

# G = nx.read_weighted_edgelist(file, create_using = nx.Graph(), nodetype = str)
# os.mkdir(orga)


def main_control(files,org,percent,clustering_algorithm):
    
    os.mkdir(org+"/"+percent)
    for f in files:
        f = f.strip()
        main(f,orga,percent,clustering_algorithm)
        # print(f.strip())
        # main(file,orga,percent,clustering_algorithm)



def main(file,organism,percent,clustering_algorithm):
    # print(file)
    # file_path = 
    G = nx.read_weighted_edgelist(file, create_using = nx.Graph(), nodetype = str)
    edge_mat = graph_to_edge_matrix(G)

    results = []
    algorithms = {}

    algorithms['affinity'] = cluster.AffinityPropagation(damping=0.6)

    # Fit all models
    for model in algorithms.values():
        model.fit(edge_mat[0])
        results.append(list(model.labels_))
    
    clust_data = get_clusters(results,edge_mat[1])
    save_clusters(clust_data,file,organism,percent,clustering_algorithm)

def save_clusters(clusters,file,org,percent,clustering):
    
    # 1_10%_reduced_graph.txt
    original_name = file.split("/")[-1]
    new_filename = original_name.split(".")[0]+"_"+org+"_"+clustering+"_clusters.txt"
    # print(new_filename)
    file_namepath = org+"/"+percent+"/"+new_filename
    print(file_namepath)
    with open(file_namepath, "w") as f:
        for c in clusters:
            if len(c) >=3:
                f.write(str(tuple(c)) +"\n")
    f.close()

def get_clusters(clustdata,namedict):

    print(clustdata)
    clusters = {}
    keys_list = list(namedict)

   
    for data in clustdata:
        for i in range(max(data)+1):
            clusters[i] = []
        # print(clusters)

        for i in range(len(data)):
            key = keys_list[i]

            # print(i,key,namedict[key])
            clusters[data[i]].append(key)
        #     x = 0
    
    clusterset = []
    for item in clusters.items():
        clusterset.append(tuple(item[1]))
    
    return(clusterset)



def graph_to_edge_matrix(G):
    # Initialize edge matrix with zeros
    edge_mat = np.zeros((len(G), len(G)), dtype=int)
    namesdic = {}
    counter = 0
    for node in G:
        namesdic[node]= counter
        counter = counter+1  

    # Loop to set 0 or 1 (diagonal elements are set to 1)
    for node in G:
        node_int = namesdic[node]
        for neighbor in G.neighbors(node):
            neighbor_int = namesdic[neighbor]
            edge_mat[node_int][neighbor_int] = 1
        edge_mat[node_int][node_int] = 1

    return edge_mat,namesdic




# main_control(files,orga,percent,clustering_algorithm)