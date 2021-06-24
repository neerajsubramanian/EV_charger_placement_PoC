from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from utilities import *
from visualization import *
from dwave.system import LeapHybridSampler

#   Read in data from files (functions from utilities.py)
sites_index, zones, rev_index, site_traffic_index = read_build_sites("build_sites_add.txt")
chargers_index, traffic_index = read_existing_chargers("existing_add.txt")

#   Compute the distances from points in files
dist_mat_ss = dist_matrix_sites_to_sites(sites_index)
dist_mat_sc = dist_matrix_sites_to_chargers(sites_index, chargers_index)

#   Build neighbor graphs
max_dist = 10
graph_ss = dist_graph(max_dist*2, dist_mat_ss)
graph_sc = dist_graph(max_dist*2, dist_mat_sc)

#   Initialize QUBO dictionary & variables for Obj/Constr
Q = defaultdict(int)
cost = 20
num_zones = len(zones) # len returns number of objects
num_sec = 4


#   Objective => add a cost for each site
for site in sites_index.keys():
    Q[(site, site)] += cost


#   Objective 2 => minimize travel time between all points


#   Constraint 1 => min ave distance to existing chargers in neighborhood
for site, val in sites_index.items():
    #   site = (zone, sector)
    #   val = (index, lat, long)

    #   sum of weighted edges
    sum_of_edges  = graph_sc.degree(val[0], weight='weight')
    #   number of edges
    num_edges = graph_sc.degree(val[0])
    #   average = sum / number
    if num_edges > 0:
        ave_dist = sum_of_edges / num_edges
    else:   #   node has no neighbors that are existing chargers, set a large value
        ave_dist = 100
    Q[(site, site)] += ave_dist

    


#   Constraint 2 => min ave distance to other new zones in neighborhood
for site1, val in sites_index.items():
    #   site = (zone, sector)
    #   val = (index, lat, long)

    for val2_index in graph_ss.neighbors(val[0]):
        #   quadratic penalty based on distance to neighbors
        Q[(site1, rev_index[val2_index])] += dist_mat_ss[val[0], val2_index]


#   Constraint 3 => number of chargers per zone = 1
#   linear coeff =  -2*c+1 ; quadratic coeff = 2*
chargers_per_zone = 1
gamma_3 = 1250
for zone in zones.keys():
    for i in range(zones[zone]):
        Q[(zone, i), (zone, i)] += (-2 * chargers_per_zone + 1) * gamma_3
        for j in range(i + 1, zones[zone]):
            Q[(zone, i), (zone, j)] += 2 * gamma_3


#   Constraint 4 => Prefer high traffic *build site* locations
# high_traffic_determinant_value = 750
# for site in sites_index.keys():
#     Q[(site, site)] += site_traffic_index
for zone in zones.keys():
    for i in range(zones[zone]):
        Q[(zone, i), (zone, i)] += -1 * site_traffic_index[(zone, i)]



#   Solve
sampler = LeapHybridSampler()
sampleset = sampler.sample_qubo(Q)
sample = sampleset.first.sample
for key, val in sample.items():
    print(key, val)

write_output_file(sample, sites_index)
viz_results(red='soln.txt', yellow="existing.txt", blue="non_soln.txt", radius=5, output_filename="soln_map.png")