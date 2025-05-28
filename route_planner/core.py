from typing import Dict, List, Tuple
from .graph import GraphBuilder
from .pathfinder import PathFinder
from .formatting import format_route_segments
from route_planner.precompute.utils import save_preprocessed, load_preprocessed

class RoutePlanner:
    def __init__(self, lines: Dict[int, List[str]], station_lines: Dict[str, List[int]]):
        self.lines = lines
        self.station_lines = station_lines
        self.graph, self.edge_weights, self.transfer_stations = GraphBuilder(lines, station_lines).build()
        self.pathfinder = PathFinder(self.graph, self.edge_weights, self.transfer_stations)

    def find_route(self, origin: str, destination: str) -> Tuple[float, List[Tuple[str, int, str]]]:
        return self.pathfinder.find_best_route(
            origin=origin,
            destination=destination,
            station_lines=self.station_lines,
            transfer_stations=self.transfer_stations,
            hub_data=self.pathfinder.hub_nodes,
            graph=self.graph,
            edge_weights=self.edge_weights
        )
    def format_route(self, path: List[Tuple[str, int, str]]) -> List[Tuple[str, str]]:
        return format_route_segments(path)

    def save_preprocessed_data(self, filename: str):
        save_preprocessed(self.pathfinder, filename)

    def load_preprocessed_data(self, filename: str):
        load_preprocessed(self.pathfinder, filename)