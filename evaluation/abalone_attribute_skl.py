# 0. 라이브러리 임포트

```python
import pandas as pd  # DataFrame 생성, CSV 읽기/쓰기, 통계 처리
import random        # 무작위 샘플링 및 SMOTE 합성 샘플 생성에 사용
import math          # 필요시 수학 함수 사용
from sklearn.preprocessing import MinMaxScaler, StandardScaler  # sklearn 비교용 스케일러
```

* **목적:** 데이터 처리, 샘플링, 수치 계산, 스케일링을 위해 필요한 라이브러리를 불러옴.
* **검증:** 임포트 오류가 발생하면 코드 실행 불가 → 패키지 설치 필요.

# 1. 파일 읽기: 컬럼명과 데이터

```python
with open("abalone_attributes.txt", "r", encoding="utf-8") as f:
    columns = [line.strip() for line in f.readlines()]
```

* **동작:** 텍스트 파일을 열어 한 줄씩 읽고, 공백 제거 후 리스트로 저장.
* **중간 상태:**
  `columns = ["Sex", "Length", "Diameter", "Height", "Whole weight", "Shucked weight", "Viscera weight", "Shell weight", "Rings"]`
* **검증 포인트:** 리스트 길이 9인지 확인.
* **예외:** 파일 없음 → `FileNotFoundError`, 디코딩 문제 → `UnicodeDecodeError`

```python
df = pd.read_csv("abalone.txt", names=columns)
```

* **동작:** CSV 파일을 읽어 DataFrame으로 변환. `names=columns`로 컬럼명 지정.
* **중간 상태:**
  `df.shape` 예: `(4177, 9)`
  `df.dtypes` 확인: `'Sex'` object, 나머지 numeric
* **검증:** 상위 5행 출력(`df.head()`)

---

# 2. Label 분리

```python
df["label"] = df["Sex"]
df = df.drop(columns=["Sex"])
```

* **동작:**

  * `Sex` 컬럼을 그대로 `label`로 복사
  * 원본 `Sex` 컬럼 삭제
* **중간 상태:**
  `df.columns = ["Length","Diameter",...,"Rings","label"]`
* **검증:** `label` 존재, `Sex` 제거, `label.value_counts()` 확인 → `{'M':1528, 'I':1342, 'F':1307}`

---

# 3. 데이터와 라벨 분리

```python
data = df.drop(columns=["label"])
label = df["label"]
```

* **동작:**

  * `data`: 수치 특성만 남김
  * `label`: 성별 시리즈 분리
* **중간 상태:**

  * `data.shape = (4177, 8)`
  * `label.shape = (4177,)`
* **검증:** `data.dtypes` numeric 확인, 결측치 없음

---

# 4. 수동 Min-Max Scaling

```python
def minmax_scale_manual(df):
    scaled = df.copy()
    for col in df.columns:
        col_min = df[col].min()
        col_max = df[col].max()
        scaled[col] = (df[col] - col_min) / (col_max - col_min)
    return scaled
```

* **동작:** 각 열마다 `(x - min)/(max - min)` 계산
* **중간 상태:**

  * 모든 값 0 ≤ x ≤ 1
  * 상수열이면 분모 0 → 실제 코드에서는 `0.0` 처리 필요
* **검증:** `scaled.describe().loc[['min','max']]` → min=0, max=1

```python
data_minmax_manual = minmax_scale_manual(data)
```

* 수동 Min-Max 적용

```python
scaler = MinMaxScaler()
data_minmax_sklearn = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
```

* **비교:** sklearn MinMaxScaler 사용, 동일 결과 예상

---

# 5. 수동 Standard Scaling

```python
def standard_scale_manual(df):
    scaled = df.copy()
    for col in df.columns:
        mean = df[col].mean()
        std = df[col].std()
        scaled[col] = (df[col] - mean) / std
    return scaled
```

* **동작:** `(x - mean) / std` 계산
* **검증:** 평균 ≈ 0, 표준편차 ≈ 1

```python
data_std_manual = standard_scale_manual(data)
std_scaler = StandardScaler()
data_std_sklearn = pd.DataFrame(std_scaler.fit_transform(data), columns=data.columns)
```

* **비교:** sklearn StandardScaler와 결과 확인

---

# 6. Random Over/Under Sampling

```python
def random_over_sampling(data, label):
    df_all = pd.concat([data,label], axis=1)
    groups = df_all.groupby("label")
    max_size = groups.size().max()
    sampled = []
    for name, group in groups:
        sampled_group = group.sample(max_size, replace=True, random_state=1)
        sampled.append(sampled_group)
    df_resampled = pd.concat(sampled)
    return df_resampled.drop(columns=["label"]), df_resampled["label"]
```

* **동작:** 소수 클래스 복원 추출로 샘플 수를 다수 클래스와 맞춤
* **출력:** 오버샘플링된 DataFrame과 label

```python
def random_under_sampling(data,label):
    df_all = pd.concat([data,label], axis=1)
    groups = df_all.groupby("label")
    min_size = groups.size().min()
    sampled=[]
    for name, group in groups:
        sampled_group = group.sample(min_size, replace=False, random_state=1)
        sampled.append(sampled_group)
    df_resampled = pd.concat(sampled)
    return df_resampled.drop(columns=["label"]), df_resampled["label"]
```

* **동작:** 다수 클래스 랜덤 추출하여 소수 클래스 수와 맞춤

```python
data_over, label_over = random_over_sampling(data, label)
data_under, label_under = random_under_sampling(data, label)
```

* **검증:** `label_over.value_counts()`, `label_under.value_counts()`

---

# 7. 간단한 SMOTE

```python
def simple_smote(data,label,k=3):
    df_all = pd.concat([data,label], axis=1)
    counts = df_all["label"].value_counts()
    max_count = counts.max()
    new_samples=[]
    for c in counts.index:
        class_data = df_all[df_all["label"]==c].iloc[:,:-1]
        n_to_add = max_count - len(class_data)
        class_list = class_data.values.tolist()
        for _ in range(n_to_add):
            x1 = random.choice(class_list)
            x2 = random.choice(class_list)
            lam = random.random()
            synthetic = [x1[i]+lam*(x2[i]-x1[i]) for i in range(len(x1))]
            new_samples.append(synthetic+[c])
    smote_df = pd.concat([df_all,pd.DataFrame(new_samples,columns=df_all.columns)])
    return smote_df.drop(columns=["label"]), smote_df["label"]
```

* **동작:**

  * 각 클래스 내부에서 두 샘플 랜덤 선택
  * 선형 보간으로 합성 샘플 생성
  * 다수 클래스 수까지 샘플링
* **검증:** `label_smote.value_counts()` → 모든 클래스 동일 개수

```python
data_smote, label_smote = simple_smote(data,label)
```

* SMOTE 적용

---

# 8. 최종 종료 메시지

```python
print("처리가 완료되었습니다.")
```

* 전체 데이터 처리, 스케일링, 오버/언더 샘플링, SMOTE까지 완료됨을 사용자에게 알림

---

# 🔹 요약: 실행 순서

1. 컬럼명 읽기 → 리스트 생성
2. CSV 파일 읽어 DataFrame 생성
3. `Sex` → `label` 복사 후 원본 삭제
4. `data`와 `label` 분리
5. Min-Max Scaling 수동 구현 & sklearn 비교
6. Standard Scaling 수동 구현 & sklearn 비교
7. Random Over / Under Sampling 수행
8. 간단한 SMOTE로 합성 샘플 생성
9. 최종 메시지 출력

---

원하면 제가 이 전체 프로세스를 **그림으로 흐름도**로 시각화해서, **입력 → 처리 → 출력** 단계별로 한눈에 볼 수 있게 만들어 드릴 수도 있어요.

혹시 그려드릴까요?
