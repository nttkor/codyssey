import pandas as pd
import matplotlib.pyplot as plt

# 파일 읽기 (다운로드한 CSV 파일을 같은 폴더에 두고 실행)
df = pd.read_csv("data.csv", dtype=str)

# 필요한 식별자와 '일반가구원'만 남기기 (나머지 컬럼 삭제)
keep = ["행정구역별(시군구)", "성별", "연령별", "시점", "일반가구원"]
df = df.loc[:, df.columns.isin(keep)].copy()

# 시점 -> 연도 정리: 숫자만 추출해 연도 컬럼 생성
df["연도"] = df["시점"].astype(str).str.replace(r"\D", "", regex=True)
df = df[df["연도"] != ""]                         # 비어있는 시점 제거
df["연도"] = df["연도"].astype(int)               # 정수형으로 변환

# '일반가구원' 문자열 정리 -> 숫자형으로 변환 (쉼표 제거, "X" 제거)
df["일반가구원"] = pd.to_numeric(
    df["일반가구원"].astype(str).str.replace(",", "").str.replace("X", ""),
    errors="coerce"
)

# 2015년 이후의 최대 기간으로 필터 (요구사항)
df = df[df["연도"] >= 2015].reset_index(drop=True)

# (권장) '전국' 단위만 사용 — 파일이 전국만 있으면 영향 없음
if "행정구역별(시군구)" in df.columns:
    df = df[df["행정구역별(시군구)"] == "전국"].reset_index(drop=True)

# --- 남자/여자 연도별 일반가구원 통계 출력 ---
sex_df = df[df["성별"].isin(["남자", "여자"])]   # '남자'와 '여자'만 선택
sex_pivot = sex_df.pivot_table(
    index="연도", columns="성별", values="일반가구원", aggfunc="sum"
).sort_index()                                    # 연도 오름차순 정렬
print("== Male / Female : yearly general household members ==")
print(sex_pivot)
sex_pivot.to_csv("sex_year_general_household.csv", encoding="utf-8-sig")  # CSV 저장

# --- 연령별(성별 합산) 연도별 일반가구원 통계 출력 ---
age_agg = df.groupby(["연도", "연령별"], as_index=False)["일반가구원"].sum()
age_pivot = age_agg.pivot(index="연도", columns="연령별", values="일반가구원").sort_index()
print("\n== Age groups by year (total general household members) ==")
print(age_pivot)
age_pivot.to_csv("age_year_general_household.csv", encoding="utf-8-sig")  # CSV 저장

# --- 남/여의 연령별 추세 그래프 (꺾은선) 생성 ---
markers = ["o", "s", "D", "^", "v", "<", ">", "P", "X", "*", "h", "H", "d", "+"]
linestyles = ["-", "--", "-.", ":", (0, (3,1)), (0, (5,1)), (0, (1,1))]

# 남자 피벗: index=연도, columns=연령별, 결측은 0으로 대체
male_pivot = df[df["성별"]=="남자"].groupby(["연도","연령별"], as_index=False)["일반가구원"].sum() \
    .pivot(index="연도", columns="연령별", values="일반가구원").fillna(0).sort_index()

# 여자 피벗: index=연도, columns=연령별, 결측은 0으로 대체
female_pivot = df[df["성별"]=="여자"].groupby(["연도","연령별"], as_index=False)["일반가구원"].sum() \
    .pivot(index="연도", columns="연령별", values="일반가구원").fillna(0).sort_index()

# Male plot: 각 연령대별로 서로 다른 마커와 선종류 사용
plt.figure(figsize=(12,6))
for i, col in enumerate(male_pivot.columns):
    plt.plot(
        male_pivot.index,
        male_pivot[col],
        label=str(col),
        marker=markers[i % len(markers)],
        linestyle=linestyles[i % len(linestyles)],
        linewidth=1
    )
plt.title("Male: General household members by age group (Yearly)")
plt.xlabel("Year")
plt.ylabel("Number")
plt.legend(title="Age group", bbox_to_anchor=(1.02,1), loc="upper left")  # 범례를 오른쪽에 배치
plt.tight_layout()
plt.savefig("male_age_trends.png", dpi=150, bbox_inches="tight")  # PNG로 저장
plt.show()
plt.close()

# Female plot: 각 연령대별로 서로 다른 마커와 선종류 사용
plt.figure(figsize=(12,6))
for i, col in enumerate(female_pivot.columns):
    plt.plot(
        female_pivot.index,
        female_pivot[col],
        label=str(col),
        marker=markers[i % len(markers)],
        linestyle=linestyles[i % len(linestyles)],
        linewidth=1
    )
plt.title("Female: General household members by age group (Yearly)")
plt.xlabel("Year")
plt.ylabel("Number")
plt.legend(title="Age group", bbox_to_anchor=(1.02,1), loc="upper left")
plt.tight_layout()
plt.savefig("female_age_trends.png", dpi=150, bbox_inches="tight")
plt.show()
plt.close()

print("\nSaved: sex_year_general_household.csv, age_year_general_household.csv, male_age_trends.png, female_age_trends.png")
