import pandas as pd

#1. 데이터 읽기 및 DataFrame 생성
# 컬럼 이름 불러오기
with open('abalone_attribute.txt', 'r') as f:
    columns = [line.strip() for line in f.readlines()]

# 데이터 불러오기
df = pd.read_csv('abalone.txt', header=None, names=columns)

print("원본 데이터:")
print(df.head())
# 2. 성별 분리 및 삭제
# label 컬럼으로 성별 저장
df['label'] = df['Sex']

# 기존 Sex 컬럼 삭제
df.drop(columns=['Sex'], inplace=True)

print("\n성별 분리 후:")
print(df.head())

#3. Min-Max Scaling (직접 구현)
# Min-Max 수식: (x - min) / (max - min)
df_minmax_manual = df.copy()
for col in df.columns[:-1]:  # label 제외
    min_val = df[col].min()
    max_val = df[col].max()
    df_minmax_manual[col] = (df[col] - min_val) / (max_val - min_val)

print("\nMin-Max Scaling (수식 구현):")
print(df_minmax_manual.head())

# 4. Min-Max Scaling (sklearn 사용)
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
scaled_values = scaler.fit_transform(df[df.columns[:-1]])  # label 제외

df_minmax_sklearn = pd.DataFrame(scaled_values, columns=df.columns[:-1])
df_minmax_sklearn['label'] = df['label']

print("\nMin-Max Scaling (sklearn):")
print(df_minmax_sklearn.head())

#5. Standard Scaling (보너스 과제)
from sklearn.preprocessing import StandardScaler

std_scaler = StandardScaler()
std_scaled = std_scaler.fit_transform(df[df.columns[:-1]])

df_standard = pd.DataFrame(std_scaled, columns=df.columns[:-1])
df_standard['label'] = df['label']

print("\nStandard Scaling 결과:")
print(df_standard.head())