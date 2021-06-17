from collections import defaultdict
import math
import numpy as np
import networkx as nx

def read_in_sites(build_sites_filename):

    # Read in each line in the file into a list of lines
    with open(build_sites_filename) as f:
        lines = f.readlines()

    counter = 0
    sites_index = {}
    rev_index = {}
    zones = defaultdict(int) # List that indicates how many sectors are in each zone. zones[zone_number] = # sectors
    for line in lines:
        temp = line.split()

        zone_index = int(temp[0][1:])-1
        zones[zone_index] += 1
        
        sec_index = int(temp[1][1:])-1
        lat = float(temp[-2])
        long = float(temp[-1])
        sites_index[(zone_index, sec_index)] = (counter, lat, long)
        rev_index[counter] = (zone_index, sec_index)

        counter += 1

    return sites_index, zones, rev_index

def read_in_existing(existing_chargers_filename):

    # Read in each line in the file into a list of lines
    with open(existing_chargers_filename) as f:
        lines = f.readlines()

    chargers_index = {}
    for line in lines:
        temp = line.split()

        name = int(temp[0][1:])-1
        lat = float(temp[-2])
        long = float(temp[-1])

        chargers_index[name] = (lat, long)

    return chargers_index

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

def dist_mat_sites_to_chargers(sites_index, chargers):

    dist_mat = np.zeros((len(sites_index), len(chargers)))

    for key_n, val_n in sites_index.items():
        for key_e, val_e in chargers.items():
            dist_mat[val_n[0], key_e] = haversine((val_n[1:]), val_e)/1000.0

    return dist_mat

def dist_mat_sites_to_sites(sites_index):

    dist_mat = np.zeros((len(sites_index), len(sites_index)))

    for key_n, val_n in sites_index.items():
        for key_e, val_e in sites_index.items():

            # only compute distance if they are in different zones
            if key_n[0] != key_e[0]:
                dist_mat[val_n[0], val_e[0]] = haversine((val_n[1:]), val_e[1:])/1000.0

    return dist_mat

def build_distance_graph(min_dist, dist_mat):

    G = nx.Graph()

    num_start_points, num_end_points = dist_mat.shape

    for i in range(num_start_points):
        G.add_node(i)
        for j in range(num_end_points):
            G.add_node(j)
            if (dist_mat[i,j] > 0) and (dist_mat[i,j] < min_dist):
                G.add_weighted_edges_from([(i, j, dist_mat[i,j])])

    return G

def write_output_to_file(sample, sites_index):

    with open('soln.txt', 'w') as f:
        with open('non_soln.txt', 'w') as g:
        
            for key, val in sample.items():
                
                if val == 1:
                    f.write("{} {} {} {}\n".format(key[0], key[1], sites_index[key][-2], sites_index[key][-1]))
                else:
                    g.write("{} {} {} {}\n".format(key[0], key[1], sites_index[key][-2], sites_index[key][-1]))
            
    return

