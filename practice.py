from collections import defaultdict

import networkx as nx
import numpy as np
from dwave.system import LeapHybridSampler

Q = defaultdict(int)
cost = 20

# 5 blue circles, each one has 4 locations in it = 20 binary variables
num_locations = 5
num_sectors = 4

# Objective: sum (cost * variable)
for i in range(num_locations):
    for j in range(num_sectors):
        Q[((i, j), (i, j))] += cost

# Build up network
min_acceptable_distance = 10
existing_locations = 10
dist = np.random.rand(num_locations, existing_locations + num_locations) * 30

# rows = blue circles
# cols = blue circles, followed by existing chargers
for i in range(num_locations):
    dist[i, i] = 0

G = nx.Graph()
for i in range(num_locations):
    for j in range(existing_locations + num_locations):
        # if it's close to another location, draw an edge
        if (dist[i, j] < min_acceptable_distance) and (i != j):
            # draw an edge
            G.add_edge(i, j)

# Constraint 1: distances - existing nodes

# Constraint 2: distances - neighboring blue circles

# Constraint 3: number of chargers in each blue circle
chargers_per_circle = 1
gamma_3 = 30
for k in range(num_locations):
    for i in range(num_sectors):
        Q[(k, i), (k, i)] += (-2 * chargers_per_circle + 1) * gamma_3
        for j in range(i + 1, num_sectors):
            Q[(k, i), (k, j)] += 2 * gamma_3

# Constraint 4: traffic constraint

sampler = LeapHybridSampler()

sampleset = sampler.sample_qubo(Q)

sample = sampleset.first.sample

for key, val in sample.items():
    print(key, val)
