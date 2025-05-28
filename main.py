from data import lines, station_lines
from route_planner import RoutePlanner

def main():
    planner = RoutePlanner(lines, station_lines)
    origin = input('출발역: ').strip()
    destination = input('도착역: ').strip()

    time, path = planner.find_route(origin, destination)
    print(f"{origin} -> {destination}: {time}분 소요")
    for ln, seg in planner.format_route(path):
        print(f"{ln}호선: {seg}")

if __name__ == '__main__':
    main()
