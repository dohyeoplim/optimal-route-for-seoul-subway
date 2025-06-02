import pandas as pd
from data import lines, station_lines
from route_planner.travel_time.core import TravelTimeExtractor


if __name__ == "__main__":
    time_table = pd.read_csv('input/seoul_metro.csv', encoding="cp949", low_memory=False)

    line_train_map = {
        1: "K106",
        2: "2246", # 성수 to 성수, 외선!
        3: "3168K",
        4: "4024",
        5: "5550",
    }

    extractor = TravelTimeExtractor(time_table)

    results = extractor.extract_line(line_train_map=line_train_map)

    print(results)
