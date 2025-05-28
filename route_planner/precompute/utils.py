import pickle
from collections import defaultdict

def dijkstra_from_node(graph, edge_weights, start):
    distances = {start: 0}
    paths = {start: [start]}
    pq = [(0, start)]
    visited = set()

    while pq:
        pq.sort(key=lambda x: x[0])
        current_dist, current = pq.pop(0)
        if current in visited:
            continue
        visited.add(current)

        for neighbor in graph[current]:
            weight = edge_weights.get((current, neighbor), float('inf'))
            new_dist = current_dist + weight
            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                paths[neighbor] = paths[current] + [neighbor]
                pq.append((new_dist, neighbor))

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
