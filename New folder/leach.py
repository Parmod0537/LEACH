'''
    This is the LEACH based setup base for clustering of Wireless Sensor Networks 
'''

import random
import math

# Constants
NUM_NODES = 20
FIELD_SIZE = 100
P = 0.1  # Probability of becoming a cluster head
MAX_ROUNDS = 10

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
        
        print ("thisis random line")        
        # Step 3: Data Transmission (Simplified)
        for ch_index, members in clusters.items():
            cluster_head = cluster_heads[ch_index]
            print(f"Cluster Head {ch_index+1}: {cluster_head}")
            print(f"Number of Members in this cluster: {len(members)}")
            for member in members:
                print(f"  Node: {member} -> Cluster Head: {cluster_head}")
            # Simulate data aggregation and transmission to base station
            print(f"Cluster Head {cluster_head} transmits aggregated data to the base station.")
        print(f"Cluster Heads in Round {round} are : {len(cluster_heads)}")
        print("")
# Run LEACH
leach(G, P, MAX_ROUNDS, nodes)

