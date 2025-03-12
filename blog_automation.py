import openai
import requests
import config  # ✅ 환경 변수 가져오기

# ✅ OpenAI API 설정
openai.api_key = config.OPENAI_API_KEY

### ✅ 1. SEO 키워드 자동 검색
def get_trending_keywords():
    url = "https://trends.google.com/trends/api/dailytrends?hl=ko"
    response = requests.get(url)
    
    if response.status_code == 200:
        trends = response.json()
        topics = [t['title'] for t in trends['default']['trendingSearchesDays'][0]['trendingSearches']]
        return topics[:5]  # 상위 5개 키워드 선택
    else:
        return ["AI 부업", "블로그 자동화", "온라인 부업", "부업 추천", "IT 트렌드"]

### ✅ 2. AI 블로그 글 생성 (SEO 키워드 반영)
def generate_blog_post(topic, keywords):
    prompt = f"""
    '{topic}'에 대한 SEO 최적화 블로그 글을 작성해줘.
    - 제목과 소제목 포함
    - 본문은 2000자 내외 작성
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
