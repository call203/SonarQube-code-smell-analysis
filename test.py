import pandas as pd
from lifelines import CoxPHFitter
from lifelines.utils import ConvergenceWarning
import warnings

# 예제 데이터 프레임 생성
data = {
    'Time': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
    'Event': [1, 1, 0, 1, 0, 1, 0, 0, 1, 0],
    'Smelly1': [1, 1, 1, 1, 1, 1, 0, 0, 1, 0],  # 예: Long Method
    'Smelly2': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],  # 예: Large Class
    'Smelly3': [1, 1, 1, 0, 0, 1, 0, 1, 0, 0]   # 예: Feature Envy
}

df = pd.DataFrame(data)

# 이벤트 발생 여부에 따른 Smelly1 변수의 분산 확인
events = df['Event'].astype(bool)
print("Variance when event occurred:", df.loc[events, 'Smelly1'].var())
print("Variance when event did not occur:", df.loc[~events, 'Smelly1'].var())

# 경고 무시 설정
warnings.simplefilter(action='ignore', category=ConvergenceWarning)

# COX 모델 생성 및 피팅
cph = CoxPHFitter()
cph.fit(df, duration_col='Time', event_col='Event')

# 모델 요약 출력
cph.print_summary()

# 모델 결과 시각화
cph.plot()


#Time: 이전 revision file 부터 reivision file사이의 시간 from SZZ :최근커밋 - 발생커밋
#Smell : 범위로 정한 smelll이 있는지 없는지 from SonarQube :둘다 SonarQube 돌려봐야할듯 그리고 그 
#Event : 수정을 한 경우 (만약 smell:1인데 event가 0이면 관련 없는 걸 수정한 경우) :이건 SZZ로 파악가능
