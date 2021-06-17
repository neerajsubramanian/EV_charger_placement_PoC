from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from dwave.system import LeapHybridSampler
from utilities import *
import map_viz

# Read in data from files
sites_index, zones, rev_index = read_in_sites("build_sites.txt")
chargers_index = read_in_existing("existing.txt")

# Compute distances from lat/long
dist_mat_sc = dist_mat_sites_to_chargers(sites_index, chargers_index)
dist_mat_ss = dist_mat_sites_to_sites(sites_index)

# Build neighbor graphs
min_dist = 10
graph_sc = build_distance_graph(min_dist*2, dist_mat_sc)
graph_ss = build_distance_graph(min_dist*2, dist_mat_ss)

cost = 20

# Initialize our QUBO dictionary
Q = defaultdict(int)

# 5 zones * 4 sectors = 20 variables
num_zones = len(zones)
# num_sec = 4

# Objective - add a cost for each site
for site in sites_index.keys():
    Q[(site, site)] += cost

# Constraint1 - min ave distance to existing chargers in neighborhood
for site, val in sites_index.items():
    # site = (zone, sector)
    # val = (index, lat, long)

    # sum of weighted edges
    sum_of_edges = graph_sc.degree(val[0], weight='weight')
    
    # number of edges
    num_edges = graph_sc.degree(val[0])
    
    # average = sum / number
    if num_edges > 0:
        ave_dist = sum_of_edges / num_edges
    else: # node has no neighbors that are existing chargers; set a large value
        ave_dist = 100
    Q[(site, site)] += ave_dist

# Constraint2 - min ave distance to other zones in neighborhood
for site1, val in sites_index.items():
    # site = (zone, sector)
    # val = (index, lat, long)

    for val2_index in graph_ss.neighbors(val[0]):
        # quadratic penalty based on distance to neighbors
        Q[(site1, rev_index[val2_index])] += dist_mat_ss[val[0], val2_index]

# Constraint3 - one charger per zone
chargers_per_zone = 1
gamma_3 = 150
for zone in zones.keys():
    for i in range(zones[zone]):
        Q[(zone, i), (zone, i)] += (-2 * chargers_per_zone + 1) * gamma_3
        for j in range(i + 1, zones[zone]):
            Q[(zone, i), (zone, j)] += 2 * gamma_3

# Solve
sampler = LeapHybridSampler()
sampleset = sampler.sample_qubo(Q)
sample = sampleset.first.sample
for key, val in sample.items():
    print(key, val)

write_output_to_file(sample, sites_index)
map_viz.viz_results(red="soln.txt", yellow="existing.txt", blue="non_soln.txt", radius=5, output_filename="soln_map.png")
