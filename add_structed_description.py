import json
from collections import OrderedDict

# 원본 JSON 파일 경로
input_path = '/Users/sehyun/Sehyun/KILAB/일본문화재 크롤링/filtered_period_data.json'
output_path = '/Users/sehyun/Sehyun/KILAB/일본문화재 크롤링/filtered_period_data_with_structured.json'

# JSON 파일 읽기
with open(input_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 각 객체에 structured_description 추가
new_data = []
for item in data:
    new_item = OrderedDict()
    for key, value in item.items():
        new_item[key] = value
        if key == "description":
            # description 뒤에 structured_description 삽입
            new_item["structured_description"] = ""
    new_data.append(new_item)

# 결과 저장
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print("✅ structured_description 키가 추가된 파일이 저장되었습니다.")