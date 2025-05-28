from collections import defaultdict
from typing import List, Tuple, Dict, Set
from .utils import  identify_hub_nodes, get_station_nodes
from route_planner.precompute import HubPrecomputer
from .route_strategies import (
    direct_route,
    hub_to_hub,
    hub_to_regular,
    regular_to_hub,
    regular_to_regular
)

class PathFinder:
    def __init__(self, graph, edge_weights, transfer_stations):
        self.graph = graph
        self.edge_weights = edge_weights
        self.transfer_stations = transfer_stations

        self.hub_nodes: Set[Tuple[str, int, str]] = identify_hub_nodes(transfer_stations)
        self.hub_distances = {}
        self.station_to_hubs = {}
        self.hubs_to_station = defaultdict(list)
        self.precomputer = HubPrecomputer(self.graph, self.edge_weights, self.hub_nodes, self.hub_distances, self.station_to_hubs, self.hubs_to_station)

        self.precomputer.precompute_hub_data()

    def find_best_route(
        self,
        origin: str,
        destination: str,
        station_lines: Dict[str, List[int]],
        transfer_stations: Dict[str, List[int]],
        hub_data: Set,
        graph: Dict,
        edge_weights: Dict
    ) -> Tuple[float, List[Tuple[str, int, str]]]:
        start_nodes = get_station_nodes(origin, station_lines, self.graph)
        end_nodes = get_station_nodes(destination, station_lines, self.graph)

        if not start_nodes or not end_nodes:
            raise ValueError(f"경로를 찾을 수 없습니다({origin} → {destination})")

        best_time = float('inf')
        best_path = []

        strategies = [
            direct_route,
            hub_to_hub,
            hub_to_regular,
            regular_to_hub,
            regular_to_regular
        ]

        for strategy in strategies:
            time, path = strategy(
                start_nodes,
                end_nodes,
                self.hub_nodes,
                self.hub_distances,
                self.station_to_hubs,
                self.hubs_to_station,
                self.graph,
                self.edge_weights
            )
            if time < best_time:
                best_time = time
                best_path = path

        if not best_path:
            raise ValueError(f"경로를 찾을 수 없습니다({origin} → {destination})")

        return best_time, best_path