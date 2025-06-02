import pandas as pd
from collections import defaultdict
from .utils import PreprocessorUtils
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Set

class GraphBuilder:
    def __init__(self, csv_path: str):
        self.time_table = pd.read_csv(csv_path, encoding="cp949", low_memory=False)
        self.subway_graph: Dict[Tuple[str, str], List[Tuple[Tuple[str, str], float]]] = defaultdict(list)
        self.station_lines_map: Dict[str, Set[str]] = defaultdict(set)
        self.transfer_stations: Set[str] = set()
        self.utils = PreprocessorUtils(self)

    def build(self):
        segments = {
            "line_1_main": self.utils.get_segment("K112"),
            "line_1_junction_at_guro_main": self.utils.get_segment("K665"),
            "line_1_junction_at_geumcheon_gu_office":
                self.utils.cut_segment(self.utils.get_segment("K7022"), "광명", "금천구청"),
            "line_1_junction_at_byeongjeom":
                self.utils.cut_segment(self.utils.get_segment("K462"), "서동탄", "병점"),

            "line_2_circular": self.utils.get_segment("2293", line=2),
            "line_2_junction_kachisan": self.utils.get_segment("5609", line=2),
            "line_2_junction_sinsuldong": self.utils.get_segment("1612", line=2),

            "line_3_main": self.utils.get_segment("3224", line=3),

            "line_4_split_1": self.utils.get_segment("S4085", line=4),
            "line_4_split_2": self.utils.get_segment("S4507", line=4),

            "line_5_main": self.utils.get_segment("5117", line=5),
            "line_5_junction":
                self.utils.cut_segment(self.utils.get_segment("5631", line=5), "강동", "마천")
        }

        circular_segments = {"line_2_circular"}

        for line_name, df in segments.items():
            if df.empty:
                print(f"Warning: no data for {line_name}")
                continue

            forward_order = list(df["역사명"].drop_duplicates())
            is_circular = (line_name in circular_segments)
            travel_times = self._extract_train_times(df)

            if is_circular:
                first_st = forward_order[0]
                last_st = forward_order[-1]
                if first_st != last_st:
                    closing_key = (last_st, first_st)
                    if closing_key not in travel_times:
                        travel_times[closing_key] = 2.0

            for (u, v), w in travel_times.items():
                if u not in forward_order or v not in forward_order:
                    continue

                node_u = (u, line_name)
                node_v = (v, line_name)

                if (node_v, w) not in self.subway_graph[node_u]:
                    self.subway_graph[node_u].append((node_v, w))
                if (node_u, w) not in self.subway_graph[node_v]:
                    self.subway_graph[node_v].append((node_u, w))

                self.station_lines_map[u].add(line_name)
                self.station_lines_map[v].add(line_name)

        branch_connections = {
            "line_1_junction_at_guro_main": ("구로", "line_1_main"),
            "line_1_junction_at_geumcheon_gu_office": ("금천구청", "line_1_junction_at_guro_main"),
            "line_1_junction_at_byeongjeom": ("병점", "line_1_junction_at_guro_main"),
            "line_2_junction_kachisan": ("신도림", "line_2_circular"),
            "line_2_junction_sinsuldong": ("성수", "line_2_circular"),
            "line_5_junction": ("강동", "line_5_main"),
        }

        for branch_line, (connection_station, main_line) in branch_connections.items():
            if branch_line not in segments or segments[branch_line].empty:
                continue

            node_branch = (connection_station, branch_line)
            node_main   = (connection_station, main_line)

            if node_branch in self.subway_graph and node_main in self.subway_graph:
                if (node_main, 2.0) not in self.subway_graph[node_branch]:
                    self.subway_graph[node_branch].append((node_main, 2.0))
                if (node_branch, 2.0) not in self.subway_graph[node_main]:
                    self.subway_graph[node_main].append((node_branch, 2.0))
            else:
                print(f"분기 연결 불가! - {branch_line} / {connection_station}")

        for station, lines in self.station_lines_map.items():
            if len(lines) <= 1:
                continue
            lines_list = list(lines)
            for i in range(len(lines_list)):
                for j in range(i+1, len(lines_list)):
                    l1, l2 = lines_list[i], lines_list[j]
                    node1, node2 = (station, l1), (station, l2)
                    if node1 in self.subway_graph and node2 in self.subway_graph:
                        if (node2, 2.0) not in self.subway_graph[node1]:
                            self.subway_graph[node1].append((node2, 2.0))
                        if (node1, 2.0) not in self.subway_graph[node2]:
                            self.subway_graph[node2].append((node1, 2.0))

        self.transfer_stations = {
            station for station, lines in self.station_lines_map.items() if len(lines) > 1
        }

        print(f"\n그래프 결과:")
        print(f"총 노드: {len(self.subway_graph)}")
        print(f"총 엣지: {sum(len(v) for v in self.subway_graph.values())}")
        print(f"환승역: {len(self.transfer_stations)}")
        print(f"분기역: {len(branch_connections)}")
        print("="*50)

    def get_graph(self) -> Dict[Tuple[str, str], List[Tuple[Tuple[str, str], float]]]:
        return self.subway_graph

    def get_transfer_stations(self) -> Set[str]:
        return self.transfer_stations

    def get_station_lines_map(self) -> Dict[str, Set[str]]:
        return self.station_lines_map

    def get_hub_nodes(self) -> Set[str]:
        return {station for station, lines in self.station_lines_map.items() if len(lines) > 1}

    def _extract_train_times(self, train_df: pd.DataFrame) -> Dict[Tuple[str, str], float]:
        times: Dict[Tuple[str, str], float] = {}
        for i in range(len(train_df) - 1):
            curr, nxt = train_df.iloc[i], train_df.iloc[i + 1]
            if curr["역사명"] == nxt["역사명"]:
                continue

            try:
                if pd.isna(curr["열차출발시간"]) and not pd.isna(curr["열차도착시간"]):
                    depart = datetime.strptime(curr["열차도착시간"], "%H:%M:%S") + timedelta(seconds=30)
                else:
                    depart = datetime.strptime(curr["열차출발시간"], "%H:%M:%S")

                arrive = datetime.strptime(nxt["열차도착시간"], "%H:%M:%S")
                diff_secs = (arrive - depart).seconds
                if arrive < depart:
                    diff_secs += 86400
                minutes = diff_secs / 60.0

                if 0 < minutes <= 60:
                    times[(curr["역사명"], nxt["역사명"])] = round(minutes, 2)
            except Exception:
                continue

        return times