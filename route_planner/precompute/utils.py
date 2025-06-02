import heapq
import pickle
from collections import defaultdict

def dijkstra_from_node(graph, edge_weights, start_node):

    distances = {start_node: 0}
    paths = {start_node: [start_node]}
    pq = [(0, start_node)]

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)

        if curr_dist > distances.get(curr_node, float('inf')):
            continue

        for neighbor, weight in graph.get(curr_node, []):
            edge_key = (curr_node, neighbor)
            actual_weight = edge_weights.get(edge_key, weight)

            new_dist = curr_dist + actual_weight

            if new_dist < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_dist
                paths[neighbor] = paths[curr_node] + [neighbor]
                heapq.heappush(pq, (new_dist, neighbor))

    return distances, paths

def save_preprocessed(precomputer, filename):
    data = {
        'hub_distances': precomputer.hub_distances,
        'station_to_hubs': precomputer.station_to_hubs,
        'hubs_to_station': dict(precomputer.hubs_to_station)
    }
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def load_preprocessed(precomputer, filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    precomputer.hub_distances = data['hub_distances']
    precomputer.station_to_hubs = data['station_to_hubs']
    precomputer.hubs_to_station = defaultdict(list, data['hubs_to_station'])
