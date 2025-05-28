from typing import List, Tuple, Dict
from collections import deque

def get_station_nodes(station: str, station_lines: Dict[str, List[int]],
                       graph: Dict) -> List[Tuple[str, int, str]]:
    nodes = []
    lines = station_lines.get(station, [])

    for line in lines:
        for direction in ('F', 'B'):
            node = (station, line, direction)
            if node in graph:
                nodes.append(node)

    return nodes

def identify_hub_nodes(transfer_stations):
    hub_nodes = set()
    for station, lines in transfer_stations.items():
        for line in lines:
            hub_nodes.add((station, line, 'F')) # 정방향 Forward
            hub_nodes.add((station, line, 'B')) # 역방향 Backward
    return hub_nodes

def find_direct_path(graph: Dict, edge_weights: Dict,
                     start: Tuple[str, int, str],
                     end: Tuple[str, int, str]) -> Tuple[float, List[Tuple[str, int, str]]]:
    if start[1] != end[1]:  # 다른 노선이면 불가
        return float('inf'), []

    if start == end:
        return 0, [start]

    # BFS
    queue = deque([(start, [start], 0)])
    visited = {start}

    while queue:
        current, path, dist = queue.popleft()

        for neighbor in graph.get(current, []):
            if neighbor[1] != start[1]:
                continue

            if neighbor == end:
                final_path = path + [neighbor]
                final_dist = dist + edge_weights.get((current, neighbor), 2)
                return final_dist, final_path

            if neighbor not in visited:
                visited.add(neighbor)
                new_dist = dist + edge_weights.get((current, neighbor), 2)
                queue.append((neighbor, path + [neighbor], new_dist))

    return float('inf'), []
