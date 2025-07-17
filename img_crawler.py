import os
import json
import time
import zipfile
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# [1] 크롬 드라이버 설정 (macOS용)
options = Options()
options.add_argument('--headless')  # 창 띄우지 않음
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# [2] JSON 파일 불러오기
with open('test_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# [3] 이미지 저장 폴더 (공통)
main_image_folder = "images"
os.makedirs(main_image_folder, exist_ok=True)

# [4] 작업 루프
for item in data:
    url = item['URL']
    jps_id = item['JPS_ID']
    print(f"\n[JPS_ID: {jps_id}] 페이지 접속 중...")

    try:
        driver.get(url)
        time.sleep(2)  # 로딩 대기

        # "作品画像一式" 링크 찾기
        link = driver.find_element(By.XPATH, '//a[p[text()="作品画像一式"]]')
        zip_url = link.get_attribute('href')
        
        if zip_url and zip_url.endswith('.zip'):
            zip_path = os.path.join(main_image_folder, f"{jps_id}.zip")

            # ZIP 다운로드
            print(f"[{jps_id}] ZIP 다운로드 중: {zip_url}")
            response = requests.get(zip_url)
            with open(zip_path, 'wb') as f:
                f.write(response.content)

            # ZIP 압축 해제 (임시 폴더 사용)
            temp_extract_path = os.path.join(main_image_folder, f"temp_{jps_id}")
            os.makedirs(temp_extract_path, exist_ok=True)
            print(f"[{jps_id}] ZIP 압축 해제 중...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_extract_path)

            # 이미지 이동 및 이름 변경 (기존 이름 + -JPS_ID)
            for filename in os.listdir(temp_extract_path):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                    name, ext = os.path.splitext(filename)
                    new_filename = f"{name}-{jps_id}{ext}"
                    src_path = os.path.join(temp_extract_path, filename)
                    dst_path = os.path.join(main_image_folder, new_filename)
                    os.rename(src_path, dst_path)
                elif filename.endswith('.txt'):
                    os.remove(os.path.join(temp_extract_path, filename))

            # 정리
            os.remove(zip_path)
            os.rmdir(temp_extract_path)

            # JSON 업데이트
            item['이미지 폴더 경로'] = main_image_folder
            print(f"[{jps_id}] 완료! 이미지 저장: {main_image_folder}")

        else:
            print(f"[{jps_id}] ZIP 링크를 찾을 수 없음 또는 형식 이상")

    except Exception as e:
        print(f"[{jps_id}] 오류 발생: {e}")

# [5] JSON 업데이트 저장
with open('updated_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ 모든 작업 완료!")
driver.quit()
