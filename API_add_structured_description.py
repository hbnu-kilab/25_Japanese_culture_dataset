import os
import json
import base64
import re
import openai
import time

# 🔑 OpenAI API 키 설정
openai.api_key_path = ".apikey"

# ⚙️ 설정
#처음 시작할때는 아무것도 없는 파일로 설정 
#json_file_path = "filtered_period_data_updated_ALL_8158개_export_no_description.json"
json_file_path = "structured_description_output.json"
image_dir = "/home/parksh/images"
output_file_path = "/home/parksh/japan/structured_description_output.json"
model = "gpt-4o-mini"
max_requests = 50


# 📤 이미지 base64 인코딩
def encode_image(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


# 💬 메시지 생성 함수
def create_messages(item, image_path):
    return [
        {
            "role": "system",
            "content": "다음 유물 사진과 메타데이터를 참고해서 structured_description을 작성해줘. 너무 짧게 쓰지 말고, 구체적인 정보를 담아서 3~5문장 정도로 작성해줘. 불확실한 내용은 추측하지 마.",
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"유물의 메타데이터는 다음과 같아:\n\n{json.dumps(item, ensure_ascii=False)}"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encode_image(image_path)}",
                        "detail": "low"
                    }
                }
            ]
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
    all_image_files = os.listdir(image_dir)

    for item in data:
        # ✅ 이미 처리된 항목은 스킵
        if "structured_description" in item and item["structured_description"]:
            continue

        if count >= max_requests:
            break

        jps_id = item.get("jps_id")
        if not jps_id:
            continue

        matching_images = [
            os.path.join(image_dir, fname)
            for fname in all_image_files
            if re.search(rf"-{jps_id}\.jpg$", fname)
        ]

        if not matching_images:
            continue

        image_path = matching_images[0]
        messages = create_messages(item, image_path)
        result = call_openai_with_retry(messages)

        if result:
            item["structured_description"] = result
            print(f"✅ {jps_id} 완료:\n{result}\n")
            count += 1
        else:
            print(f"❌ {jps_id} 처리 실패\n")
            failed_ids.append(jps_id)

    return data, failed_ids


# 🚀 실행
with open(json_file_path, "r", encoding="utf-8") as f:
    json_data = json.load(f)

processed_data, failed_ids = process_json_data(json_data, image_dir, max_requests=max_requests)

# 💾 저장
with open(output_file_path, "w", encoding="utf-8") as f:
    json.dump(processed_data, f, ensure_ascii=False, indent=2)

print(f"\n🎉 완료: structured_description이 추가된 JSON이 저장되었습니다: {output_file_path}")

if failed_ids:
    print(f"\n⚠️ 총 {len(failed_ids)}건 실패")
    print("실패한 jps_id 목록:")
    print(", ".join(map(str, failed_ids)))
else:
    print("\n✅ 모든 요청이 성공적으로 완료되었습니다.")