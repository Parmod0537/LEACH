import random
NUM_NODES = 20
FIELD_SIZE = 100
P = 0.1  # Probability of becoming a cluster head
MAX_ROUNDS = 10
SINK_NODEX=[50]
SINK_NODEY=[99]
INITIAL_ENERGY=50
TRANSMISSION_ENERGY=0.5


nodes = [(round(random.uniform(0, FIELD_SIZE),2), round(random.uniform(0, FIELD_SIZE),2)) for _ in range(NUM_NODES)]

node_energy=[(node,INITIAL_ENERGY) for node in nodes]
print (node_energy[0][0])


