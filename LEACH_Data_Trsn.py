# This is the LEACH based setup base for clustering of Wireless Sensor Networks

import math
import random
import matplotlib.pyplot as plt

NODE_COUNT = 20
FIELD_SIZE = 100
CLUSTER_HEAD_PROBABILITY = 0.1
MAX_ROUNDS = 10
SINK_NODE=[50, 99]
INITIAL_ENERGY=0.5
TRANSMISSION_ENERGY=0.005
E_ELEC = 50e-9
E_FS = 10e-12       # Energy consumed in Free Space model
E_MP = 0.0013e-12       # Energy consumed in Multipath model
THRESH_DIST = math.sqrt(E_FS/E_MP)
MSG_SIZE =4000

def euclidean_distance(node_array, ch_array):
    return math.sqrt((node_array[0] - ch_array[0])**2 + (node_array[1] - ch_array[1])**2)

def plot_nodes(node_energy, cluster_heads, clusters, round):

    nodes = [(node[0][0], node[0][1]) for node in node_energy]
    cluster_heads = [(node[0][0], node[0][1]) for node in cluster_heads]
    
    plt.figure(figsize=(10, 10))
    
    # plot lines to show which node is related to which cluster head
    for ch_index, members in clusters.items():
        cluster_head = cluster_heads[ch_index]
        for member in members:
            plt.plot([cluster_head[0], member[0][0]], [cluster_head[1], member[0][1]], 'k--')
    
    # Plot the nodes as blue dots and cluster heads as red dots
    plt.scatter(nodes[0], nodes[1],  c = 'blue', label = "Nodes")
    plt.scatter(cluster_heads[0][0], cluster_heads[0][1],  c = 'red', label = "Cluster Heads")
    
    # Adding sink node
    plt.scatter(SINK_NODE[0], SINK_NODE[1], c = "green", label = "Sink Node", marker = '2', s = 500)

    # Plot settings
    plt.xlim(0, FIELD_SIZE)
    plt.ylim(0, FIELD_SIZE)
    plt.title(f"LEACH Clustering - Round {round}")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    
    # Get the legend out of the plot
    plt.legend(bbox_to_anchor = (0.8,1.1) , loc = 'upper left')
    plt.grid(True)
    plt.savefig(f'leach_round_data_{round}.png')
    plt.close()

def leach(cluster_head_nodes , p, max_rounds, node_energy):
    for round in range(max_rounds):
        
        if not cluster_head_nodes :
            cluster_head_nodes = [item for item in node_energy]
        threshold = p/(1-p*(round%int(1/p)))

        for node in cluster_head_nodes :
            for nod in node_energy:
                if node[0] == nod[0]:
                    cluster_head_nodes[cluster_head_nodes .index(node)] = nod

        print(f"Round:{round}, Threshold: {threshold}")
        
        cluster_heads = []
        while len(cluster_heads) == 0: 
            for node in cluster_head_nodes :
                if random.uniform(0, 1) < threshold:
                    cluster_heads.append(node)
                    cluster_head_nodes .remove(node)
        
        print(f"Nodes Variable: {node_energy}")
        print(f"Remaining Nodes:{cluster_head_nodes } \nLength of cluster_head_nodes  is: {len(cluster_head_nodes )}.")

        clusters = {i: [] for i in range(len(cluster_heads))}
        for node in node_energy:
            if node not in cluster_heads:
                distances = [euclidean_distance(node[0], ch[0]) for ch in cluster_heads]
                if distances: 
                    nearest_cluster_head_index = distances.index(min(distances))
                    clusters[nearest_cluster_head_index].append(node)
                    
        print(f"Value in Cluster Variable : {clusters}")
        
        plt.figure(figsize=(10,10))
        plt.xlim(0, FIELD_SIZE)
        plt.ylim(0, FIELD_SIZE)
        plt.title(f"LEACH Clustering - Round {round}")
        plt.xlabel("X-coordinate")
        plt.ylabel("Y-coordinate")
        
        for ch_index, members in clusters.items():
            cluster_head = cluster_heads[ch_index]
            
            print(f"Cluster Head {ch_index+1}: {cluster_head}")
            print(f"Number of Members in this cluster: {len(members)}")
            for member,energy in members:
                distance = euclidean_distance(member,cluster_head[0])
                if distance < THRESH_DIST:
                    energy_consumed = (E_ELEC * MSG_SIZE) + (E_FS * MSG_SIZE *(distance ** 2))
                else:
                    energy_consumed = (E_ELEC * MSG_SIZE) + (E_MP * MSG_SIZE *(distance ** 4))
                energy -= energy_consumed
                node_energy[nodes.index(member)] = (member,energy)
                print(f"  Node: {member}, Energy Left: {energy} -> Cluster Head: {cluster_head}")
                
            print(f"Cluster Head {cluster_head} transmits aggregated data to the base station.")
            ch_energy = cluster_head[1] - TRANSMISSION_ENERGY
            node_energy[nodes.index(cluster_head[0])] = (cluster_head[0],ch_energy)
            #cluster_heads[ch_index] ---- Cluster Head coordinates and energy
            print(f"After Transmission  Cluster Head {cluster_head} , Energy Left: {cluster_head[1]}")
        print(f"Cluster Heads in Round {round} are : {len(cluster_heads)}")
        print("")
        plot_nodes(node_energy, cluster_heads, clusters, round)

# Generate random nodes
nodes = [(round(random.uniform(0, FIELD_SIZE), 2), round(random.uniform(0, FIELD_SIZE), 2)) for _ in range(NODE_COUNT)]

node_energy = [[node, INITIAL_ENERGY] for node in nodes]
cluster_head_nodes = [item for item in node_energy]
dissipated_nodes = []

leach(cluster_head_nodes, CLUSTER_HEAD_PROBABILITY, MAX_ROUNDS, node_energy)