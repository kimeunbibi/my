from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pyperclip  # 클립보드 복사 기능
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import config  # ✅ 환경 변수 가져오기
from blog_automation import generate_blog_post, get_trending_keywords  # AI 글 자동 생성


###
# C:\my
# python naver_blog_auto.py

# ✅ Headless Mode 설정 추가
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 🚀 창 없이 실행
options.add_argument("--no-sandbox")  # 일부 환경에서 필요한 옵션
options.add_argument("--disable-dev-shm-usage")  # 메모리 부족 방지
options.add_argument("--window-size=1920,1080")  # 가상 화면 크기 설정 (생략 가능)
options.add_argument("--disable-gpu")  # GPU 가속 사용 안 함 (일부 환경에서 필요)
options.add_argument("--start-maximized")  # 화면을 최대화된 상태에서 실행 (옵션)

# ✅ Chrome WebDriver 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# ✅ 네이버 블로그 글쓰기 페이지 이동
driver.get("https://blog.naver.com/EditPost.naver")

print("✅ Headless Mode에서 실행 중...")

# ✅ 페이지 제목 출력 (테스트)
print("📌 현재 페이지 제목:", driver.title)

###
def write_title(driver, text):
    try:
        print("✅ 제목 입력 시도...")

        # ✅ iframe 전환 (네이버 블로그 글쓰기 페이지의 본문 편집기)
        driver.switch_to.default_content()
        editor_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(editor_iframe)
        print("✅ iframe 전환 완료")

        # ✅ 제목 입력란 찾기 (JavaScript 사용)
        title_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.se-title-text p.se-text-paragraph span"))
        )
        print("✅ 제목 입력란 찾음")

        # ✅ 방법 1: JavaScript로 제목 변경 (send_keys 대신)
        driver.execute_script("arguments[0].innerText = arguments[1];", title_box, text)
        print(f"✅ 제목 입력 완료 (JavaScript 사용): {text}")

        time.sleep(2)  # 입력 안정화 대기

    except Exception as e:
        print("⚠ 제목 입력 중 오류 발생:", e)





def write_content(driver, text):
    try:
        print("✅ 본문 입력 시도...")

        # ✅ 최상위 프레임으로 이동 후 iframe 찾기
        driver.switch_to.default_content()
        editor_iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(editor_iframe)  # 🔥 본문 편집기 iframe 내부로 이동
        print("✅ 본문 입력 iframe 전환 완료")

        # ✅ 본문 입력란 찾기 (제목과 확실히 구분)
        content_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.se-component.se-text p.se-text-paragraph span"))
        )
        print("✅ 본문 입력란 찾음 (제목과 다름)")

        # ✅ 기존 내용 삭제 후 본문 입력
        driver.execute_script("arguments[0].innerText = arguments[1];", content_box, text)
        print(f"✅ 본문 입력 완료 (JavaScript 사용): {text}")

        time.sleep(2)  # 입력 안정화 대기

    except Exception as e:
        print("⚠ 본문 입력 중 오류 발생:", e)



def complete_writing(driver):
    try:
        print("✅ 게시글 발행 시도...")

        # ✅ 최상위 프레임으로 이동
        driver.switch_to.default_content()

        # ✅ iframe 확인 및 전환 (iframe 내부라면 전환)
        try:
            editor_iframe = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            driver.switch_to.frame(editor_iframe)
            print("✅ iframe 전환 완료")
        except:
            print("⚠ iframe 전환 불필요")

        # ✅ 첫 번째 발행 버튼 클릭
        try:
            first_publish_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "publish_btn")]'))
            )
        except:
            first_publish_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "발행")]'))
            )
        print("✅ 첫 번째 발행 버튼 찾음")

        # ✅ JavaScript로 강제 클릭 (첫 번째 버튼)
        driver.execute_script("arguments[0].click();", first_publish_button)
        print("✅ 첫 번째 발행 버튼 클릭 완료")

        time.sleep(3)  # UI 업데이트 대기

        # ✅ 두 번째 최종 발행 버튼 클릭 (새로운 네이버 UI에서 추가됨)
        try:
            second_publish_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="seOnePublishBtn"]'))
            )
            driver.execute_script("arguments[0].click();", second_publish_button)
            print("✅ 두 번째 최종 발행 버튼 클릭 완료")
        except:
            print("⚠ 두 번째 발행 버튼 없음. 바로 게시됨.")

        time.sleep(5)  # 네이버 서버에서 처리 대기

        print("✅ 게시글 발행 완료!")

    except Exception as e:
        print("⚠ 게시글 발행 중 오류 발생:", e)

###

# ✅ 네이버 로그인 정보
NAVER_ID = config.NAVER_ID
NAVER_PW = config.NAVER_PW

# ✅ 블로그 글 자동 생성 (AI 활용)
topic = "AI를 활용한 부업"
keywords = get_trending_keywords()  # SEO 키워드 가져오기
BLOG_TITLE = topic  # 제목 = 주제
BLOG_CONTENT = generate_blog_post(topic, keywords)  # AI 생성 글

# ✅ Selenium 웹드라이버 설정
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # 창 최대화
driver = webdriver.Chrome(service=service, options=options)

# ✅ 네이버 로그인 페이지 접속
driver.get("https://nid.naver.com/nidlogin.login")
time.sleep(2)

# ✅ 아이디 입력 (클립보드 복사 후 붙여넣기)
pyperclip.copy(NAVER_ID)  # 아이디 복사
id_box = driver.find_element(By.ID, "id")  # 아이디 입력창 찾기
id_box.click()  # 클릭하여 활성화
id_box.send_keys(Keys.CONTROL, 'v')  # Ctrl + V 붙여넣기
time.sleep(1)

# ✅ 비밀번호 입력 (클립보드 복사 후 붙여넣기)
pyperclip.copy(NAVER_PW)  # 비밀번호 복사
pw_box = driver.find_element(By.ID, "pw")  # 비밀번호 입력창 찾기
pw_box.click()
pw_box.send_keys(Keys.CONTROL, 'v')  # Ctrl + V 붙여넣기
time.sleep(1)

# ✅ 로그인 버튼 클릭
login_btn = driver.find_element(By.ID, "log.login")
login_btn.click()
time.sleep(5)  # 로그인 처리 시간 대기

# ✅ 네이버 블로그 글쓰기 페이지 이동
driver.get("https://blog.naver.com/" + NAVER_ID + "?Redirect=Write&")
time.sleep(5)

write_title(driver, "title")

write_content(driver, "테스트 본문입니다.")


# # ✅ 본문 입력 필드 찾기 & 입력
# content_box = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
# content_box.send_keys(BLOG_CONTENT)

# ✅ 발행 버튼 클릭
complete_writing(driver)

print("✅ 블로그 자동 업로드 완료!")
time.sleep(5)
# driver.quit()
