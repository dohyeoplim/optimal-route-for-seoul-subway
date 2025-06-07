from route_planner import RoutePlanner
import time

def main():
    subway_data = "./input/seoul_metro.csv"

    planner = RoutePlanner(subway_data, transfer_time=2.0)

    origin = input('출발역: ').strip()
    destination = input('도착역: ').strip()

    t1 = time.perf_counter()
    time_min, path = planner.find_route(origin, destination)
    t2 = time.perf_counter()

    print(f"{origin} -> {destination}: {time_min}분 소요")
    for ln, seg in planner.format_route(path):
        print(f"{ln}: {seg}")

    print(f"[⏱] 쿼리 시간: {(t2 - t1) * 1000:.2f} ms")


if __name__ == '__main__':
    main()
