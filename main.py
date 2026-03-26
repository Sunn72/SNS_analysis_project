import pandas as pd
from googleapiclient.discovery import build
import time

#1 초기 설정
api_key = "YOUR_YOUTUBE_API_KEY"
youtube = build('youtube', 'v3', developerKey=api_key)

#2 키워드 로드 함수
def load_keywords(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f'오류: {file_path} 파일이 없습니다.')
        return []

#3 특정 키워드로 영상 정보, 통계 가져오는 함수
def get_video_data(query, label, max_results=20):
    print(f"현재 '{query}' 키워드(Label: {label}) 수집 중...")
    #3.1 검색 API 호출(영상 ID, 제목 수집)
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=max_results,
        type='video',
        order='relevance',
        regionCode='KR'
    ).execute()

    video_items = search_response.get('items', [])
    results = []

    for item in video_items:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        published_at = item['snippet']['publishedAt']

        #3.2 통계 API 수집(조회수, 좋아요, 댓글 수 수집)
        stats_response = youtube.videos().list(
            part='statistics',
            id = video_id
        ).execute()

        if not stats_response['items']: continue
        stats = stats_response['items'][0]['statistics']

        #3.2.1 데이터 저장(딕셔너리)
        results.append({
            'search_keyword' : query,
            'label' : label,
            'title' : title,
            'video_id' : video_id,
            'view_count' : int(stats.get('viewCount', 0)),
            'like_count' : int(stats.get('likeCount', 0)),
            'comment_count' : int(stats.get('commentCount', 0)),
            'published_at' : published_at
        })

        #3.2.2 할당량 보호 및 서버 부하 방지
        time.sleep(0.05)
    
    return results

#4 메인 실행 프로세스
def main():
    #4.1 키워드 파일 불러오기
    bait_keywords = load_keywords('bait_keywords.txt')
    normal_keywords = load_keywords('normal_keywords.txt')

    if not bait_keywords and not normal_keywords:
        print('수집할 키워드가 없습니다. 프로그램을 종료합니다.')
        return
    
    all_collected_data = []

    #4.2 각 키워드별로 수집 반복
    for kw in bait_keywords:
        all_collected_data.extend(get_video_data(kw, label=1))

    for kw in normal_keywords:
        all_collected_data.extend(get_video_data(kw, label=0))

    #4.3 중복 제거 로직
    df = pd.DataFrame(all_collected_data)

    print(f"\n중복 제거 전 데이터 개수: {len(df)}개")
    
    df = df.drop_duplicates(subset=['video_id'], keep='first')
    
    print(f"중복 제거 후 최종 데이터 개수: {len(df)}개")

    #5 Pandas로 CSV 파일 저장
    #5.1 파일 저장(한글 깨짐 방지로 utf-8-sig 사용)
    filename = "youtube_analysis_data.csv"
    df.to_csv(filename, index=False, encoding='utf-8-sig')

    print('\n'+'='*30)
    print(f"수집완료. 총 {len(df)}개의 데이터가 '{filename}'에 저장되었습니다.")
    print('='*30)

if __name__ == "__main__":
    main()

