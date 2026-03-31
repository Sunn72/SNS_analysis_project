import pandas as pd
import re
from sklearn.model_selection import train_test_split

def clean_text(text):
    #1 이메일, URL 등 제거
    #2 한글, 영어, 숫자 제외 특수문자 제거
    text = re.sub(f'[^\uAC00-\uD7A30-9a-zA-Z\s]', ' ', text)
    #3 중복 공백 제거
    text = re.sub(r'\s+', ' ', text).strip()
    return text

#4 데이터 로드
df = pd.read_csv('youtube_analysis_data.csv')
#제목 전처리 적용
df['title'] = df['title'].apply(clean_text)

#5 train, test 구분(8:2)
train_df, test_df = train_test_split(
    df, test_size = 0.2, random_state=42, stratify=df['label']
)

train_df.to_csv('train_data.psv', index=False, encoding='utf-8-sig')
test_df.to_csv('test_data.csv', index=False, encoding='utf-8-sig')

#6 종료 상황 출력
print('전처리 완료')
print(f"학습데이터: {len(train_df)}개, 테스트 데이터: {len(test_df)}개")