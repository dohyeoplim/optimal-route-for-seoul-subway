def format_route_segments(path):
    segments = []
    if not path:
        return segments

    current_line = path[0][1]
    segment_stations = [path[0][0]]

    for i in range(1, len(path)):
        station, line, direction = path[i]
        if line != current_line:
            segments.append((current_line, "-".join(segment_stations)))
            current_line = line
            segment_stations = [station]
        else:
            segment_stations.append(station)

    segments.append((current_line, " - ".join(segment_stations)))
    return segments