from data import lines, station_lines
from route_planner import RoutePlanner
from planner import SeoulMetroRoutePlanner
import time
import random

def analyze_hub_network():
    transfer_stations = {st: lns for st, lns in station_lines.items() if len(lns) > 1}

    print(f"총 지하철역 수: {len(station_lines)}")
    print(f"허브역 수: {len(transfer_stations)}")
    print(f"허브 비율: {len(transfer_stations)/len(station_lines)*100:.1f}%\n")

    print("주요 허브역(3개 호선 이상 커버):")
    major_hubs = [(st, len(lns)) for st, lns in transfer_stations.items() if len(lns) >= 3]
    for station, num_lines in sorted(major_hubs, key=lambda x: x[1], reverse=True):
        lines_str = ", ".join(map(str, sorted(transfer_stations[station])))
        print(f"  {station}: {num_lines}개 호선({lines_str})")

    return transfer_stations

def test_routing():
    hub_planner = RoutePlanner(lines, station_lines)
    test_cases = [
        ("서울역", "강남"),
        ("신도림", "왕십리"),
        ("소요산", "온양온천"),
        ("대화", "오금"),
        ("방화", "마천"),
        ("회기", "충무로"),
        ("합정", "건대입구"),
        ("교대", "을지로3가"),
    ]

    total_hub_time = 0

    for origin, destination in test_cases:
        print("-" * 60)
        print(f"\n{origin} → {destination}")

        start = time.perf_counter()
        hub_time, hub_path = hub_planner.find_route(origin, destination)
        hub_query_time = (time.perf_counter() - start) * 1000
        total_hub_time += hub_query_time

        print(f"이동시간: {hub_time}분")
        print(f"러닝타임: {hub_query_time:.2f}ms")

        print("겅로:")
        for line_info, segment in hub_planner.format_route(hub_path):
            print(f"{line_info}: {segment}")

    print("\n" + "=" * 80)
    print(f"평균 러닝타임: {total_hub_time/len(test_cases):.2f}ms")


if __name__ == "__main__":
    transfer_stations = analyze_hub_network()

    test_routing()