# 🚇 Fast Pathfinding on the Seoul Metro with Hub Indexing

[![Open in Figma](https://img.shields.io/badge/Open%20in-Figma%20Slides-orange?logo=figma&logoColor=white)](https://www.figma.com/deck/5x6KgCPvpCXWInCwpLzRn1/DSA-Spring-2025-Project?node-id=1-1935&viewport=-186%2C-48%2C0.84&t=zyjp3C7K4stFfWvW-1&scaling=min-zoom&content-scaling=fixed&page-id=0%3A1)

![24](https://github.com/user-attachments/assets/8a2c07cf-0fbd-4325-84a9-8a28a65a398c)


<br/>

Developed by:

- **Dohyeop Lim** — Dept. of Artificial Intelligence, Seoul National University of Science and Technology
- **Soyeung Park** — Dept. of Artificial Intelligence, Seoul National University of Science and Technology
- **Taeho Park** — Dept. of Artificial Intelligence, Seoul National University of Science and Technology

<br/>

## 🚀 Quick Start

**Project Structure:**
```plaintext
├── main.py                # Entry point for route queries
├── route_planner/
│   ├── core.py            # Main module
│   ├── preprocessing/     # Constructs graph from raw csv time table
│   ├── precompute/        # Precomputes hub-station-routes
│   └── pathfinder/        # Hub-aware route search logic
├── input/seoul_metro.csv  # Raw subway time table data
└── README.md
```

**How to Use:**
```bash
python main.py
```

Then enter:
```plaintext
출발역: 시청
도착역: 동작
```

Expected Output:
```plaintext
시청 -> 동작: 15.0분 소요
1호선: 시청 - 서울역
4호선: 서울역 - 숙대입구 - 삼각지 - 신용산 - 이촌 - 동작
```

<br/>

## 📂 Source Dataset

[서울 도시철도 열차운행시각표](https://www.data.go.kr/data/15098251/fileData.do)
  - Provider: data.go.kr, Ministry of the Interior and Safety
  - Provides information by line number and includes the following attributes: `호선`, `역사코드`, `역사명`, `방향`, `도착시간`, `출발시간` for each train operation.

<br/>

## 🧠 Algorithm Overview

### 1. 🛠 Preprocessing Phase

| Phase                     | Description                                                        | Data Structure                            |
|--------------------------|--------------------------------------------------------------------|-------------------------------------------|
| Hub Nodes Identification | Extract nodes in the hub list                    | `hub_nodes: Set[(station, line, dir)]`    |
| Hub ↔ Hub Path Search    | Run Dijkstra                           | `hub_distances: Dict[hub → {target: (distance, path)}]` |
| Regular → Hub Mapping    | Find reachable hubs                        | `station_to_hubs: Dict[node → List[(hub, distance, path)]]` |
| Hub → Regular Mapping    | Inverse mapping to connect hubs back to regular nodes (top-k)           | `hubs_to_station: Dict[node → List[(hub, distance, path)]]` |
| Edge Weights Extraction  | Flatten all weighted edges                         | `edge_weights: Dict[(from, to) → weight]` |

### 2. ⚡ Query Phase

| Case                                     | Resolution Strategy                                                                          | Time Complexity |
|-----------------------------------------------------------------|----------------------------------------------------------------------------------------------|------------------|
| Hub → Hub                    | Direct lookup from `hub_distances`                                                          | $O(1)$             |
| Hub → Regular / Regular → Hub       | Lookup nearest hubs for regular node → merge with `hub_distances`                       | $O(k)$, $k$ = # of hubs |
| Regular → Regular                  | Regular → Nearest Hub → Hub Network → Nearest Hub → Regular                                 | $O(k^2)$, precomputed |


<br/>

## 🧪 Performance Evaluation

### ⏱ Query Time
| Query Type         | Avg. Latency (ms) | Speedup |
|--------------------|--------------|-----------------------|
| Dijkstra (Baseline)| 0.25         | —                     |
| Hub → Hub          | **0.06**     | **4.17× Faster**      |
| Hub → Regular      | **0.09**     | **2.78× Faster**      |
| Regular → Regular  | **0.21**     | **1.19× Faster**      |
