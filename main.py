from route_planner import RoutePlanner

def main():
    subway_data = "./input/seoul_metro.csv"

    planner = RoutePlanner(subway_data, transfer_time=2.0)

    origin = input('출발역: ').strip()
    destination = input('도착역: ').strip()

    time, path = planner.find_route(origin, destination)
    print(f"{origin} -> {destination}: {time}분 소요")
    for ln, seg in planner.format_route(path):
        print(f"{ln}: {seg}")

if __name__ == '__main__':
    main()
