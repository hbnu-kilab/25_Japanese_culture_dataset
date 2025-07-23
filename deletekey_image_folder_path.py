import json

# JSON 파일 경로 설정
file_path = '/Users/sehyun/Sehyun/KILAB/일본문화재 크롤링/filtered_period_data_updated_ALL_8158개_export_no_description.json'  # 여기에 원본 JSON 파일 경로 입력

# JSON 파일 읽기
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 각 항목에서 "image_folder_path" 키 제거
for item in data:
    item.pop('image_folder_path', None)

# 원본 파일에 덮어쓰기
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ 원본 파일에서 'image_folder_path' 필드가 제거되었습니다.")