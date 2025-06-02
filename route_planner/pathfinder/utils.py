from typing import List, Tuple, Dict, Set
from collections import deque

def get_station_nodes(
        station_name: str,
        station_lines_map: Dict[str, Set[str]],
        graph: Dict[Tuple[str, str], List[Tuple[Tuple[str, str], float]]]
) -> List[Tuple[str, str]]:
    nodes: List[Tuple[str, str]] = []
    lines = station_lines_map.get(station_name, set())
    for line in lines:
        node = (station_name, line)
        if node in graph:
            nodes.append(node)
    return nodes

def find_direct_path(graph: Dict, edge_weights: Dict,
                     start: Tuple[str, str, str],
                     end: Tuple[str, str, str]) -> Tuple[float, List[Tuple[str, str, str]]]:
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
