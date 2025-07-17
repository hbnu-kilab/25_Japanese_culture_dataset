import pandas as pd
import json

# TSV 파일 경로
tsv_path = '/Users/sehyun/Downloads/aca063e07d82c46999e15c24874ca431.tsv'

# TSV 파일 읽기
df = pd.read_csv(tsv_path, sep='\t', dtype=str).fillna('')

# 처리 함수 정의
def process_row(row):
    return {
        "JPS_ID": row["JPS_ID"],
        "文化財指定": row["文化財指定"] if row["文化財指定"].strip() else "미등록",
        "分類": row["分類"],
        "作品名": row["作品名"],
        "員数": row["員数"],
        "作者": row["作者"] if row["作者"].strip() else "미상",
        "制作地": row["制作地"] if row["制作地"].strip() else "미상",
        "時代世紀": row["時代世紀"] if row["時代世紀"].strip() else "미상",
        "法量": row["法量"] if row["法量"].strip() else "미측정",
        "所蔵者": row["所蔵者"],
        "解説": row["解説"] if row["解説"].strip() else "설명필요",
        "이미지 폴더 경로": "",  # 비워두기
        "コンテンツの公開状況": row["コンテンツの公開状況"],
        "コンテンツの権利区分": row["コンテンツの権利区分"],
        "URL": row["URL"]
    }

# 데이터 처리
json_data = [process_row(row) for _, row in df.iterrows()]

# 결과 저장 (선택)
with open('converted_data.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=2)

# 출력 (옵션)
print(json.dumps(json_data, ensure_ascii=False, indent=2))