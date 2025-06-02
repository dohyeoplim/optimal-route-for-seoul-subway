from collections import defaultdict
from typing import List, Tuple, Dict, Set, Optional
from .utils import get_station_nodes
from route_planner.precompute import HubPrecomputer

class PathFinder:
    def __init__(self, planner):
        self.planner = planner

        self.precomputer = HubPrecomputer(graph=self.planner.graph, hub_stations=self.planner.hub_stations)

        self.precomputer.precompute_hub_data()

        self.planner.hub_distances = self.precomputer.hub_distances
        self.planner.station_to_hubs = self.precomputer.station_to_hubs
        self.planner.hubs_to_station = self.precomputer.hubs_to_station

    def find_best_route(self, origin: str, destination: str) -> Tuple[float, List[Tuple[str, str]]]:
        origin_nodes = get_station_nodes(origin, self.planner.station_lines, self.planner.graph)
        destination_nodes = get_station_nodes(destination, self.planner.station_lines, self.planner.graph)

        if not origin_nodes or not destination_nodes:
            raise ValueError(f"존재하지 않는 역입니다 - 출발: {origin}, 도착: {destination}")

        best_distance = float('inf')
        best_path: List[Tuple[str, str]] = []

        for origin_node in origin_nodes:
            for destination_node in destination_nodes:
                o_station, o_line = origin_node
                d_station, d_line = destination_node

                # 케이스 1: hub -> hub
                if o_station in self.planner.hub_stations and d_station in self.planner.hub_stations:
                    if origin_node in self.planner.hub_distances and destination_node in self.planner.hub_distances[origin_node]:
                        dist, path = self.planner.hub_distances[origin_node][destination_node]
                        if dist < best_distance:
                            best_distance = dist
                            best_path = path

                # 케이스 2: hub -> regular
                elif o_station in self.planner.hub_stations and d_station not in self.planner.hub_stations:
                    if destination_node in self.planner.hubs_to_station:
                        for hub_node, dist, path in self.planner.hubs_to_station[destination_node]:
                            if hub_node == origin_node and dist < best_distance:
                                best_distance = dist
                                best_path = path

                # 케이스 3: regular -> hub
                elif o_station not in self.planner.hub_stations and d_station in self.planner.hub_stations:
                    if origin_node in self.planner.station_to_hubs:
                        for hub_node, dist, path in self.planner.station_to_hubs[origin_node]:
                            if hub_node == destination_node and dist < best_distance:
                                best_distance = dist
                                best_path = path

                # 케이스 4: regular -> regular
                else:
                    if origin_node in self.planner.station_to_hubs and destination_node in self.planner.hubs_to_station:
                        for hub1, dist1, path1 in self.planner.station_to_hubs[origin_node]:
                            for hub2, dist2, path2 in self.planner.hubs_to_station[destination_node]:
                                if hub1 == hub2:
                                    total_dist = dist1 + dist2
                                    combined_path = path1[:-1] + path2
                                elif hub1 in self.planner.hub_distances and hub2 in self.planner.hub_distances[hub1]:
                                    hub_dist, hub_path = self.planner.hub_distances[hub1][hub2]
                                    total_dist = dist1 + hub_dist + dist2
                                    combined_path = path1[:-1] + hub_path[:-1] + path2
                                else:
                                    continue

                                if total_dist < best_distance:
                                    best_distance = total_dist
                                    best_path = combined_path

        if not best_path:
            raise ValueError(f"경로를 찾을 수 없습니다 - ({origin} → {destination})")

        return best_distance, best_path