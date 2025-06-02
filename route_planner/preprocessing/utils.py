import pandas as pd
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Set

class PreprocessorUtils:
    def __init__(self, builder):
        self.builder = builder

    def get_segment(self, code: str, line: int = None, day: str = "DAY") -> pd.DataFrame:
        query = (self.builder.time_table['열차코드'] == code) & (self.builder.time_table['주중주말'] == day)
        if line is not None:
            query &= self.builder.time_table['호선'] == line
        return self.builder.time_table[query].sort_values("열차출발시간").reset_index(drop=True)

    @staticmethod
    def cut_segment(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
        start_idx = df[df['역사명'] == start].index[0]
        end_idx = df[df['역사명'] == end].index[0]
        if start_idx > end_idx:
            start_idx, end_idx = end_idx, start_idx
        return df.iloc[start_idx:end_idx + 1].reset_index(drop=True)

    @staticmethod
    def extract_train_times(train_df: pd.DataFrame) -> Dict[Tuple[str, str], float]:
        times = {}
        for i in range(len(train_df) - 1):
            current = train_df.iloc[i]
            next_st = train_df.iloc[i + 1]

            if current['역사명'] == next_st['역사명']:
                continue

            try:
                if pd.isna(current['열차출발시간']) and not pd.isna(current['열차도착시간']):
                    depart = datetime.strptime(current['열차도착시간'], '%H:%M:%S') + timedelta(seconds=30)
                else:
                    depart = datetime.strptime(current['열차출발시간'], '%H:%M:%S')

                arrive = datetime.strptime(next_st['열차도착시간'], '%H:%M:%S')

                minutes = (arrive - depart).seconds / 60 if arrive >= depart else ((arrive - depart).seconds + 86400) / 60

                if 0 < minutes <= 60:
                    times[(current['역사명'], next_st['역사명'])] = round(minutes, 2)
            except Exception:
                continue

        return times
    @staticmethod
    def identify_hub_nodes(station_lines: Dict[str, Set[str]]):
        hub_nodes = set()
        for station, lines in station_lines.items():
            if len(lines) > 1:
                for line in lines:
                    hub_nodes.add((station, line, "F"))
                    hub_nodes.add((station, line, "B"))
        return hub_nodes
