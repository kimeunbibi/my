import openai
import requests
import config  # ✅ config.py에서 설정값 불러오기

# 📌 OpenAI API 키 설정
openai.api_key = config.OPENAI_API_KEY

# 📌 네이버 블로그 API & Unsplash API 정보
NAVER_BLOG_API_URL = config.NAVER_BLOG_API_URL
NAVER_ACCESS_TOKEN = config.NAVER_ACCESS_TOKEN
UNSPLASH_ACCESS_KEY = config.UNSPLASH_ACCESS_KEY

### ✅ SEO 키워드 자동 검색
def get_trending_keywords():
    url = "https://trends.google.com/trends/api/dailytrends?hl=ko"
    response = requests.get(url)
    
    if response.status_code == 200:
        trends = response.json()
        topics = [t['title'] for t in trends['default']['trendingSearchesDays'][0]['trendingSearches']]
        return topics[:5]  # 상위 5개 키워드 선택
    else:
        return ["AI 부업", "블로그 자동화", "온라인 부업", "부업 추천", "IT 트렌드"]

### ✅ 블로그 글 생성 (SEO 키워드 반영)
def generate_blog_post(topic, keywords):
    prompt = f"""
    '{topic}'에 대한 SEO 최적화 블로그 글을 작성해줘.
    - 제목과 소제목 포함
    - 본문은 1000자 이상 작성
    - 자연스럽고 인간적인 문체로 작성 (블로그 스타일)
    - 최신 트렌드를 반영
    - 검색 최적화(SEO) 키워드 포함: {', '.join(keywords)}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates SEO-optimized blog posts."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response["choices"][0]["message"]["content"]

### ✅ 무료 이미지 추가 (Unsplash API)
def get_unsplash_image(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url).json()
    return response['urls']['regular']

### ✅ 블로그 자동 업로드 (네이버 API)
def post_to_naver(title, content, image_url):
    content_with_image = f"<img src='{image_url}'/><br>{content}"  # 본문에 이미지 삽입
    headers = {"Authorization": f"Bearer {NAVER_ACCESS_TOKEN}"}
    data = {"title": title, "contents": content_with_image}
    
    response = requests.post(NAVER_BLOG_API_URL, headers=headers, data=data)
    return response.json()

### 🚀 최종 실행 코드 (자동화)
if __name__ == "__main__":
    topic = "AI를 활용한 부업"
    keywords = get_trending_keywords()
    blog_content = generate_blog_post(topic, keywords)
    image_url = get_unsplash_image(topic)
    
    print("✅ 생성된 블로그 글:\n", blog_content)
    print("✅ 추가된 이미지:", image_url)

    # 블로그 자동 업로드 실행
    result = post_to_naver(topic, blog_content, image_url)
    print("✅ 블로그 업로드 결과:", result)
