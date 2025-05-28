import time
from .utils import dijkstra_from_node

class HubPrecomputer:
    def __init__(self, graph, edge_weights, hub_nodes, hub_distances, station_to_hubs, hubs_to_station):
        self.graph = graph
        self.edge_weights = edge_weights
        self.hub_nodes = hub_nodes
        self.hub_distances = hub_distances
        self.station_to_hubs = station_to_hubs
        self.hubs_to_station = hubs_to_station

    def precompute_hub_data(self):
        print(f"허브역 {len(self.hub_nodes)}개 처리 중...")
        start_time = time.time()

        for hub in self.hub_nodes:
            distances, paths = dijkstra_from_node(self.graph, self.edge_weights, hub)
            self.hub_distances[hub] = {
                target: (distances[target], paths[target])
                for target in self.hub_nodes if target in distances
            }

        all_nodes = set(self.graph.keys())
        non_hub_nodes = all_nodes - self.hub_nodes

        for node in non_hub_nodes:
            distances, paths = dijkstra_from_node(self.graph, self.edge_weights, node)
            reachable_hubs = [
                (hub, distances[hub], paths[hub])
                for hub in self.hub_nodes if hub in distances
            ]
            reachable_hubs.sort(key=lambda x: x[1])
            self.station_to_hubs[node] = reachable_hubs[:5]

        for hub in self.hub_nodes:
            distances, paths = dijkstra_from_node(self.graph, self.edge_weights, hub)
            for node in non_hub_nodes:
                if node in distances:
                    self.hubs_to_station[node].append((hub, distances[node], paths[node]))

        for node in non_hub_nodes:
            if node in self.hubs_to_station:
                self.hubs_to_station[node].sort(key=lambda x: x[1])

        print(f"허브역 처리 완료. 소요 시간: {time.time() - start_time:.2f}초")