#   reads data from files that the main program can use for solver
#   this file's functions are called//outputs are used in the main program -> obj_constr.py in the n_final_1_ branch

from collections import defaultdict
import math
import numpy as np
import networkx as nx


#   Calculate distance between points
def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


#   Read data from build_sites.txt file for the zones selected (displayed in n_visualization)
def read_build_sites(build_sites_filename):
    with open(build_sites_filename) as f:
        lines = f.readlines()
    counter = 0
    sites_index = {}
    rev_index = {}
    #   List that indicates how many sectors are in each zone. zones[zone_number] = # sectors    
    zones = defaultdict(int)
    for line in lines:
        temp = line.split()
        zone_index = int(temp[0][1:])-1
        zones[zone_index] +=1
        sec_index = int(temp[1][1:])-1
        latf = float(temp[-2])
        longf = float(temp[-1])
        sites_index[(zone_index, sec_index)] = (counter, latf, longf)
        rev_index[counter] = (zone_index, sec_index)
        counter += 1
    # print(sites_index)
    # print(zones)
    # print(rev_index)
    # print(counter)
    return sites_index, zones, rev_index


#   Read data from existing.txt file for existing chargers
def read_existing_chargers(existing_filename):
    with open(existing_filename) as f:
        lines = f.readlines()
    chargers_index = {}
    for line in lines:
        # print(line)
        temp = line.split()
        name = int(temp[0][1:])-1
        latf = float(temp[-2])
        longf = float(temp[-1])
        chargers_index[name] = (latf, longf)
    # print(chargers_index)
    return chargers_index

#   Distance from sites to sites
def dist_matrix_sites_to_sites(sites_index):
    dist_matrix = np.zeros((len(sites_index), len(sites_index)))
    for key_n, value_n in sites_index.items():
        for key_e, value_e in sites_index.items():
            #   only compute distance if different sites
            if key_n[0] != key_e[0]:
                dist_matrix[value_n[0], value_e[0]] = haversine(value_n[1:], value_e[1:])/1000.0
    return dist_matrix


#   Distance from sites to chargers (using chargers_index)
def dist_matrix_sites_to_chargers(sites_index, chargers):
    dist_matrix = np.zeros((len(sites_index), len(chargers)))
    for key_n, value_n in sites_index.items():
        for key_e, value_e in chargers.items():
            dist_matrix[value_n[0], key_e] = haversine((value_n[1:]), value_e)/1000.0
    return dist_matrix


#   Distance graph -> minimum acceptable distance, dist_matrices:
def dist_graph(max_dist, dist_matrix):
    G = nx.Graph()
    num_start_points, num_end_points = dist_matrix.shape
    for i in range(num_start_points):
        G.add_node(i)
        for j in range(num_end_points):
            G.add_node(j)
            #   check for valid dist_matrix value & satisfy the min_acceptable_distance constraint
            if (dist_matrix[i,j] > 0) and (dist_matrix[i,j] < max_dist):
                G.add_weighted_edges_from([(i, j, dist_matrix[i,j])])
    return G


#   Write the output to file -> build the map.png file when called
def write_output_file(sample, sites_index):
    #   with block with w flag for write then close
    with open('soln.txt', 'w') as f:
        with open('non_soln.txt', 'w') as g:
            for key, val in sample.items():
                if val == 1:
                    f.write("{} {} {} {}\n".format(key[0], key[1], sites_index[key][-2], sites_index[key][-1]))
                else:
                    g.write("{} {} {} {}\n".format(key[0], key[1], sites_index[key][-2], sites_index[key][-1]))
            
    return

