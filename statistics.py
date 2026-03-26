import pandas as pd

def run_statistics():
    #1 데이터 불러오기
    try:
        df = pd.read_csv('youtube_analysis_data.csv')
        print(f'총 수집 데이터 개수: {len(df)}')
    except FileNotFoundError:
        print("'youtube_analysis_data.csv' 파일을 찾을 수 없습니다.")
        return
    
    #2 그룹별 데이터 분리
    # label 1: Bait, label 2: Normal
    clickbait = df[df['label']==1]
    normal = df[df['label']==0]

    #3 요약 통계 계산 함수
    def get_summary(data, name):
        return {
            "분류": name,
            "영상 개수": len(data),
            "평균 조회수": int(data['view_count'].mean()),
            "중앙값 조회수": int(data['view_count'].median()),
            "최대 조회수": int(data['view_count'].max()),
            "평균 좋아요": int(data['like_count'].mean()),
            "평균 댓글": int(data['commit_count'].mean())
        }
    
    #4 결과 출력
    results = [get_summary(clickbait, "Bait (1)"), get_summary(normal, "Normal (0))")]
    summary_df = pd.DataFrame(results)

    print("=== 그룹별 데이터 통계 ===")
    print(summary_df.to_string(index=False))
    print('='*35)

    #5 가설 검증 결과 (간이 분석)
    view_diff = summary_df.loc[0, "평균 조회수"]/summary_df.loc[1, "평균 조회수"]
    print(f"\n분석 결과: 자극적 제목의 평균 조회수가 일반 제목보다 약 {view_diff:.2f}배 높습니다.")

    #6 각 그룹의 조회수 top3 제목
    print("\n[자극적] 조회수 TOP 3")
    print(clickbait.sort_values(by='view_count', ascending=False)[['title', 'view_count']].head(3).to_string(index=False))

    print("\n[일반] 조회수 TOP3")
    print(normal.sort_values(by='view_count', ascending=False)[['title', 'view_count']].head(3).to_string(index=False))

if __name__ == "__main__":
    run_statistics()