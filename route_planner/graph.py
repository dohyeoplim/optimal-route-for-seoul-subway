from collections import defaultdict
from typing import Dict, List, Tuple

def build_transfer_stations(station_lines: Dict[str, List[int]]):
    return {st: lns for st, lns in station_lines.items() if len(lns) > 1}

class GraphBuilder:
    def __init__(self, lines: Dict[int, List[str]], station_lines: Dict[str, List[int]]):
        self.lines = lines
        self.station_lines = station_lines
        self.transfer_stations = build_transfer_stations(station_lines)

    def build(self):
        graph = defaultdict(list)
        edge_weights = {}

        for line_no, stations in self.lines.items():
            for i in range(len(stations) - 1):
                u = (stations[i], line_no, 'F')
                v = (stations[i+1], line_no, 'F')
                graph[u].append(v)
                edge_weights[(u, v)] = 2
            for i in range(len(stations) - 1, 0, -1):
                u = (stations[i], line_no, 'B')
                v = (stations[i-1], line_no, 'B')
                graph[u].append(v)
                edge_weights[(u, v)] = 2

        for station, line_list in self.transfer_stations.items():
            nodes = [(station, line, d) for line in line_list for d in ('F', 'B')]
            for i in range(len(nodes)):
                for j in range(len(nodes)):
                    if i != j:
                        graph[nodes[i]].append(nodes[j])
                        edge_weights[(nodes[i], nodes[j])] = 2 if nodes[i][2] == nodes[j][2] else 3

        return graph, edge_weights, self.transfer_stations
