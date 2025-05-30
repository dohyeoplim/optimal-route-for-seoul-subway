from collections import defaultdict 

_RAW_LINES = {
    # 1호선 메인라인 (소요산-인천)
    1: """
소요산 - 동두천 - 보산 - 동두천중앙 - 지행 - 덕정 - 덕계 - 양주 - 녹양 - 가능 - 의정부 - 회룡 - 망월사 - 도봉산 - 도봉 - 방학 - 창동 - 녹천 - 월계 - 성북 - 석계 - 신이문 - 외대앞 - 회기 - 청량리 - 제기동 - 신설동 - 동묘앞 - 동대문 - 종로5가 - 종로3가 - 종각 - 시청 - 서울역 - 남영 - 용산 - 노량진 - 대방 - 신길 - 영등포 - 신도림 - 구로 - 구일 - 개봉 - 오류동 - 온수 - 역곡 - 소사 - 부천 - 중동 - 송내 - 부개 - 부평 - 백운 - 동암 - 간석 - 주안 - 도화 - 제물포 - 도원 - 동인천 - 인천
""",
    
    # 1호선 수원-신창 구간
    "1_suwon": """
구로 - 가산디지털단지 - 독산 - 금천구청 - 석수 - 관악 - 안양 - 명학 - 금정 - 군포 - 당정 - 의왕 - 성균관대 - 화서 - 수원 - 세류 - 병점 - 세마 - 오산대 - 오산 - 진위 - 송탄 - 서정리 - 지제 - 평택 - 성환 - 직산 - 두정 - 천안 - 봉명 - 쌍용 - 아산 - 배방 - 온양온천 - 신창
""",
    
    # 1호선 광명 분기선
    "1_gwangmyeong": """
금천구청 - 광명
""",
    
    # 1호선 서동탄 분기선
    "1_sdt": """
병점 - 서동탄
""",
    
    2: """
시청 - 을지로입구 - 을지로3가 - 을지로4가 - 동대문역사문화공원 - 신당 - 상왕십리 - 왕십리 - 한양대 - 뚝섬 - 성수 - 건대입구 - 구의 - 강변 - 잠실나루 - 잠실 - 신천 - 종합운동장 - 삼성 - 선릉 - 역삼 - 강남 - 교대 - 서초 - 방배 - 사당 - 낙성대 - 서울대입구 - 봉천 - 신림 - 신대방 - 구로디지털단지 - 대림 - 신도림 - 문래 - 영등포구청 - 당산 - 합정 - 홍대입구 - 신촌 - 이대 - 아현 - 충정로 - 시청
""",
    3: """
대화 - 주엽 - 정발산 - 마두 - 백석 - 대곡 - 화정 - 원당 - 삼송 - 지축 - 구파발 - 연신내 - 불광 - 녹번 - 홍제 - 무악재 - 독립문 - 경복궁 - 안국 - 종로3가 - 을지로3가 - 충무로 - 동대입구 - 약수 - 금호 - 옥수 - 압구정 - 신사 - 잠원 - 고속터미널 - 교대 - 남부터미널 - 양재 - 매봉 - 도곡 - 대치 - 학여울 - 대청 - 일원 - 수서 - 가락시장 - 경찰병원 - 오금
""",
 
    4: """
진접 - 오남 - 별내별가람 - 당고개 - 상계 - 노원 - 창동 - 쌍문 - 수유 - 미아 - 미아삼거리 - 길음 - 성신여대입구 - 한성대입구 - 혜화 - 동대문 - 동대문역사문화공원 - 충무로 - 명동 - 회현 - 서울역 - 숙대입구 - 삼각지 - 신용산 - 이촌 - 동작 - 이수 - 사당 - 남태령 - 선바위 - 경마공원 - 대공원 - 과천 - 정부과천청사 - 인덕원 - 평촌 - 범계 - 금정 - 산본 - 수리산 - 대야미 - 반월 - 상록수 - 한대앞 - 중앙 - 고잔 - 공단 - 안산 - 신길온천 - 정왕 - 오이도
""",
    
    # 5호선 메인라인 (방화-강동)
    5: """
방화 - 개화산 - 김포공항 - 송정 - 마곡 - 발산 - 우장산 - 화곡 - 까치산 - 신정 - 목동 - 오목교 - 양평 - 영등포구청 - 영등포시장 - 신길 - 여의도 - 여의나루 - 마포 - 공덕 - 애오개 - 충정로 - 서대문 - 광화문 - 종로3가 - 을지로4가 - 동대문역사문화공원 - 청구 - 신금호 - 행당 - 왕십리 - 마장 - 답십리 - 장한평 - 군자 - 아차산 - 광나루 - 천호 - 강동
""",
    
    # 5호선 상일동지선 (강동-상일동)
    "5_sangil": """
강동 - 길동 - 굽은다리 - 명일 - 고덕 - 상일동
""",
    
    # 5호선 마천지선 (강동-마천, 둔촌동 경유)
    "5_macheon": """
강동 - 둔촌동 - 올림픽공원 - 방이 - 오금 - 개롱 - 거여 - 마천
""",
}

# 분기점 정보 (어떤 역에서 어떤 분기선들이 만나는지)
BRANCH_CONNECTIONS = {
    "가산디지털단지": [1, "1_suwon", "1_gwangmyeong"],  # 1호선 메인, 수원방면, 광명방면
    "병점": ["1_suwon", "1_sdt"],  # 수원방면, 서동탄방면
    "강동": [5, "5_sangil", "5_macheon"],  # 5호선 메인, 상일동지선, 마천지선
}

def process_lines():
    """그래프 구축에 필요한 정보 생성성"""
    lines = {}
    station_lines_temp = defaultdict(list)
    
    for line_key, stations_str in _RAW_LINES.items():
        # 역 이름 추출 및 정리
        stations = [s.strip() for s in stations_str.split('-') if s.strip()]
        lines[line_key] = stations
        
        # 각 역이 어떤 노선에 속하는지 기록
        for station in stations:
            station_lines_temp[station].append(line_key)
    
    # 노선 번호 정렬
    station_lines = {station: sorted(line_list, key=lambda x: (str(x).split('_')[0], str(x))) 
                    for station, line_list in station_lines_temp.items()}
    
    # 환승역 찾기 (2개 이상의 노선이 지나는 역)
    transfer_map = {station: lines_list for station, lines_list in station_lines.items() 
                   if len(lines_list) > 1}#종로3가: [1, 3, 5]
    
    return lines, station_lines, transfer_map

# 데이터 처리
lines, station_lines, transfer_map = process_lines()




# # 결과 출력 (테스트용)
# if __name__ == "__main__":
#     print("=== 노선별 역 목록 ===")
#     for line_key, stations in lines.items():
#         print(f"{line_key}: {len(stations)}개 역")
#         print(f"  시작: {stations[0]} -> 끝: {stations[-1]}")
    
#     print("\n=== 환승역 예시 (처음 5개) ===")
#     for i, (station, lines_list) in enumerate(transfer_map.items()):
#         if i >= 5:
#             break
#         print(f"{station}: {lines_list}")
