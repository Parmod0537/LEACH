# '''
#     This is the LEACH based setup base for clustering of Wireless Sensor Networks

# '''

# import random
# import math
# from matplotlib import pyplot as plt
# # Constants
# NUM_NODES = 20
# FIELD_SIZE = 100
# P = 0.1  # Probability of becoming a cluster head
# MAX_ROUNDS = 10
# SINK_NODEX=[50]
# SINK_NODEY=[99]
# INITIAL_ENERGY=50
# TRANSMISSION_ENERGY=0.5


# # Function to calculate Euclidean distance
# def euclidean_distance(node_array, ch_array):
#     return math.sqrt((node_array[0][0] - ch_array[0][0])**2 + (node_array[0][1] - ch_array[0][1])**2)

# # Generate random nodes
# nodes = [(round(random.uniform(0, FIELD_SIZE),2), round(random.uniform(0, FIELD_SIZE),2)) for _ in range(NUM_NODES)]

# node_energy=[[node,INITIAL_ENERGY] for node in nodes]

# # Nodes which are able to become cluster heads are stored in G ( Make a copy of nodes in G )
# G=[item for item in node_energy]

# # Nodes which do not have energy left to transmit data are stored here
# dissipated_nodes=[]


# # LEACH Algorithm
# def leach(G, p, max_rounds, node_energy):
#     for round in range(max_rounds):
        
#         if not G:
#             G=[item for item in node_energy]
#         threshold=p/(1-p*(round%int(1/p)))

#         for node in G:
#             for nod in node_energy:
#                 if node[0] == nod[0]:
#                     G[G.index(node)] = nod

#         print(f"Round:{round}, Threshold: {threshold}")
#         # Step 1: Cluster Head Selection
#         cluster_heads = []
#         while len(cluster_heads) == 0:  # Ensure at least one cluster head is selected
#             for node in G:
#                 if random.uniform(0, 1) < threshold:
#                     cluster_heads.append(node)
#                     G.remove(node)
#             print(f"Nodes Variable: {node_energy}")
#             print(f"Remaining Nodes:{G} \nLength of G is: {len(G)}.")

#         # Step 2: Cluster Formation
#         clusters = {i: [] for i in range(len(cluster_heads))}
#         for node in node_energy:
#             if node not in cluster_heads:
#                 # Calculate distances from the current node to all cluster heads
#                 distances = [euclidean_distance(node, ch) for ch in cluster_heads]
#                 if distances:  # Ensure distances list is not empty
#                     # Find the index of the nearest cluster head
#                     nearest_ch_index = distances.index(min(distances))
#                     # Assign the current node to the nearest cluster head's cluster
#                     clusters[nearest_ch_index].append(node)
                    
#         print(f"Value in Cluster Variable : {clusters}")
        
#         plt.figure(figsize=(10,10))
#         plt.xlim(0, FIELD_SIZE)
#         plt.ylim(0, FIELD_SIZE)
#         plt.title(f"LEACH Clustering - Round {round}")
#         plt.xlabel("X-coordinate")
#         plt.ylabel("Y-coordinate")
        
        
#         # Step 3: Data Transmission (Simplified)
#         for ch_index, members in clusters.items():
#             cluster_head = cluster_heads[ch_index]
#             # Assign Cluster heads coordinate to ch 
            
#             print(f"Cluster Head {ch_index+1}: {cluster_head}")
#             print(f"Number of Members in this cluster: {len(members)}")
#             for member,energy in members:
#                 # plt.plot([cluster_head[0], member[0]], [cluster_head[1], member[1]], 'k--')
#                 energy -= TRANSMISSION_ENERGY
#                 node_energy[nodes.index(member)]=(member,energy)
#                 print(f"  Node: {member}, Energy Left: {energy} -> Cluster Head: {cluster_head}")
#             # Simulate data aggregation and transmission to base station
#             print(f"Cluster Head {cluster_head} transmits aggregated data to the base station.")
#             ch_energy = cluster_head[1] - TRANSMISSION_ENERGY
#             node_energy[nodes.index(cluster_head[0])]=(cluster_head[0],ch_energy)
#             #cluster_heads[ch_index] ---- Cluster Head coordinates and energy
#             print(f"After Transmission  Cluster Head {cluster_head} , Energy Left: {cluster_head[1]}")
#         print(f"Cluster Heads in Round {round} are : {len(cluster_heads)}")
#         print("")


# # Run LEACH
# leach(G, P, MAX_ROUNDS, node_energy)

# # plt.figure(figsize=(10,10))
# # plt.xlim(0, FIELD_SIZE)
# # plt.ylim(0, FIELD_SIZE)
# # plt.title(f"LEACH Clustering ")
# # plt.xlabel("X-coordinate")
# # plt.ylabel("Y-coordinate")
# # plt.plot([2,10],[3,5])
# # plt.grid(True)
# # plt.show()


obj = round(5.4343,2)
print(obj)