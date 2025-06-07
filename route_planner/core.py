from typing import Dict, List, Tuple, Union
from route_planner.preprocessing import GraphBuilder
from route_planner.pathfinder import PathFinder
from route_planner.precompute.utils import save_preprocessed, load_preprocessed
from route_planner.utils import format_route_segments
import pprint

def debug_seoul_station(builder):
    seoul_station = "서울역"
    debug_info = {}

    # 1. Lines associated with 서울역
    seoul_lines = builder.station_lines_map.get(seoul_station, set())
    debug_info["lines"] = list(seoul_lines)

    # 2. Nodes for 서울역 that exist in the graph
    seoul_nodes = []
    for line in seoul_lines:
        node = (seoul_station, line)
        if node in builder.subway_graph:
            seoul_nodes.append(node)
    debug_info["nodes_in_graph"] = seoul_nodes

    # 3. Transfer edges between lines at 서울역
    transfer_edges = []
    for i in range(len(seoul_nodes)):
        for j in range(i + 1, len(seoul_nodes)):
            node1, node2 = seoul_nodes[i], seoul_nodes[j]
            neighbors = builder.subway_graph[node1]
            if any(n == node2 and abs(w - 2.0) < 1e-3 for n, w in neighbors):
                transfer_edges.append((node1, node2))
    debug_info["transfer_edges_between_lines"] = transfer_edges

    # 4. Missing nodes or missing transfer edges
    missing_nodes = [(seoul_station, line) for line in seoul_lines if (seoul_station, line) not in builder.subway_graph]
    debug_info["missing_nodes"] = missing_nodes

    return debug_info


class RoutePlanner:
    def __init__(self, csv_path: str, transfer_time: float = 2.0):
        builder = GraphBuilder(csv_path)
        builder.build()

        print(builder.station_lines_map.get("서울역"))

        self.graph = builder.get_graph()
        self.hub_stations = builder.get_transfer_stations()
        self.station_lines = builder.get_station_lines_map()
        self.hub_nodes = builder.get_hub_nodes()

        self.edge_weights = {}

        for u, neighbors in self.graph.items():
            for v, time in neighbors:
                penalty = 0
                if u[0] in self.hub_stations and v[0] in self.hub_stations:
                    u_lines = self.station_lines[u[0]]
                    v_lines = self.station_lines[v[0]]
                    if not (u_lines & v_lines):
                        penalty = transfer_time
                self.edge_weights[(u, v)] = time + penalty

        self.pathfinder = PathFinder(planner=self)


    def find_route(self, origin: str, destination: str) -> Tuple[float, List[Tuple[str, str]]]:
        return self.pathfinder.find_best_route(origin=origin, destination=destination)

    @staticmethod
    def format_route(path: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        return format_route_segments(path)

    def save_preprocessed_data(self, filename: str):
        save_preprocessed(self.pathfinder, filename)

    def load_preprocessed_data(self, filename: str):
        load_preprocessed(self.pathfinder, filename)