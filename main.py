from data import lines, station_lines
from planner import SeoulMetroRoutePlanner

def main():
    planner = SeoulMetroRoutePlanner(lines, station_lines)
    origin = input('Origin station: ').strip()
    destination = input('Destination station: ').strip()

    time, path = planner.find_fastest_route(origin, destination)
    print(f"Fastest route from {origin} to {destination}: {time} minutes")
    for ln, seg in planner.format_route(path):
        print(f"Take Line {ln}: {seg}")

if __name__ == '__main__':
    main()
