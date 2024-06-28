# This is the LEACH based setup base for clustering of Wireless Sensor Networks

import math
import random
import matplotlib.pyplot as plt

# Constants
NUM_NODES = 100
FIELD_SIZE = 100
P = 0.1  # Probability of becoming a cluster head
MAX_ROUNDS = 10
SINK_NODEX=[50]
SINK_NODEY=[99]
INITIAL_ENERGY=50
TRANSMISSION_ENERGY=0.5





# Function to calculate Euclidean distance
def euclidean_distance(node_array, ch_array):
    return math.sqrt((node_array[0] - ch_array[0])**2 + (node_array[1] - ch_array[1])**2)

# Generate random nodes
nodes = [(round(random.uniform(0, FIELD_SIZE),2), round(random.uniform(0, FIELD_SIZE),2)) for _ in range(NUM_NODES)]

# Nodes which are able to become cluster heads are stored in G ( Make a copy of nodes in G )
G=[item for item in nodes]

# LEACH Algorithm
def leach(G, p, max_rounds, nodes):
    for round in range(max_rounds):
        if not G:
            G=[item for item in nodes]
        threshold=p/(1-p*(round%int(1/p)))
        print(f"Round:{round}, Threshold: {threshold}")
        # Step 1: Cluster Head Selection
        cluster_heads = []
        while len(cluster_heads) == 0:  # Ensure at least one cluster head is selected
            for node in G:
                if random.uniform(0, 1) < threshold:
                    cluster_heads.append(node)
                    G.remove(node)
            print(f"Nodes Variable: {nodes}")
            print(f"Remaining Nodes:{G} \nLength of G is: {len(G)}.")
        # Step 2: Cluster Formation
        clusters = {i: [] for i in range(len(cluster_heads))}
        for node in nodes:
            if node not in cluster_heads:
                # Calculate distances from the current node to all cluster heads
                distances = [euclidean_distance(node, ch) for ch in cluster_heads]
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
        # Plot the nodes on the Graph
        plt.scatter(*zip(*nodes), c='blue', label='Nodes')
        plt.scatter(SINK_NODEX,SINK_NODEY, c="green", label="Sink Node", marker='2', s=500)
       
        # Step 3: Data Transmission (Simplified)
        for ch_index, members in clusters.items():
            cluster_head = cluster_heads[ch_index]
            # Assign Cluster heads coordinate to ch
            
            print(f"Cluster Head {ch_index+1}: {cluster_head}")
            print(f"Number of Members in this cluster: {len(members)}")
            for member in members:
                plt.plot([cluster_head[0], member[0]], [cluster_head[1], member[1]], 'k--')
                print(f"  Node: {member} -> Cluster Head: {cluster_head}")
            # Simulate data aggregation and transmission to base stations
            print(f"Cluster Head {cluster_head} transmits aggregated data to the base station.")
        print(f"Cluster Heads in Round {round} are : {len(cluster_heads)}")
        print("")

        plt.scatter(*zip(*cluster_heads), c='red', label='Cluster Heads')
        plt.legend(bbox_to_anchor=(0.8,1.1) , loc='upper left')
        plt.grid(True)
        plt.savefig(f'Leach Results/leach_round_{round}.png')
        plt.close()


# Run LEACH
leach(G, P, MAX_ROUNDS, nodes)


