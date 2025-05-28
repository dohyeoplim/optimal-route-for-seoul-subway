def format_route_segments(path):
    segments = []
    if not path:
        return segments

    current_line = path[0][1]
    current_direction = path[0][2]
    segment_stations = [path[0][0]]

    for i in range(1, len(path)):
        station, line, direction = path[i]
        if line != current_line:
            direction_str = "→" if current_direction == 'F' else "←"
            segments.append((f"{current_line} {direction_str}", " - ".join(segment_stations)))
            current_line, current_direction = line, direction
            segment_stations = [station]
        else:
            segment_stations.append(station)

    direction_str = "→" if current_direction == 'F' else "←"
    segments.append((f"{current_line} {direction_str}", " - ".join(segment_stations)))
    return segments