'''
    This is the LEACH based setup base for clustering of Wireless Sensor Networks

'''

import math
import random

from matplotlib import pyplot as plt

# Constants
NUM_NODES = 100
FIELD_SIZE = 100
P = 0.1  # Probability of becoming a cluster head
MAX_ROUNDS = 10
SINK_NODEX=[50]
SINK_NODEY=[99]
INITIAL_ENERGY=0.5
TRANSMISSION_ENERGY=0.005
E_ELEC = 50e-9
E_FS = 10e-12       # Energy consumed in Free Space model
E_MP = 0.0013e-12       # Energy consumed in Multipath model
D0 = math.sqrt(E_FS/E_MP)       # Threshold distance between two nodes
K=4000      # Size of message in bits

# Function to calculate Euclidean distance
def euclidean_distance(node_array, ch_array):
    return math.sqrt((node_array[0] - ch_array[0])**2 + (node_array[1] - ch_array[1])**2)

# Generate random nodes
nodes = [(round(random.uniform(0, FIELD_SIZE),2), round(random.uniform(0, FIELD_SIZE),2)) for _ in range(NUM_NODES)]

node_energy=[[node,INITIAL_ENERGY] for node in nodes]

# Nodes which are able to become cluster heads are stored in G ( Make a copy of nodes in G )
G=[item for item in node_energy]

# Nodes which do not have energy left to transmit data are stored here
dissipated_nodes=[]


# LEACH Algorithm
def leach(G, p, max_rounds, node_energy):
    for round in range(max_rounds):
        
        if not G:
            G=[item for item in node_energy]
        threshold=p/(1-p*(round%int(1/p)))

        for node in G:
            for nod in node_energy:
                if node[0] == nod[0]:
                    G[G.index(node)] = nod

        print(f"Round:{round}, Threshold: {threshold}")
        # Step 1: Cluster Head Selection
        cluster_heads = []
        while len(cluster_heads) == 0:  # Ensure at least one cluster head is selected
            for node in G:
                if random.uniform(0, 1) < threshold:
                    cluster_heads.append(node)
                    G.remove(node)
        
        print(f"Nodes Variable: {node_energy}")
        print(f"Remaining Nodes:{G} \nLength of G is: {len(G)}.")

        # Step 2: Cluster Formation
        clusters = {i: [] for i in range(len(cluster_heads))}
        for node in node_energy:
            if node not in cluster_heads:
                # Calculate distances from the current node to all cluster heads
                distances = [euclidean_distance(node[0], ch[0]) for ch in cluster_heads]
                if distances:  # Ensure distances list is not empty
                    # Find the index of the nearest cluster head
                    nearest_ch_index = distances.index(min(distances))
                    # Assign the current node to the nearest cluster head's cluster
                    clusters[nearest_ch_index].append(node)
                    
        print(f"Value in Cluster Variable : {clusters}")
        
        plt.figure(figsize=(10,10))
        plt.xlim(0, FIELD_SIZE)
        plt.ylim(0, FIELD_SIZE)
        plt.title(f"LEACH Clustering - Round {round}")
        plt.xlabel("X-coordinate")
        plt.ylabel("Y-coordinate")
        
        
        # Step 3: Data Transmission (Simplified)
        for ch_index, members in clusters.items():
            cluster_head = cluster_heads[ch_index]
            # Assign Cluster heads coordinate to ch 
            
            print(f"Cluster Head {ch_index+1}: {cluster_head}")
            print(f"Number of Members in this cluster: {len(members)}")
            for member,energy in members:
                distance = euclidean_distance(member,cluster_head[0])
                if distance < D0:
                    energy_consumed= (E_ELEC * K) + (E_FS * K *(distance ** 2))
                else:
                    energy_consumed= (E_ELEC * K) + (E_MP * K *(distance ** 4))
                energy -= energy_consumed
                node_energy[nodes.index(member)]=(member,energy)
                print(f"  Node: {member}, Energy Left: {energy} -> Cluster Head: {cluster_head}")
                
            # Simulate data aggregation and transmission to base station
            print(f"Cluster Head {cluster_head} transmits aggregated data to the base station.")
            ch_energy = cluster_head[1] - TRANSMISSION_ENERGY
            node_energy[nodes.index(cluster_head[0])]=(cluster_head[0],ch_energy)
            #cluster_heads[ch_index] ---- Cluster Head coordinates and energy
            print(f"After Transmission  Cluster Head {cluster_head} , Energy Left: {cluster_head[1]}")
        print(f"Cluster Heads in Round {round} are : {len(cluster_heads)}")
        print("")

        def plot_nodes(node_energy):
            # Array X and Y containing coordinates only x and y for nodes
            x = [node[0][0] for node in node_energy]
            y = [node[0][1] for node in node_energy]
            # Array xch and ych containing coordinates only x and y for cluster heads
            xch = [node[0][0] for node in cluster_heads]
            ych = [node[0][1] for node in cluster_heads]
            
            plt.figure(figsize=(10, 10))
            # plot lines to show which node is related to which cluster head
            for ch_index, members in clusters.items():
                cluster_head = cluster_heads[ch_index]
                for member in members:
                    plt.plot([cluster_head[0][0], member[0][0]], [cluster_head[0][1], member[0][1]], 'k--')
            
            # Plot the nodes as blue dots and cluster heads as red dots
            plt.scatter(x, y,  c='blue', label="Nodes")
            plt.scatter(xch, ych,  c='red', label="Cluster Heads")
            
            # Adding sink node
            plt.scatter(SINK_NODEX, SINK_NODEY, c="green", label="Sink Node", marker='2', s=500)

            # Plot settings
            plt.xlim(0, FIELD_SIZE)
            plt.ylim(0, FIELD_SIZE)
            plt.title(f"LEACH Clustering - Round {round}")
            plt.xlabel("X-coordinate")
            plt.ylabel("Y-coordinate")
            # Get the legend out of the plot
            plt.legend(bbox_to_anchor=(0.8,1.1) , loc='upper left')
            plt.grid(True)
            plt.savefig(f'leach_round_data_{round}.png')
            plt.close()

        plot_nodes(node_energy)


# Run LEACH
leach(G, P, MAX_ROUNDS, node_energy)

