import pandas as pd                # 데이터프레임 생성, CSV 읽기/쓰기, 통계 처리용 라이브러리
import random                      # 난수 생성 및 무작위 샘플링용 라이브러리
import math                        # 수학 관련 함수 (현재 코드에서는 사용하지 않지만 확장 대비 포함)

# 1️⃣ 컬럼명 읽기 ------------------------------------------------------------
with open("abalone_attributes.txt", "r", encoding="utf-8") as f:        # 속성명 파일을 UTF-8로 읽기 모드로 엶
    columns = [line.strip() for line in f.readlines()]                  # 각 줄의 개행문자 제거(strip) 후 리스트로 저장

# 2️⃣ CSV 읽기 -------------------------------------------------------------
df = pd.read_csv("abalone.txt", names=columns)                          # 컬럼명을 지정해 abalone.txt 파일을 DataFrame으로 읽음

# 3️⃣ label 분리 -----------------------------------------------------------
df["label"] = df["Sex"]                                                # 'Sex' 컬럼을 복사해 'label' 컬럼 생성 (분류 목표)
df = df.drop(columns=["Sex"])                                          # 원본 'Sex' 컬럼은 삭제 (data에는 숫자만 남게 함)

# 4️⃣ data / label 분리 ---------------------------------------------------
data = df.drop(columns=["label"])                                      # 수치형 데이터만 남김 (입력 특징)
label = df["label"]                                                    # 라벨(성별) 데이터만 따로 추출

# 5️⃣ ✅ 수동 Min-Max Scaling ---------------------------------------------
def minmax_scale_manual(df):                                           # DataFrame 전체를 Min-Max 정규화하는 함수 정의
    scaled = df.copy()                                                 # 원본 손상 방지를 위해 복사본 생성
    for col in df.columns:                                             # 모든 컬럼(열)에 대해 반복
        col_min = df[col].min()                                        # 현재 컬럼의 최소값 계산
        col_max = df[col].max()                                        # 현재 컬럼의 최대값 계산
        if col_max != col_min:                                         # 최대값과 최소값이 같은 경우(상수열) 분모 0 방지
            scaled[col] = (df[col] - col_min) / (col_max - col_min)    # 수식: (x - min) / (max - min)
        else:                                                          # 상수열인 경우
            scaled[col] = 0.0                                          # 모든 값을 0.0으로 설정
    return scaled                                                      # 정규화된 DataFrame 반환

data_minmax = minmax_scale_manual(data)                                # data에 대해 수동 Min-Max 스케일링 수행

# 6️⃣ ✅ 수동 Standard Scaling --------------------------------------------
def standard_scale_manual(df):                                         # 표준화(Z-score) 함수 정의
    scaled = df.copy()                                                 # 원본 데이터 복사
    for col in df.columns:                                             # 모든 컬럼 반복
        mean = df[col].mean()                                          # 평균 계산
        std = df[col].std()                                            # 표준편차 계산
        if std != 0:                                                   # 분모 0 방지 (상수열인 경우)
            scaled[col] = (df[col] - mean) / std                       # 수식: (x - 평균) / 표준편차
        else:
            scaled[col] = 0.0                                          # 표준편차가 0이면 0으로 처리
    return scaled                                                      # 표준화된 DataFrame 반환

data_std = standard_scale_manual(data)                                 # data에 대해 수동 Standard Scaling 수행

# 7️⃣ ✅ Random Over Sampling ---------------------------------------------
def random_over_sampling(data, label):                                 # 무작위 오버샘플링 함수 정의
    df_all = pd.concat([data, label], axis=1)                          # 입력 데이터와 라벨을 합쳐 하나의 DataFrame 생성
    groups = df_all.groupby("label")                                   # label(성별) 기준으로 그룹화
    max_size = groups.size().max()                                     # 가장 많은 클래스의 샘플 수 확인
    sampled = []                                                       # 결과를 저장할 리스트 초기화
    for name, group in groups:                                         # 각 클래스별 그룹 순회
        sampled_group = group.sample(max_size, replace=True, random_state=1)  # 부족한 클래스는 복원추출로 늘림
        sampled.append(sampled_group)                                  # 샘플된 그룹을 리스트에 추가
    df_resampled = pd.concat(sampled)                                  # 모든 그룹을 하나로 합침
    return df_resampled.drop(columns=["label"]), df_resampled["label"] # feature, label로 분리하여 반환

# 8️⃣ ✅ Random Under Sampling --------------------------------------------
def random_under_sampling(data, label):                                # 무작위 언더샘플링 함수 정의
    df_all = pd.concat([data, label], axis=1)                          # 데이터와 라벨 결합
    groups = df_all.groupby("label")                                   # 라벨별로 그룹화
    min_size = groups.size().min()                                     # 가장 적은 클래스의 샘플 수 확인
    sampled = []                                                       # 결과 저장용 리스트
    for name, group in groups:                                         # 각 클래스별 그룹 순회
        sampled_group = group.sample(min_size, replace=False, random_state=1)  # 다수 클래스는 일부만 추출
        sampled.append(sampled_group)                                  # 리스트에 추가
    df_resampled = pd.concat(sampled)                                  # 병합하여 균형잡힌 DataFrame 생성
    return df_resampled.drop(columns=["label"]), df_resampled["label"] # feature, label로 분리하여 반환

# 9️⃣ ✅ 간단한 SMOTE -----------------------------------------------------
def simple_smote(data, label):                                         # 단순 SMOTE(합성 샘플 생성) 함수 정의
    df_all = pd.concat([data, label], axis=1)                          # 데이터와 라벨 결합
    counts = df_all["label"].value_counts()                            # 각 클래스별 샘플 개수 세기
    max_count = counts.max()                                           # 가장 많은 클래스의 개수 저장
    new_samples = []                                                   # 합성 샘플을 담을 리스트

    for c in counts.index:                                             # 각 클래스에 대해 반복
        class_data = df_all[df_all["label"] == c].iloc[:, :-1]         # 해당 클래스의 feature만 추출
        n_to_add = max_count - len(class_data)                         # 추가해야 할 합성 샘플 수 계산
        class_list = class_data.values.tolist()                        # 리스트 형태로 변환 (난수 선택용)
        for _ in range(n_to_add):                                      # 부족한 만큼 반복
            x1 = random.choice(class_list)                             # 첫 번째 샘플 무작위 선택
            x2 = random.choice(class_list)                             # 두 번째 샘플 무작위 선택
            lam = random.random()                                      # 0~1 사이 난수 λ 생성
            synthetic = [x1[i] + lam * (x2[i] - x1[i]) for i in range(len(x1))]  # 선형 보간으로 새로운 샘플 생성
            new_samples.append(synthetic + [c])                        # 새 샘플과 라벨을 결합해 저장

    smote_df = pd.concat([df_all, pd.DataFrame(new_samples, columns=df_all.columns)]) # 원본 + 합성 샘플 병합
    return smote_df.drop(columns=["label"]), smote_df["label"]         # feature, label로 나눠 반환

# 🔟 실행 ---------------------------------------------------------------
data_over, label_over = random_over_sampling(data, label)              # 오버샘플링 수행 → 균형잡힌 데이터 생성
data_under, label_under = random_under_sampling(data, label)           # 언더샘플링 수행 → 균형잡힌 축소 데이터 생성
data_smote, label_smote = simple_smote(data, label)                    # SMOTE 수행 → 합성 샘플 포함 균형 데이터 생성

print("✅ 모든 처리 완료!")                                            # 모든 단계 정상 완료 시 메시지 출력
