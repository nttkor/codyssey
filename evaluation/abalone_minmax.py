import pandas as pd  # pandas를 불러와 DataFrame 조작에 사용합니다
import random  # 무작위 샘플링 및 SMOTE용 난수 생성에 사용합니다
import math    # (필요시) 수학 함수 사용을 위해 임포트합니다

# ---------------------------
# 1. 파일 읽기
# ---------------------------
with open("abalone_attributes.txt", "r", encoding="utf-8") as f:  # 속성명이 담긴 파일을 열고
    columns = [line.strip() for line in f.readlines()]  # 각 줄을 읽어 공백 제거 후 리스트로 만듭니다

# 데이터 파일을 읽어 DataFrame 생성 (컬럼 이름을 위에서 읽은 columns로 지정)
df = pd.read_csv("abalone.txt", names=columns)  # abalone.txt를 ',' 구분자로 읽어 DataFrame으로 변환합니다

print("원본 데이터 (상위 5개):")  # 디버그용: 원본 데이터 일부를 출력합니다
print(df.head(), "\n")  # DataFrame의 상위 5개 행을 출력합니다

# ---------------------------
# 2. label 분리
# ---------------------------
df["label"] = df["Sex"]  # 'Sex' 컬럼의 값을 'label'이라는 새 컬럼으로 복사합니다
df = df.drop(columns=["Sex"])  # 원본의 'Sex' 컬럼은 더 이상 필요 없으므로 삭제합니다

print("성별 분리 후 데이터:")  # 디버그용 출력
print(df.head(), "\n")  # 변경된 DataFrame 상위 5개 행을 출력합니다

# ---------------------------
# 3. 데이터 / 라벨 분리
# ---------------------------
data = df.drop(columns=["label"])  # 특성(입력) 데이터만 남깁니다
label = df["label"]  # 분리한 'label' 시리즈(성별)를 따로 저장합니다

print("data shape:", data.shape)  # 특성 데이터의 형태(행,열) 출력
print("label shape:", label.shape, "\n")  # 레이블 시리즈의 길이 출력

# ---------------------------
# 4. Min-Max Scaling (직접 구현)
# ---------------------------
def minmax_scale_manual(df):  # 수동으로 Min-Max 정규화를 수행하는 함수 정의
    scaled = df.copy()  # 원본을 건드리지 않도록 복사본을 만듭니다
    for col in df.columns:  # 각 열(특성)을 순회합니다
        col_min = df[col].min()  # 해당 열의 최솟값을 구합니다
        col_max = df[col].max()  # 해당 열의 최댓값을 구합니다
        scaled[col] = (df[col] - col_min) / (col_max - col_min)  # (x - min) / (max - min) 공식을 적용합니다
    return scaled  # 정규화된 DataFrame을 반환합니다

data_minmax_manual = minmax_scale_manual(data)  # 수동 구현한 Min-Max 스케일링 적용
print("수식 기반 Min-Max Scaling 결과 (상위 5개):")  # 디버그용 출력
print(data_minmax_manual.head(), "\n")  # 스케일링 결과 상위 5개 표시

# ---------------------------
# sklearn 버전 (비교용)
# ---------------------------
from sklearn.preprocessing import MinMaxScaler, StandardScaler  # sklearn에서 제공하는 스케일러를 불러옵니다

scaler = MinMaxScaler()  # MinMaxScaler 객체 생성
data_minmax_sklearn = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)  # fit_transform으로 스케일링하고 DataFrame으로 변환
print("sklearn MinMaxScaler 결과 (상위 5개):")  # 디버그용 출력
print(data_minmax_sklearn.head(), "\n")  # sklearn 적용 결과 상위 5개 표시

# ---------------------------
# 5. Standard Scaling (직접 구현)
# ---------------------------
def standard_scale_manual(df):  # 수동으로 표준화(Standardization)를 수행하는 함수 정의
    scaled = df.copy()  # 원본을 보존하기 위해 복사본을 사용
    for col in df.columns:  # 각 열에 대해
        mean = df[col].mean()  # 평균 계산
        std = df[col].std()  # 표준편차 계산 (기본 pandas 표준편차는 샘플 표준편차(ddof=1))
        scaled[col] = (df[col] - mean) / std  # (x - mean) / std 공식을 적용합니다
    return scaled  # 표준화된 DataFrame 반환

data_std_manual = standard_scale_manual(data)  # 수동 표준화 수행
print("수식 기반 Standard Scaling 결과 (상위 5개):")  # 디버그용 출력
print(data_std_manual.head(), "\n")  # 수동 표준화 결과 상위 5개 출력

# sklearn 버전 (비교용)
std_scaler = StandardScaler()  # sklearn StandardScaler 객체 생성
data_std_sklearn = pd.DataFrame(std_scaler.fit_transform(data), columns=data.columns)  # fit_transform으로 표준화 후 DataFrame 변환
print("sklearn StandardScaler 결과 (상위 5개):")  # 디버그용 출력
print(data_std_sklearn.head(), "\n")  # sklearn 표준화 결과 상위 5개 출력

# ---------------------------
# 6. Random Over / Under Sampling
# ---------------------------
def random_over_sampling(data, label):  # 랜덤 오버샘플링 함수 정의
    df_all = pd.concat([data, label], axis=1)  # 특성 데이터와 라벨을 하나의 DataFrame으로 합칩니다
    groups = df_all.groupby("label")  # label 기준으로 그룹화합니다
    
    max_size = groups.size().max()  # 가장 많은 클래스의 샘플 개수를 구합니다
    sampled = []  # 샘플을 담을 리스트 초기화
    
    for name, group in groups:  # 각 클래스 그룹을 순회합니다
        sampled_group = group.sample(max_size, replace=True, random_state=1)  # 부족한 만큼 복원추출로 샘플을 늘립니다
        sampled.append(sampled_group)  # 결과 리스트에 추가
    
    df_resampled = pd.concat(sampled)  # 모든 그룹을 합쳐 재샘플링된 DataFrame을 만듭니다
    return df_resampled.drop(columns=["label"]), df_resampled["label"]  # 특성과 라벨을 분리해 반환


def random_under_sampling(data, label):  # 랜덤 언더샘플링 함수 정의
    df_all = pd.concat([data, label], axis=1)  # 특성+라벨 합치기
    groups = df_all.groupby("label")  # 라벨로 그룹화
    
    min_size = groups.size().min()  # 가장 적은 클래스의 개수를 기준으로 설정
    sampled = []  # 결과를 담을 리스트
    
    for name, group in groups:  # 각 그룹마다
        sampled_group = group.sample(min_size, replace=False, random_state=1)  # 중복 없이 샘플링하여 크기를 맞춥니다
        sampled.append(sampled_group)  # 리스트에 추가
    
    df_resampled = pd.concat(sampled)  # 합쳐서 반환할 DataFrame 생성
    return df_resampled.drop(columns=["label"]), df_resampled["label"]  # 특성과 라벨을 분리해 반환

# 실제로 오버/언더 샘플링 적용
data_over, label_over = random_over_sampling(data, label)  # 오버샘플링 적용
data_under, label_under = random_under_sampling(data, label)  # 언더샘플링 적용

print("Over Sampling 후 각 클래스 개수:")  # 디버그용 출력
print(label_over.value_counts(), "\n")  # 오버샘플링 후 클래스별 개수 출력

print("Under Sampling 후 각 클래스 개수:")  # 디버그용 출력
print(label_under.value_counts(), "\n")  # 언더샘플링 후 클래스별 개수 출력

# ---------------------------
# 7. 보너스: 간단한 SMOTE 구현
# ---------------------------
def simple_smote(data, label, k=3):  # SMOTE의 간단화 버전 함수 정의 (k는 사용하지 않음; 인터페이스 유지를 위해 포함)
    """SMOTE 간단 버전: 같은 클래스 내부의 두 샘플을 랜덤으로 골라 선형 보간하여 합성 샘플 생성"""
    df_all = pd.concat([data, label], axis=1)  # 특성+라벨 합치기
    counts = df_all["label"].value_counts()  # 각 클래스별 샘플 개수
    max_count = counts.max()  # 최다 클래스의 개수
    
    new_samples = []  # 생성한 합성 샘플을 담을 리스트
    for c in counts.index:  # 각 클래스마다
        class_data = df_all[df_all["label"] == c].iloc[:, :-1]  # 해당 클래스의 특성 데이터만 취함
        n_to_add = max_count - len(class_data)  # 보충해야 할 샘플 수 계산
        class_list = class_data.values.tolist()  # numpy array를 리스트로 변환하여 사용
        
        for _ in range(n_to_add):  # 필요한 만큼 합성 샘플을 생성
            x1 = random.choice(class_list)  # 클래스내 임의의 샘플 1
            x2 = random.choice(class_list)  # 클래스내 임의의 샘플 2
            lam = random.random()  # 0~1 사이의 랜덤 계수
            synthetic = [x1[i] + lam * (x2[i] - x1[i]) for i in range(len(x1))]  # 선형 보간으로 합성 샘플 생성
            new_samples.append(synthetic + [c])  # 라벨을 마지막에 붙여 리스트에 추가
    
    smote_df = pd.concat([df_all, pd.DataFrame(new_samples, columns=df_all.columns)])  # 원본에 합성 샘플을 합쳐 DataFrame 생성
    return smote_df.drop(columns=["label"]), smote_df["label"]  # 특성과 라벨 분리하여 반환

# SMOTE 적용
data_smote, label_smote = simple_smote(data, label)  # 간단 SMOTE 실행
print("SMOTE 적용 후 클래스 개수:")  # 디버그용 출력
print(label_smote.value_counts(), "\n")  # SMOTE 적용 후 클래스별 개수 출력

# ---------------------------
# 끝
# ---------------------------
print("처리가 완료되었습니다.")  # 전체 프로세스 종료 메시지 출력
