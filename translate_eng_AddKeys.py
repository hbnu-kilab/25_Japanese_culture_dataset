import json

key_translation = {
    "文化財指定": "cultural_property_status",
    "分類": "category",
    "作品名": "title",
    "員数": "quantity",
    "作者": "author",
    "制作地": "production_place",
    "時代世紀": "era_century",
    "法量": "dimension",
    "所蔵者": "owner",
    "解説": "description",
    "이미지 폴더 경로": "image_folder_path",
    "コンテンツの公開状況": "content_availability",
    "コンテンツの権利区分": "content_license",
    "URL": "url"
}

def transform_data(data_list):
    transformed = []
    for item in data_list:
        new_item = {
            "id": int(item.get("JPS_ID", 0)),
            "metadata": {},
            "definition": "",
            "history": "",
            "purpose": "",
            "exterior": "",
            "distinctive_feature": "",
            "korean_artifact": "",
            "chinese_artifact": ""
        }

        for old_key, new_key in key_translation.items():
            new_item["metadata"][new_key] = item.get(old_key, "")

        transformed.append(new_item)
    return transformed

def convert_json(input_file: str, output_file: str):
    with open(input_file, 'r', encoding='utf-8') as f:
        original_data = json.load(f)

    converted_data = transform_data(original_data)

    with open('/Users/sehyun/Sehyun/KILAB/일본문화재 크롤링', 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, ensure_ascii=False, indent=2)

    print(f"✅ 변환 완료! 결과가 '{output_file}'에 저장되었습니다.")

if __name__ == "__main__":
    input_filename = "original_data.json"
    output_filename = "converted_data.json"
    convert_json(input_filename, output_filename)