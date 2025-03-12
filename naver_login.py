from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pyperclip  # 클립보드 복사 기능

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import config  # ✅ 환경 변수 가져오기 (네이버 아이디, 비밀번호 보관)

# ✅ 네이버 로그인 정보 (config.py에서 불러오기)
NAVER_ID = config.NAVER_ID
NAVER_PW = config.NAVER_PW

# ✅ Selenium 웹드라이버 설정
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # 창 최대화
driver = webdriver.Chrome(service=service, options=options)

# ✅ 네이버 로그인 페이지 접속
driver.get("https://nid.naver.com/nidlogin.login")
time.sleep(2)

# ✅ 아이디 입력 (클립보드 복사 후 붙여넣기)
pyperclip.copy(NAVER_ID)  # 아이디 클립보드에 복사
id_box = driver.find_element(By.ID, "id")  # 아이디 입력창 찾기
id_box.click()  # 클릭하여 활성화
id_box.send_keys(Keys.CONTROL, 'v')  # Ctrl + V 로 붙여넣기
time.sleep(1)  # 입력 대기

# ✅ 비밀번호 입력 (클립보드 복사 후 붙여넣기)
pyperclip.copy(NAVER_PW)  # 비밀번호 클립보드에 복사
pw_box = driver.find_element(By.ID, "pw")  # 비밀번호 입력창 찾기
pw_box.click()
pw_box.send_keys(Keys.CONTROL, 'v')  # Ctrl + V 로 붙여넣기
time.sleep(1)

# ✅ 로그인 버튼 클릭
login_btn = driver.find_element(By.ID, "log.login")
login_btn.click()
time.sleep(5)  # 로그인 처리 시간 대기

# ✅ 로그인 성공 확인 (네이버 메인으로 이동)
if "nid.naver.com" not in driver.current_url:
    print("✅ 네이버 로그인 성공!")
else:
    print("⚠ 로그인 실패: 추가 인증이 필요할 수 있음.")

# ✅ 브라우저 종료 (테스트 후 필요 없으면 유지 가능)
driver.quit()
