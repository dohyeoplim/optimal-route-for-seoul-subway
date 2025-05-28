from .utils import find_direct_path

def direct_route(start_nodes, end_nodes, *args):
    graph = args[-2]
    edge_weights = args[-1]

    best_time = float('inf')
    best_path = []

    for start in start_nodes:
        for end in end_nodes:
            if start[1] == end[1]: # 같은 호선
                dist, path = find_direct_path(graph, edge_weights, start, end)
                if dist < best_time:
                    best_time = dist
                    best_path = path

    return best_time, best_path


def hub_to_hub(start_nodes, end_nodes, hub_nodes, hub_distances, *args):
    best_time = float('inf')
    best_path = []

    for start in start_nodes:
        for end in end_nodes:
            if start in hub_nodes and end in hub_nodes:
                if start in hub_distances and end in hub_distances.get(start, {}):
                    dist, path = hub_distances[start][end]
                    if dist < best_time:
                        best_time = dist
                        best_path = path

    return best_time, best_path


def hub_to_regular(start_nodes, end_nodes, hub_nodes, hub_distances,
                        station_to_hubs, hubs_to_station, *args):
    best_time = float('inf')
    best_path = []

    for start in start_nodes:
        for end in end_nodes:
            if start in hub_nodes and end not in hub_nodes and end in hubs_to_station:
                for hub, d2, p2 in hubs_to_station[end]:
                    if start in hub_distances and hub in hub_distances.get(start, {}):
                        d1, p1 = hub_distances[start][hub]
                        total = d1 + d2
                        if total < best_time:
                            best_time = total
                            best_path = p1[:-1] + p2 if start != hub else p2

    return best_time, best_path


def regular_to_hub(start_nodes, end_nodes, hub_nodes, hub_distances,
                        station_to_hubs, hubs_to_station, *args):
    best_time = float('inf')
    best_path = []

    for start in start_nodes:
        for end in end_nodes:
            if start not in hub_nodes and end in hub_nodes and start in station_to_hubs:
                for hub, d1, p1 in station_to_hubs[start]:
                    if hub in hub_distances and end in hub_distances.get(hub, {}):
                        d2, p2 = hub_distances[hub][end]
                        total = d1 + d2
                        if total < best_time:
                            best_time = total
                            best_path = p1[:-1] + p2 if hub != end else p1

    return best_time, best_path


def regular_to_regular(start_nodes, end_nodes, hub_nodes, hub_distances,
                            station_to_hubs, hubs_to_station, *args):
    best_time = float('inf')
    best_path = []

    for start in start_nodes:
        for end in end_nodes:
            if (start not in hub_nodes and end not in hub_nodes and
                    start in station_to_hubs and end in hubs_to_station):

                for hub1, d1, p1 in station_to_hubs[start]:
                    for hub2, d3, p3 in hubs_to_station[end]:
                        if hub1 == hub2:
                            total = d1 + d3
                            if total < best_time:
                                best_time = total
                                best_path = p1[:-1] + p3
                        elif hub1 in hub_distances and hub2 in hub_distances.get(hub1, {}):
                            d2, p2 = hub_distances[hub1][hub2]
                            total = d1 + d2 + d3
                            if total < best_time:
                                best_time = total
                                best_path = p1[:-1] + p2[:-1] + p3

    return best_time, best_path
