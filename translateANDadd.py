import json
import os
from tqdm import tqdm

# 파일 경로
BASE_DIR = "/Users/sehyun/Sehyun/KILAB/일본문화재 크롤링"
INPUT_FILENAME = "converted_data.json"  # 실제 파일명으로 수정
OUTPUT_FILENAME = "일본문화재_영문확장.json"

INPUT_FILE = os.path.join(BASE_DIR, INPUT_FILENAME)
OUTPUT_FILE = os.path.join(BASE_DIR, OUTPUT_FILENAME)

# 키 매핑
field_map = {
    "JPS_ID": "jps_id",
    "文化財指定": "cultural_property_status",
    "分類": "category",
    "作品名": "title",
    "員数": "quantity",
    "作者": "author",
    "制作地": "production_place",
    "時代世紀": "period_century",
    "法量": "dimensions",
    "所蔵者": "owner",
    "解説": "description",
    "이미지 폴더 경로": "image_folder_path",
    "コンテンツの公開状況": "content_availability",
    "コンテンツの権利区分": "content_license",
    "URL": "url"
}

# 새로 추가할 키들
new_fields = [
    "definition",
    "history",
    "purpose",
    "exterior",
    "distinctive_feature",
    "korean_artifact",
    "chinese_artifact"
]

def convert_and_extend(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"❌ 입력 파일이 존재하지 않습니다: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    translated_data = []

    for item in tqdm(data, desc="Processing items"):
        translated_item = {}

        # 기존 키 변환
        for key, value in item.items():
            new_key = field_map.get(key, key)
            translated_item[new_key] = value

        # 새 키 추가 (빈 값으로)
        for key in new_fields:
            translated_item[key] = ""

        translated_data.append(translated_item)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    convert_and_extend(INPUT_FILE, OUTPUT_FILE)