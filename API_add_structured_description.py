import os
import json
import base64
import re
import openai
import time

# 🔑 OpenAI API 키 설정
openai.api_key_path = ".apikey"

# ⚙️ 설정
#두번째부터는 파일경로 structured_description_output.json 이걸로, 덮어쓰기 위함 
json_file_path = "filtered_period_data_updated_ALL_8158개_export_no_description.json"
image_dir = "/home/parksh/images"
output_file_path = "/home/parksh/japan/structured_description_output.json"
model = "gpt-4o-mini"
max_requests = 50

# 📁 로그 파일
missing_images_log = "missing_images.txt"
failed_generation_log = "failed_generation.txt"

# 🔄 로그 초기화
for log_file in [missing_images_log, failed_generation_log]:
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("")

# 📤 이미지 base64 인코딩
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# 📜 구조화 프롬프트 생성 함수
def generate_prompt_text(entry):
    return f"""
다음은 일본 문화재 정보입니다. 이 정보를 바탕으로 아래의 다섯 항목에 따라 structured_description을 작성해주세요.

- 정의: 유물이 무엇인지 정의
- 역사적 설명: 유물의 역사적 배경, 관련 인물·사건 등
- 용도: 유물의 제작 목적 또는 사용 용도
- 외관 특징: 재료, 형식, 외형적 표현 방식
- 고유 특징: 유물의 특수성, 희소성, 명문 등

출력 형식은 아래와 같이 문장 1~5로 구분하여 주세요:

---
문장 1: 정의)  
문장 2: 역사적 설명)  
문장 3: 용도)  
문장 4: 외관 특징)  
문장 5: 고유 특징)  
---

아래는 유물 정보입니다:

제목: {entry.get('title', '')}  
분류: {entry.get('category', '')}  
수량: {entry.get('quantity', '')}  
저자: {entry.get('author', '')}  
제작 장소: {entry.get('production_place', '')}  
시대: {entry.get('period_century', '')}  
소장처: {entry.get('owner', '')}  
설명: {entry.get('description', '') if entry.get('description', '') != '설명필요' else '없음'}
""".strip()

# 💬 메시지 생성 함수 (이미지 optional)
def create_messages(item, image_path=None):
    prompt_text = generate_prompt_text(item)
    content = [{"type": "text", "text": prompt_text}]
    if image_path:
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{encode_image(image_path)}",
                "detail": "low"
            }
        })
    return [
        {
            "role": "system",
            "content": "당신은 이미지와 유물 정보를 바탕으로 일본 문화재에 대한 구조화된 설명을 한국어로 작성하는 전문가입니다. 출력은 반드시 한국어로 해주세요."
        },
        {
            "role": "user",
            "content": content
        }
    ]

# 🔁 요청 재시도 함수
def call_openai_with_retry(messages, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=0.2,
            )
            return response.choices[0].message.content.strip()
        except openai.error.RateLimitError as e:
            print(f"⏳ Rate limit... {e}. {delay}s 후 재시도")
            time.sleep(delay)
        except Exception as e:
            print(f"❌ 요청 실패: {e}")
            return None
    return None

# 🧠 본 작업 로직
def process_json_data(data, image_dir, max_requests=50):
    count = 0
    failed_ids = []
    missing_image_ids = []
    all_image_files = os.listdir(image_dir)

    for item in data:
        desc = item.get("structured_description")
        if desc is not None and desc.strip() != "":
            continue

        if count >= max_requests:
            break

        jps_id = item.get("jps_id")
        if not jps_id:
            continue

        matching_images = [
            os.path.join(image_dir, fname)
            for fname in all_image_files
            if re.search(rf"-{jps_id}\.(jpg|jpeg|png)$", fname, re.IGNORECASE)
        ]

        image_path = matching_images[0] if matching_images else None
        if not image_path:
            missing_image_ids.append(jps_id)
            print(f"⚠️ 이미지 없음: {jps_id} → 메타데이터만으로 생성 시도")
            with open(missing_images_log, "a", encoding="utf-8") as f:
                f.write(f"{jps_id}\n")

        messages = create_messages(item, image_path)
        result = call_openai_with_retry(messages)

        if result:
            item["structured_description"] = result
            print(f"✅ {jps_id} 완료:\n{result}\n")
            count += 1
        else:
            print(f"❌ {jps_id} 처리 실패\n")
            failed_ids.append(jps_id)
            with open(failed_generation_log, "a", encoding="utf-8") as f:
                f.write(f"{jps_id}\n")

    return data, failed_ids, missing_image_ids

# 🚀 실행
if __name__ == "__main__":
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        print(f"📂 파일 로드 완료: {json_file_path}")
    else:
        raise FileNotFoundError(f"❌ {json_file_path} 파일이 존재하지 않습니다. 경로를 확인해주세요.")

    processed_data, failed_ids, missing_image_ids = process_json_data(json_data, image_dir, max_requests=max_requests)

    # 💾 결과 저장
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 완료: structured_description이 추가된 JSON이 저장되었습니다: {output_file_path}")

    if failed_ids:
        print(f"\n⚠️ 총 {len(failed_ids)}건 실패 (→ {failed_generation_log}에 저장됨)")
    else:
        print("\n✅ 모든 요청이 성공적으로 완료되었습니다.")

    if missing_image_ids:
        print(f"\n🖼️ 이미지 없는 항목 {len(missing_image_ids)}건 (→ {missing_images_log}에 저장됨)")
    else:
        print("\n📸 모든 항목에 이미지가 존재합니다.")