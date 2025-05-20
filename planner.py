import networkx as nx

class SeoulMetroRoutePlanner:
    def __init__(self, lines: dict[int, list[str]], station_lines: dict[str, list[int]]):
        self.lines = lines
        self.station_lines = station_lines
        self.transfer_map = {st: lns for st, lns in station_lines.items() if len(lns) > 1}

        self.graph = nx.Graph()
        self._build_graph()

    def _build_graph(self) -> None:
        # 1) Intra-line
        for ln, stations in self.lines.items():
            for u, v in zip(stations, stations[1:]):
                n1 = f"{u} (L{ln})"
                n2 = f"{v} (L{ln})"
                self.graph.add_edge(n1, n2, weight=2)

        # 2) Transfer
        for st, lns in self.transfer_map.items():
            nodes = [f"{st} (L{ln})" for ln in lns]
            for i in range(len(nodes)):
                for j in range(i+1, len(nodes)):
                    self.graph.add_edge(nodes[i], nodes[j], weight=2)

    def find_fastest_route(self, origin: str, destination: str) -> tuple[int, list[str]]:
        starts = [f"{origin} (L{ln})" for ln in self.station_lines.get(origin, [])]
        ends   = [f"{destination} (L{ln})" for ln in self.station_lines.get(destination, [])]

        if not starts:
            raise ValueError(f"Unknown origin station: {origin}")
        if not ends:
            raise ValueError(f"Unknown destination station: {destination}")

        best_time = float('inf')
        best_path: list[str] = []
        for s in starts:
            for t in ends:
                try:
                    time, path = nx.single_source_dijkstra(self.graph, s, t)
                    if time < best_time:
                        best_time, best_path = time, path
                except (nx.NetworkXNoPath, nx.NodeNotFound):
                    continue

        if not best_path:
            raise ValueError(f"No route found between {origin} and {destination}.")
        return best_time, best_path

    @staticmethod
    def format_route(path: list[str]) -> list[tuple[str, str]]:
        legs: list[tuple[str, str]] = []
        current_ln = None
        segment: list[str] = []
        for node in path:
            st, ln_tag = node.rsplit(' ', 1)
            ln = ln_tag.strip('()')
            if ln != current_ln:
                if segment:
                    legs.append((current_ln, ' - '.join(segment)))
                current_ln = ln
                segment = [st]
            else:
                segment.append(st)
        if segment:
            legs.append((current_ln, ' - '.join(segment)))
        return legs
