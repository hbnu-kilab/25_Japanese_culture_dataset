import json
import re

# 파일 경로 설정
input_path = "/Users/sehyun/Sehyun/KILAB/일본문화재 크롤링/일본문화재_영문확장.json"
output_path = "/Users/sehyun/Sehyun/KILAB/일본문화재 크롤링/filtered_period_data_updated.json"

# 타겟 연도 범위
target_year_ranges = [
    (-300, 300),     # 야요이 시대
    (250, 538),      # 고훈 시대
    (593, 710),      # 아스카 시대
    (710, 794),      # 나라 시대
    (794, 894),      # 헤이안 시대
    (1185, 1573),    # 가마쿠라~무로마치 시대
    (1368, 1644),    # 명-조선-일본 무역
    (1573, 1600),    # 아즈치모모야마 시대
    (1644, 1868),    # 에도 시대
]

# 타겟 시대 이름
target_eras = [
    "弥生時代", "古墳時代", "飛鳥時代", "奈良時代", "平安時代",
    "鎌倉時代", "南北朝時代", "室町時代", "安土桃山時代", "江戸時代"
]

# 연도 포함 여부 판단 함수
def contains_year_in_range(text):
    # 前○○表기 포함: 前300 → -300으로 처리
    year_matches = re.findall(r"(前)?(\d{1,4})", text)
    for mae, y in year_matches:
        try:
            year = -int(y) if mae else int(y)
            for start, end in target_year_ranges:
                if start <= year <= end:
                    return True
        except ValueError:
            continue
    return False

# 필터 조건
def is_target_entry(entry):
    period = entry.get("period_century", "")
    # 1. 시대명이 포함된 경우
    for era in target_eras:
        if era in period:
            return True
    # 2. 연도 범위 포함 여부
    if contains_year_in_range(period):
        return True
    return False

# JSON 파일 읽기
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 필터링 수행
filtered_data = [entry for entry in data if is_target_entry(entry)]

# 결과 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

print(f"✅ 필터링된 항목 수: {len(filtered_data)}개")
print(f"📁 저장 위치: {output_path}")
