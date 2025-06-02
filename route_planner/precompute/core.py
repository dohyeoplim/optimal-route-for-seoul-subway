import time
from collections import defaultdict
from typing import Dict, Set, Tuple, List, Optional
from .utils import dijkstra_from_node

class HubPrecomputer:
    def __init__(
            self,
            graph: Dict[Tuple[str, str, str], List[Tuple[Tuple[str, str, str], float]]],
            hub_stations: Set[str]
    ):
        self.graph = graph
        self.hub_stations = hub_stations

        self.edge_weights = {}
        for node, neighbors in graph.items():
            for neighbor, weight in neighbors:
                self.edge_weights[(node, neighbor)] = weight

        self.hub_distances: Dict[
            Tuple[str, str, str],
            Dict[Tuple[str, str, str], Tuple[float, List[Tuple[str, str, str]]]]
        ] = {}

        self.station_to_hubs: Dict[
            Tuple[str, str, str],
            List[Tuple[Tuple[str, str, str], float, List[Tuple[str, str, str]]]]
        ] = defaultdict(list)

        self.hubs_to_station: Dict[
            Tuple[str, str, str],
            List[Tuple[Tuple[str, str, str], float, List[Tuple[str, str, str]]]]
        ] = defaultdict(list)

    def precompute_hub_data(self):
        print(f"허브역 {len(self.hub_stations)}개")
        start_time = time.time()

        all_nodes = set(self.graph.keys())

        hub_nodes = {node for node in all_nodes if node[0] in self.hub_stations}
        non_hub_nodes = all_nodes - hub_nodes

        print(f"- 허브 노드: {len(hub_nodes)}개")
        print(f"- 일반 노드: {len(non_hub_nodes)}개")

        print("1단계: 허브 간 거리 계산")
        hub_count = 0
        for hub_node in hub_nodes:
            distances, paths = dijkstra_from_node(self.graph, self.edge_weights, hub_node)

            self.hub_distances[hub_node] = {}
            for target_node in hub_nodes:
                if target_node != hub_node and target_node in distances:
                    self.hub_distances[hub_node][target_node] = (
                        distances[target_node],
                        paths[target_node]
                    )

            hub_count += 1

        print("2단계: 일반역 → 허브역 거리 계산")
        node_count = 0
        for node in non_hub_nodes:
            distances, paths = dijkstra_from_node(self.graph, self.edge_weights, node)

            reachable_hubs = []
            for hub_node in hub_nodes:
                if hub_node in distances:
                    reachable_hubs.append((
                        hub_node,
                        distances[hub_node],
                        paths[hub_node]
                    ))

            reachable_hubs.sort(key=lambda x: x[1])
            self.station_to_hubs[node] = reachable_hubs[:10]

            node_count += 1

        print("3단계: 허브역 → 일반역 거리 계산")
        hub_count = 0
        for hub_node in hub_nodes:
            distances, paths = dijkstra_from_node(self.graph, self.edge_weights, hub_node)

            for node in non_hub_nodes:
                if node in distances:
                    self.hubs_to_station[node].append((
                        hub_node,
                        distances[node],
                        paths[node]
                    ))

            hub_count += 1

        for node in non_hub_nodes:
            self.hubs_to_station[node].sort(key=lambda x: x[1])
            self.hubs_to_station[node] = self.hubs_to_station[node][:10]

        elapsed_time = time.time() - start_time
        print(f"Done. 소요 시간: {elapsed_time:.2f}초")
        print("="*50)

        self._print_statistics()

        print("=" * 50)

    def _print_statistics(self):
        hub_node_count = sum(1 for node in self.graph if node[0] in self.hub_stations)
        total_node_count = len(self.graph)
        coverage = (hub_node_count / total_node_count) * 100

        print(f"허브 커버리지: {hub_node_count}/{total_node_count} ({coverage:.1f}%)")

        if self.station_to_hubs:
            avg_hubs_per_station = sum(len(hubs) for hubs in self.station_to_hubs.values()) / len(self.station_to_hubs)
            print(f"역당 평균 연결 허브: {avg_hubs_per_station:.1f}개")

        total_entries = (
                sum(len(d) for d in self.hub_distances.values()) +
                sum(len(l) for l in self.station_to_hubs.values()) +
                sum(len(l) for l in self.hubs_to_station.values())
        )
        print(f"총 저장된 경로 수: {total_entries:,}")
