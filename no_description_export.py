import json

# JSON 파일 경로
file_path = '/Users/sehyun/Sehyun/KILAB/일본문화재 크롤링/filtered_period_data_with_structured_여기에설명채우기.json'

# 파일 읽기
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# "설명 필요" 또는 "설명필요"가 아닌 항목만 필터링
excluded_phrases = {"설명 필요", "설명필요"}
filtered_data = [item for item in data if item.get('description', '').strip() not in excluded_phrases]

# 결과 출력
print(f'"설명 필요" 또는 "설명필요"가 아닌 항목 수: {len(filtered_data)}개')

# 새 JSON 파일로 저장
output_path = '/Users/sehyun/Sehyun/KILAB/일본문화재 크롤링/설명완료_항목_추출.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=2)

print(f'필터링된 항목들을 "{output_path}" 파일로 저장했습니다.')