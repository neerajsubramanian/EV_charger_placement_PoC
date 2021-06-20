from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from utilities import *
from visualization import *
from dwave.system import LeapHybridSampler

#   Read in data from files (functions from utilities.py)
sites_index, zones, rev_index = read_build_sites("build_sites.txt")
chargers_index = read_existing_chargers("existing.txt")

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


#   Objective - add a cost for each site
for site in sites_index.keys():
    Q[(site, site)] += cost



#   Constraint 1 = min ave distance to existing chargers in neighborhood
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

    


#   Constraint 2 = min ave distance to other new zones in neighborhood
for site1, val in sites_index.items():
    #   site = (zone, sector)
    #   val = (index, lat, long)

    for val2_index in graph_ss.neighbors(val[0]):
        #   quadratic penalty based on distance to neighbors
        Q[(site1, rev_index[val2_index])] += dist_mat_ss[val[0], val2_index]


#   Constraint 3 => number of chargers per zone = 1

chargers_per_zone = 1
gamme_3 = 150
# for zone in zones.keys():
#     for i in range(zones[zone]):
#         Q[(zone, i), (zone, j)] += (-2 * )


        ##  MORE WORK TO DO - INCOMPLETE -> n_final version