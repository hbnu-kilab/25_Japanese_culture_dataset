import json
import os
from tqdm import tqdm

# 🔁 원본 파일 경로 및 저장 경로 설정
BASE_DIR = "/Users/sehyun/Sehyun/KILAB/일본문화재 크롤링"
INPUT_FILENAME = "converted_data.json"
OUTPUT_FILENAME = "japan_cultural_data_converted.json"

INPUT_FILE = os.path.join(BASE_DIR, INPUT_FILENAME)
OUTPUT_FILE = os.path.join(BASE_DIR, OUTPUT_FILENAME)

# 🔑 키 영어로 매핑
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

def convert_keys_to_english(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    translated_data = []

    for item in tqdm(data, desc="Converting keys"):
        translated_item = {}
        for key, value in item.items():
            new_key = field_map.get(key, key)  # 매핑 없으면 원래 키 유지
            translated_item[new_key] = value
        translated_data.append(translated_item)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(translated_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    convert_keys_to_english(INPUT_FILE, OUTPUT_FILE)