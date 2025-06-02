import re
from typing import List, Tuple

def format_route_segments(path: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    segments: List[Tuple[str, str]] = []
    if not path:
        return segments

    def line_label(internal_line: str) -> str:
        m = re.match(r"line_(\d+)", internal_line)
        return f"{m.group(1)}호선" if m else internal_line

    current_line = path[0][1]
    current_label = line_label(current_line)
    segment_stations = [path[0][0]]

    for station, line in path[1:]:
        if line != current_line:
            segments.append((current_label, " - ".join(segment_stations)))
            current_line = line
            current_label = line_label(current_line)
            segment_stations = [station]
        else:
            segment_stations.append(station)

    segments.append((current_label, " - ".join(segment_stations)))
    return segments