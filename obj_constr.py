from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from dwave.system import LeapHybridSampler

Q = defaultdict(int)
cost = 20

# 5 zones * 4 sectors = 20 variables
num_zones = 5
num_sec = 4

# Objective
# sum(zones) and sum (sectors)
for i in range(num_zones):
    for j in range(num_sec):
        Q[((i, j), (i, j))] += cost

# Buid up the network
# max acceptable distance?
min_acceptable_distance = 10
existing_locations = 10
# times 30 so that they're in between 0 and 30 in terms of distance
#need to divide the zones into sectors
dist = np.random.rand(num_zones, existing_locations + num_zones) * 30
# rows = zones; colms = zones follwed by existing chargers
# distance from one node to itself should be set to 0
for i in range(num_zones):
    dist[i, i] = 0
G = nx.Graph()
for i in range(num_zones):
    for j in range(num_sec):
        for k in range(existing_locations):
            if (dist[sites_index[(i,j)], k] < min_acceptable_distance):
                # G.add_edge(i, j)
                #over all of the edges add up all the weights
                #trying to identify charger by zone, sec loc
                G.add_weighted_edges_from([(sites_index[(i,j)],k,dist[sites_index[(i,j)],k])])
            
nx.draw(G)
plt.show()


# Constraint1
#distance from new chargers to existing chargers in the network
for i in range(num_zones): #what is the avg distance to the existing chargers
    for j in range(num_sec):
        for k in range(existing_locations+num_zones):
            #for build site i,j -> get all of the neighbors in G and add up the edge weights
            weighted_sum = G.degree(sites_index[(i,j)], weight='weight')
            #degree is number of edges that are touching a specific node.
            num_neighbors = G.degree(sites_index[(i,j)])
            #average
            avg_dist = weighted_sum/num_neighbors
            #add a linear bias
            Q[((i,j), (i,j))] += avg_dist
 
# Constraint2
#distance from new chargers to other new chargers to be added to the network
# for i in range(num_zones):
#     for j in range(num_sec):
# 1-  build a new graph -> edges should be from each biuld site to nearby build sites in other zones
# 2- weighted sum -> num_neighbors -> avg_dist  --> this is going to be a quad term - not a linear term -> 

# Constraint3
chargers_per_circle = 1
gamma_3 = 30
for k in range(num_zones):
    for i in range(num_sec):
        Q[(k, i), (k, i)] += (-2 * chargers_per_circle + 1) * gamma_3
        for j in range(i + 1, num_sec):
            Q[(k, i), (k, j)] += 2 * gamma_3

# Solve
sampler = LeapHybridSampler()
sampleset = sampler.sample_qubo(Q)
sample = sampleset.first.sample
for key, val in sample.items():
    print(key, val)
