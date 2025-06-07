from collections import defaultdict
from typing import List, Tuple, Dict, Set, Optional
from .utils import get_station_nodes
from route_planner.precompute import HubPrecomputer
import heapq

class PathFinder:
    def __init__(self, planner):
        self.planner = planner

        self.precomputer = HubPrecomputer(graph=self.planner.graph, hub_stations=self.planner.hub_stations)
        self.precomputer.precompute_hub_data()

        self.planner.hub_distances = self.precomputer.hub_distances  # 허브 거리 
        self.planner.station_to_hubs = self.precomputer.station_to_hubs
        self.planner.hubs_to_station = self.precomputer.hubs_to_station
        self._precompute_hub_heuristics()

    def _precompute_hub_heuristics(self):
        """Precompute minimum distance to nearest hub for each node"""
        self.min_dist_to_hub = {}
        
        for node in self.planner.graph:
            if node[0] in self.planner.hub_stations:
                self.min_dist_to_hub[node] = 0
            elif node in self.planner.station_to_hubs:
                # Find minimum distance to any hub
                min_dist = float('inf')
                for hub_node, dist, _ in self.planner.station_to_hubs[node]:
                    min_dist = min(min_dist, dist)
                self.min_dist_to_hub[node] = min_dist
            else:
                self.min_dist_to_hub[node] = float('inf')

    def _heuristic(self, current: Tuple[str, str], goal: Tuple[str, str]) -> float:
        current_to_hub = self.min_dist_to_hub.get(current, 0) # current_to_hub = self.min_dist_to_hub.get(current,0)
        goal_to_hub = self.min_dist_to_hub.get(goal, 0) # goal_to_hub =  
        
        return current_to_hub + goal_to_hub
    
    def _reconstruct_path(self, came_from: Dict, current: Tuple[str, str]) -> List[Tuple[str, str]]:
        """Reconstruct path from came_from dictionary"""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def _astar_search(self, start: Tuple[str, str], goal: Tuple[str, str]) -> Tuple[float, List[Tuple[str, str]]]:
        """A* search algorithm"""
        # Priority queue: (f_score, g_score, node)
        open_set = [(0, 0, start)]
        came_from = {}
        
        g_score = {start: 0}
        f_score = {start: self._heuristic(start, goal)}
        
        visited = set()
        
        while open_set:
            _, current_g, current = heapq.heappop(open_set)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == goal:
                path = self._reconstruct_path(came_from, current)
                return g_score[goal], path
            
            # Explore neighbors
            for neighbor, weight in self.planner.graph.get(current, []):
                # Use edge weights that include transfer penalties
                edge_key = (current, neighbor)
                actual_weight = self.planner.edge_weights.get(edge_key, weight)
                
                tentative_g = g_score[current] + actual_weight
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self._heuristic(neighbor, goal)
                    f_score[neighbor] = f
                    heapq.heappush(open_set, (f, tentative_g, neighbor))
        
        return float('inf'), []
    
    def _hub_based_search(self, origin_node: Tuple[str, str], destination_node: Tuple[str, str]) -> Tuple[float, List[Tuple[str, str]]]:
        """Original hub-based search as fallback"""
        o_station, o_line = origin_node
        d_station, d_line = destination_node
        
        best_distance = float('inf')
        best_path = []
        
        # Case 1: hub -> hub
        if o_station in self.planner.hub_stations and d_station in self.planner.hub_stations:
            if origin_node in self.planner.hub_distances and destination_node in self.planner.hub_distances[origin_node]:
                dist, path = self.planner.hub_distances[origin_node][destination_node]
                if dist < best_distance:
                    best_distance = dist
                    best_path = path
        
        # Case 2: hub -> regular
        elif o_station in self.planner.hub_stations and d_station not in self.planner.hub_stations:
            if destination_node in self.planner.hubs_to_station:
                for hub_node, dist, path in self.planner.hubs_to_station[destination_node]:
                    if hub_node == origin_node and dist < best_distance:
                        best_distance = dist
                        best_path = path
        
        # Case 3: regular -> hub
        elif o_station not in self.planner.hub_stations and d_station in self.planner.hub_stations:
            if origin_node in self.planner.station_to_hubs:
                for hub_node, dist, path in self.planner.station_to_hubs[origin_node]:
                    if hub_node == destination_node and dist < best_distance:
                        best_distance = dist
                        best_path = path
        
        # Case 4: regular -> regular (optimized with early termination)
        else:
            if origin_node in self.planner.station_to_hubs and destination_node in self.planner.hubs_to_station:
                # Create lookup for faster access
                dest_hubs = {hub: (dist, path) for hub, dist, path in self.planner.hubs_to_station[destination_node]}
                
                for hub1, dist1, path1 in self.planner.station_to_hubs[origin_node]:
                    # Early termination if current path is already worse
                    if dist1 >= best_distance:
                        continue
                    
                    # Direct hub connection
                    if hub1 in dest_hubs:
                        dist2, path2 = dest_hubs[hub1]
                        total_dist = dist1 + dist2
                        if total_dist < best_distance:
                            best_distance = total_dist
                            best_path = path1[:-1] + path2
                    
                    # Hub-to-hub connection
                    elif hub1 in self.planner.hub_distances:
                        for hub2 in dest_hubs:
                            if hub2 in self.planner.hub_distances[hub1]:
                                hub_dist, hub_path = self.planner.hub_distances[hub1][hub2]
                                dist2, path2 = dest_hubs[hub2]
                                total_dist = dist1 + hub_dist + dist2
                                
                                if total_dist < best_distance:
                                    best_distance = total_dist
                                    best_path = path1[:-1] + hub_path[:-1] + path2
        
        return best_distance, best_path
    def find_best_route(self, origin: str, destination: str) -> Tuple[float, List[Tuple[str, str]]]:

        
        origin_nodes = get_station_nodes(origin, self.planner.station_lines, self.planner.graph)
        destination_nodes = get_station_nodes(destination, self.planner.station_lines, self.planner.graph)
        
        if not origin_nodes or not destination_nodes:
            raise ValueError(f"존재하지 않는 역입니다 - 출발: {origin}, 도착: {destination}")
        
        best_distance = float('inf')
        best_path = []
        
        for origin_node in origin_nodes:
            for destination_node in destination_nodes:
                # Try A* search first
                astar_dist, astar_path = self._astar_search(origin_node, destination_node)
                
                # Also try hub-based search
                hub_dist, hub_path = self._hub_based_search(origin_node, destination_node)
                
                # Choose the better result
                if astar_dist < hub_dist and astar_dist < best_distance:
                    best_distance = astar_dist
                    best_path = astar_path
                elif hub_dist < best_distance:
                    best_distance = hub_dist
                    best_path = hub_path
        
        if not best_path:
            raise ValueError(f"경로를 찾을 수 없습니다 - ({origin} → {destination})")
        
        # # 역 이름과 노선 확인
        # print("신당:", self.planner.station_lines.get("신당"))
        # print("신도림:", self.planner.station_lines.get("신도림"))

# # 그래프에 있는지 확인
#         print("신당 노드:", [n for n in self.planner.graph if n[0] == "신당"])
#         print("신도림 노드:", [n for n in self.planner.graph if n[0] == "신도림"])
        
        return best_distance, best_path
