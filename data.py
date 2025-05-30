from collections import defaultdict # ?
# 분기선을 포함한 새로운 데이터 구조
_RAW_LINES = {
    # 1호선 메인라인 (소요산-인천, 가산디지털단지-신창)
    1: """
소요산 - 동두천 - 보산 - 동두천중앙 - 지행 - 덕정 - 덕계 - 양주 - 녹양 - 가능 - 의정부 - 회룡 - 망월사 - 도봉산 - 도봉 - 방학 - 창동 - 녹천 - 월계 - 성북 - 석계 - 신이문 - 외대앞 - 회기 - 청량리 - 제기동 - 신설동 - 동묘앞 - 동대문 - 종로5가 - 종로3가 - 종각 - 시청 - 서울역 - 남영 - 용산 - 노량진 - 대방 - 신길 - 영등포 - 신도림 - 구로 - 구일 - 개봉 - 오류동 - 온수 - 역곡 - 소사 - 부천 - 중동 - 송내 - 부개 - 부평 - 백운 - 동암 - 간석 - 주안 - 도화 - 제물포 - 도원 - 동인천 - 인천
""",
    
    # 1호선 수원-신창 구간 (가산디지털단지에서 연결)
    "1_suwon": """
구로 - 가산디지털단지 - 독산 - 금천구청 - 석수 - 관악 - 안양 - 명학 - 금정 - 군포 - 당정 - 의왕 - 성균관대 - 화서 - 수원 - 세류 - 병점 - 세마 - 오산대 - 오산 - 진위 - 송탄 - 서정리 - 지제 - 평택 - 성환 - 직산 - 두정 - 천안 - 봉명 - 쌍용 - 아산 - 배방 - 온양온천 - 신창
""",
    
    # 1호선 광명 분기선
    "1_gwangmyeong": """
금천구청 - 광명
""",
    
    # 1호선 서동탄 분기선
    "1_sdt": """
병점 - 서동탄
""",
    
    # 2호선 (순환선이므로 분기 없음)
    2: """
시청 - 을지로입구 - 을지로3가 - 을지로4가 - 동대문역사문화공원 - 신당 - 상왕십리 - 왕십리 - 한양대 - 뚝섬 - 성수 - 건대입구 - 구의 - 강변 - 잠실나루 - 잠실 - 신천 - 종합운동장 - 삼성 - 선릉 - 역삼 - 강남 - 교대 - 서초 - 방배 - 사당 - 낙성대 - 서울대입구 - 봉천 - 신림 - 신대방 - 구로디지털단지 - 대림 - 신도림 - 문래 - 영등포구청 - 당산 - 합정 - 홍대입구 - 신촌 - 이대 - 아현 - 충정로 - 시청
""",
    
    # 3호선
    3: """
대화 - 주엽 - 정발산 - 마두 - 백석 - 대곡 - 화정 - 원당 - 삼송 - 지축 - 구파발 - 연신내 - 불광 - 녹번 - 홍제 - 무악재 - 독립문 - 경복궁 - 안국 - 종로3가 - 을지로3가 - 충무로 - 동대입구 - 약수 - 금호 - 옥수 - 압구정 - 신사 - 잠원 - 고속터미널 - 교대 - 남부터미널 - 양재 - 매봉 - 도곡 - 대치 - 학여울 - 대청 - 일원 - 수서 - 가락시장 - 경찰병원 - 오금
""",
    
    # 4호선
    4: """
진접 - 오남 - 별내별가람 - 당고개 - 상계 - 노원 - 창동 - 쌍문 - 수유 - 미아 - 미아삼거리 - 길음 - 성신여대입구 - 한성대입구 - 혜화 - 동대문 - 동대문역사문화공원 - 충무로 - 명동 - 회현 - 서울역 - 숙대입구 - 삼각지 - 신용산 - 이촌 - 동작 - 이수 - 사당 - 남태령 - 선바위 - 경마공원 - 대공원 - 과천 - 정부과천청사 - 인덕원 - 평촌 - 범계 - 금정 - 산본 - 수리산 - 대야미 - 반월 - 상록수 - 한대앞 - 중앙 - 고잔 - 공단 - 안산 - 신길온천 - 정왕 - 오이도
""",
    
    # 5호선 메인라인 (방화-강동)
    5: """
방화 - 개화산 - 김포공항 - 송정 - 마곡 - 발산 - 우장산 - 화곡 - 까치산 - 신정 - 목동 - 오목교 - 양평 - 영등포구청 - 영등포시장 - 신길 - 여의도 - 여의나루 - 마포 - 공덕 - 애오개 - 충정로 - 서대문 - 광화문 - 종로3가 - 을지로4가 - 동대문역사문화공원 - 청구 - 신금호 - 행당 - 왕십리 - 마장 - 답십리 - 장한평 - 군자 - 아차산 - 광나루 - 천호 - 강동
""",
    
    # 5호선 상일동지선 (강동-상일동)
    "5_sangil": """
강동 - 길동 - 굽은다리 - 명일 - 고덕 - 상일동
""",
    
    # 5호선 마천지선 (강동-마천, 둔촌동 경유)
    "5_macheon": """
강동 - 둔촌동 - 올림픽공원 - 방이 - 오금 - 개롱 - 거여 - 마천
""",
}

# 분기점 정보 (어떤 역에서 어떤 분기선들이 만나는지)
BRANCH_CONNECTIONS = {
    "가산디지털단지": [1, "1_suwon", "1_gwangmyeong"],  # 1호선 메인, 수원방면, 광명방면
    "병점": ["1_suwon", "1_sdt"],  # 수원방면, 서동탄방면
    "강동": [5, "5_sangil", "5_macheon"],  # 5호선 메인, 상일동지선, 마천지선
}

def process_lines():
    """라인 데이터를 처리하여 그래프 구축에 필요한 정보 생성"""
    lines = {}
    station_lines_temp = defaultdict(list)
    
    for line_key, stations_str in _RAW_LINES.items():
        # 역 이름 추출 및 정리
        stations = [s.strip() for s in stations_str.split('-') if s.strip()]
        lines[line_key] = stations
        
        # 각 역이 어떤 노선에 속하는지 기록
        for station in stations:
            station_lines_temp[station].append(line_key)
    
    # 노선 번호 정렬
    station_lines = {station: sorted(line_list, key=lambda x: (str(x).split('_')[0], str(x))) 
                    for station, line_list in station_lines_temp.items()}
    
    # 환승역 찾기 (2개 이상의 노선이 지나는 역)
    transfer_map = {station: lines_list for station, lines_list in station_lines.items() 
                   if len(lines_list) > 1}#종로3가: [1, 3, 5]
    
    return lines, station_lines, transfer_map

# 데이터 처리
lines, station_lines, transfer_map = process_lines()




# # 결과 출력 (테스트용)
# if __name__ == "__main__":
#     print("=== 노선별 역 목록 ===")
#     for line_key, stations in lines.items():
#         print(f"{line_key}: {len(stations)}개 역")
#         print(f"  시작: {stations[0]} -> 끝: {stations[-1]}")
    
#     print("\n=== 환승역 예시 (처음 5개) ===")
#     for i, (station, lines_list) in enumerate(transfer_map.items()):
#         if i >= 5:
#             break
#         print(f"{station}: {lines_list}")

# #  main . py ( 객체 분리 )
# from data import lines, station_lines
# from route_planner import RoutePlanner

# def main():
#     planner = RoutePlanner(lines, station_lines)
#     origin = input('출발역: ').strip()
#     destination = input('도착역: ').strip()

#     time, path = planner.find_route(origin, destination)
#     print(f"{origin} -> {destination}: {time}분 소요")
#     for ln, seg in planner.format_route(path):
#         print(f"{ln}호선: {seg}")

# if __name__ == '__main__':
#     main()


# # # planner.py
# # import networkx as nx

# # class SeoulMetroRoutePlanner:
# #     def __init__(self, lines: dict[int, list[str]], station_lines: dict[str, list[int]]):
# #         self.lines = lines
# #         self.station_lines = station_lines
# #         self.transfer_map = {st: lns for st, lns in station_lines.items() if len(lns) > 1}

# #         self.graph = nx.Graph()
# #         self._build_graph()

# #     def _build_graph(self) -> None:
# #         # 1) Intra-line
# #         for ln, stations in self.lines.items():
# #             for u, v in zip(stations, stations[1:]):
# #                 n1 = f"{u} (L{ln})"
# #                 n2 = f"{v} (L{ln})"
# #                 self.graph.add_edge(n1, n2, weight=2)

# #         # 2) Transfer
# #         for st, lns in self.transfer_map.items():
# #             nodes = [f"{st} (L{ln})" for ln in lns]
# #             for i in range(len(nodes)):
# #                 for j in range(i+1, len(nodes)):
# #                     self.graph.add_edge(nodes[i], nodes[j], weight=2)

# #     def find_fastest_route(self, origin: str, destination: str) -> tuple[int, list[str]]:
# #         starts = [f"{origin} (L{ln})" for ln in self.station_lines.get(origin, [])]
# #         ends   = [f"{destination} (L{ln})" for ln in self.station_lines.get(destination, [])]

# #         if not starts:
# #             raise ValueError(f"Unknown origin station: {origin}")
# #         if not ends:
# #             raise ValueError(f"Unknown destination station: {destination}")

# #         best_time = float('inf')
# #         best_path: list[str] = []
# #         for s in starts:
# #             for t in ends:
# #                 try:
# #                     time, path = nx.single_source_dijkstra(self.graph, s, t)
# #                     if time < best_time:
# #                         best_time, best_path = time, path
# #                 except (nx.NetworkXNoPath, nx.NodeNotFound):
# #                     continue

# #         if not best_path:
# #             raise ValueError(f"No route found between {origin} and {destination}.")
# #         return best_time, best_path

# #     @staticmethod
# #     def format_route(path: list[str]) -> list[tuple[str, str]]:
# #         legs: list[tuple[str, str]] = []
# #         current_ln = None
# #         segment: list[str] = []
# #         for node in path:
# #             st, ln_tag = node.rsplit(' ', 1)
# #             ln = ln_tag.strip('()')
# #             if ln != current_ln:
# #                 if segment:
# #                     legs.append((current_ln, ' - '.join(segment)))
# #                 current_ln = ln
# #                 segment = [st]
# #             else:
# #                 segment.append(st)
# #         if segment:
# #             legs.append((current_ln, ' - '.join(segment)))
# #         return legs
