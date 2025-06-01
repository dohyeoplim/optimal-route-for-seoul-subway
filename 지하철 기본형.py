#!/usr/bin/env python
# coding: utf-8

# In[1]:


import heapq
from collections import defaultdict

# 기존 데이터 입력부 (생략하고 동일, 그대로 복사 가능)
lines = {
    1: "소요산 - 동두천 - 보산 - 동두천중앙 - 지행 - 덕정 - 덕계 - 양주 - 녹양 - 가능 - 의정부 - 회룡 - 망월사 - 도봉산 - 도봉 - 방학 - 창동 - 녹천 - 월계 - 성북 - 석계 - 신이문 - 외대앞 - 회기 - 청량리 - 제기동 - 신설동 - 동묘앞 - 동대문 - 종로5가 - 종로3가 - 종각 - 시청 - 서울역 - 남영 - 용산 - 노량진 - 대방 - 신길 - 영등포 - 신도림 - 구로 - 구일 - 개봉 - 오류동 - 온수 - 역곡 - 소사 - 부천 - 중동 - 송내 - 부개 - 부평 - 백운 - 동암 - 간석 - 주안 - 도화 - 제물포 - 도원 - 동인천 - 인천 - 광명 - 가산디지털단지 - 독산 - 금천구청 - 석수 - 관악 - 안양 - 명학 - 금정 - 군포 - 당정 - 의왕 - 성균관대 - 화서 - 수원 - 세류 - 병점 - 세마 - 오산대 - 오산 - 진위 - 송탄 - 서정리 - 지제 - 평택 - 성환 - 직산 - 두정 - 천안 - 봉명 - 쌍용 - 아산 - 배방 - 온양온천 - 신창 - 서동탄",
    2: "시청 - 을지로입구 - 을지로3가 - 을지로4가 - 동대문역사문화공원 - 신당 - 상왕십리 - 왕십리 - 한양대 - 뚝섬 - 성수 - 건대입구 - 구의 - 강변 - 잠실나루 - 잠실 - 신천 - 종합운동장 - 삼성 - 선릉 - 역삼 - 강남 - 교대 - 서초 - 방배 - 사당 - 낙성대 - 서울대입구 - 봉천 - 신림 - 신대방 - 구로디지털단지 - 대림 - 신도림 - 문래 - 영등포구청 - 당산 - 합정 - 홍대입구 - 신촌 - 이대 - 아현 - 충정로 - 시청",
    3: "대화 - 주엽 - 정발산 - 마두 - 백석 - 대곡 - 화정 - 원당 - 삼송 - 지축 - 구파발 - 연신내 - 불광 - 녹번 - 홍제 - 무악재 - 독립문 - 경복궁 - 안국 - 종로3가 - 을지로3가 - 충무로 - 동대입구 - 약수 - 금호 - 옥수 - 압구정 - 신사 - 잠원 - 고속터미널 - 교대 - 남부터미널 - 양재 - 매봉 - 도곡 - 대치 - 학여울 - 대청 - 일원 - 수서 - 가락시장 - 경찰병원 - 오금",
    4: "진접 - 오남 - 별내별가람 - 당고개 - 상계 - 노원 - 창동 - 쌍문 - 수유 - 미아 - 미아삼거리 - 길음 - 성신여대입구 - 한성대입구 - 혜화 - 동대문 - 동대문역사문화공원 - 충무로 - 명동 - 회현 - 서울역 - 숙대입구 - 삼각지 - 신용산 - 이촌 - 동작 - 이수 - 사당 - 남태령 - 선바위 - 경마공원 - 대공원 - 과천 - 정부과천청사 - 인덕원 - 평촌 - 범계 - 금정 - 산본 - 수리산 - 대야미 - 반월 - 상록수 - 한대앞 - 중앙 - 고잔 - 공단 - 안산 - 신길온천 - 정왕 - 오이도",
    5: "방화 - 개화산 - 김포공항 - 송정 - 마곡 - 발산 - 우장산 - 화곡 - 까치산 - 신정 - 목동 - 오목교 - 양평 - 영등포구청 - 영등포시장 - 신길 - 여의도 - 여의나루 - 마포 - 공덕 - 애오개 - 충정로 - 서대문 - 광화문 - 종로3가 - 을지로4가 - 동대문역사문화공원 - 청구 - 신금호 - 행당 - 왕십리 - 마장 - 답십리 - 장한평 - 군자 - 아차산 - 광나루 - 천호 - 강동 - 길동 - 굽은다리 - 명일 - 고덕 - 상일동 - 둔촌동 - 올림픽공원 - 방이 - 오금 - 개롱 - 거여 - 마천"
}

# 그래프 구성
graph = defaultdict(list)
transfer = defaultdict(list)

for line, stations in lines.items():
    station_list = [s.strip() for s in stations.split('-')]
    for i in range(len(station_list)):
        station = f"{station_list[i]}({line})"
        if i > 0:
            prev_station = f"{station_list[i-1]}({line})"
            graph[station].append((prev_station, 2))
            graph[prev_station].append((station, 2))
        transfer[station_list[i]].append(station)

for same_name_stations in transfer.values():
    for i in range(len(same_name_stations)):
        for j in range(i+1, len(same_name_stations)):
            graph[same_name_stations[i]].append((same_name_stations[j], 2))
            graph[same_name_stations[j]].append((same_name_stations[i], 2))

def dijkstra(start, end):
    heap = [(0, start, [start])]
    visited = set()
    
    while heap:
        cost, node, path = heapq.heappop(heap)
        if node == end:
            return cost, path
        
        if node in visited:
            continue
        visited.add(node)
        
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(heap, (cost + weight, neighbor, path + [neighbor]))
                
    return float('inf'), []

def find_path(start_name, end_name):
    results = []
    for start in transfer[start_name]:
        for end in transfer[end_name]:
            cost, path = dijkstra(start, end)
            results.append((cost, path))
    return min(results)

# 여기서 경로 상세 요약 출력
def print_route_summary(path, cost):
    route_info = []
    prev_line = None

    for station in path:
        name, line = station[:-3], station[-2]
        if not prev_line:
            route_info.append(f"{name}에서 {line}호선 탑승")
        elif prev_line != line:
            route_info.append(f"{name}에서 {line}호선으로 환승")
        prev_line = line

    print("이동 요약:")
    for info in route_info:
        print("-", info)
    print(f"총 소요 시간: {cost}분")

# 예제 실행
cost, path = find_path("동대문역사문화공원", "왕십리")
print_route_summary(path, cost)


# In[2]:


cost, path = find_path("길음", "왕십리")
print_route_summary(path, cost)


# In[ ]:




