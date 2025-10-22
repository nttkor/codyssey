import pandas as pd
import random
import math

# 1️⃣ 컬럼명 읽기
with open("abalone_attributes.txt", "r", encoding="utf-8") as f:
    columns = [line.strip() for line in f.readlines()]

# 2️⃣ CSV 읽기
df = pd.read_csv("abalone.txt", names=columns)

# 3️⃣ label 분리
df["label"] = df["Sex"]
df = df.drop(columns=["Sex"])

# 4️⃣ data / label 분리
data = df.drop(columns=["label"])
label = df["label"]

# 5️⃣ ✅ 수동 Min-Max Scaling
def minmax_scale_manual(df):
    scaled = df.copy()
    for col in df.columns:
        col_min = df[col].min()
        col_max = df[col].max()
        if col_max != col_min:  # 분모 0 방지
            scaled[col] = (df[col] - col_min) / (col_max - col_min)
        else:
            scaled[col] = 0.0
    return scaled

data_minmax = minmax_scale_manual(data)

# 6️⃣ ✅ 수동 Standard Scaling
def standard_scale_manual(df):
    scaled = df.copy()
    for col in df.columns:
        mean = df[col].mean()
        std = df[col].std()
        if std != 0:
            scaled[col] = (df[col] - mean) / std
        else:
            scaled[col] = 0.0
    return scaled

data_std = standard_scale_manual(data)

# 7️⃣ ✅ Random Over Sampling
def random_over_sampling(data, label):
    df_all = pd.concat([data, label], axis=1)
    groups = df_all.groupby("label")
    max_size = groups.size().max()
    sampled = []
    for name, group in groups:
        sampled_group = group.sample(max_size, replace=True, random_state=1)
        sampled.append(sampled_group)
    df_resampled = pd.concat(sampled)
    return df_resampled.drop(columns=["label"]), df_resampled["label"]

# 8️⃣ ✅ Random Under Sampling
def random_under_sampling(data, label):
    df_all = pd.concat([data, label], axis=1)
    groups = df_all.groupby("label")
    min_size = groups.size().min()
    sampled = []
    for name, group in groups:
        sampled_group = group.sample(min_size, replace=False, random_state=1)
        sampled.append(sampled_group)
    df_resampled = pd.concat(sampled)
    return df_resampled.drop(columns=["label"]), df_resampled["label"]

# 9️⃣ ✅ 간단한 SMOTE
def simple_smote(data, label):
    df_all = pd.concat([data, label], axis=1)
    counts = df_all["label"].value_counts()
    max_count = counts.max()
    new_samples = []

    for c in counts.index:
        class_data = df_all[df_all["label"] == c].iloc[:, :-1]
        n_to_add = max_count - len(class_data)
        class_list = class_data.values.tolist()
        for _ in range(n_to_add):
            x1 = random.choice(class_list)
            x2 = random.choice(class_list)
            lam = random.random()
            synthetic = [x1[i] + lam * (x2[i] - x1[i]) for i in range(len(x1))]
            new_samples.append(synthetic + [c])

    smote_df = pd.concat([df_all, pd.DataFrame(new_samples, columns=df_all.columns)])
    return smote_df.drop(columns=["label"]), smote_df["label"]

# 10️⃣ 실행
data_over, label_over = random_over_sampling(data, label)
data_under, label_under = random_under_sampling(data, label)
data_smote, label_smote = simple_smote(data, label)

print("✅ 모든 처리 완료!")
