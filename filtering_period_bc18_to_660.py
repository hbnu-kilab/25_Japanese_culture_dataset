import json
import re

# 파일 경로 설정
input_path = "/Users/sehyun/Sehyun/KILAB/일본문화재 크롤링/일본문화재_영문확장.json"
output_path = "/Users/sehyun/Sehyun/KILAB/일본문화재 크롤링/filtered_bc18_to_660.json"

# 타겟 연도 범위: 기원전 18년 ~ 서기 660년
start_year = -18
end_year = 660

# 연도 포함 여부 판단 함수
def contains_year_in_range(text):
    # "前300" 같은 표현도 처리
    year_matches = re.findall(r"(前)?(\d{1,4})", text)
    for mae, y in year_matches:
        try:
            year = -int(y) if mae else int(y)
            if start_year <= year <= end_year:
                return True
        except ValueError:
            continue
    return False

# 필터 조건
def is_target_entry(entry):
    period = entry.get("period_century", "")
    return contains_year_in_range(period)

# JSON 읽기
with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 필터링
filtered_data = [entry for entry in data if is_target_entry(entry)]

# 저장
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

print(f"✅ 추출된 항목 수: {len(filtered_data)}개")
print(f"📁 저장 위치: {output_path}")
