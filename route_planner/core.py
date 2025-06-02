from typing import Dict, List, Tuple, Union
from route_planner.preprocessing import GraphBuilder
from route_planner.pathfinder import PathFinder
from route_planner.precompute.utils import save_preprocessed, load_preprocessed
from route_planner.utils import format_route_segments
import pprint

class RoutePlanner:
    def __init__(self, csv_path: str, transfer_time: float = 2.0):
        builder = GraphBuilder(csv_path)
        builder.build()

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