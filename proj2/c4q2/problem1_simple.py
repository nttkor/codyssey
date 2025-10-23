import os
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
# --- 1. 읽기 및 전처리 ---
df = pd.read_csv("data.csv", dtype=str)
cols_keep = ["행정구역별(시군구)", "성별", "연령별", "시점", "일반가구원"]
df = df.loc[:, df.columns.isin(cols_keep)].copy()
df["연도"] = df["시점"].astype(str).str.replace(r'\D', '', regex=True).astype(int)
df["일반가구원"] = pd.to_numeric(df["일반가구원"].str.replace(",", "").replace("X", ""), errors="coerce")
df = df[(df["연도"] >= 2015) & (df["행정구역별(시군구)"] == "전국")]

# --- 2. 성별(남자/여자) 연도별 집계 출력 ---
sex_df = df[df["성별"].isin(["남자", "여자"])]
sex_pivot = sex_df.pivot_table(index="연도", columns="성별", values="일반가구원", aggfunc="sum").sort_index()
print("== Sex (Male/Female) by Year ==")
print(sex_pivot)
sex_pivot.to_csv("sex_year_general_household.csv", encoding="utf-8-sig")

# --- 3. 연령별 연도별 집계 ---
age_agg = df.groupby(["연도", "연령별"], as_index=False)["일반가구원"].sum()
age_pivot = age_agg.pivot(index="연도", columns="연령별", values="일반가구원").sort_index()
print("\n== Age groups by Year (sample rows) ==")
print(age_pivot.head())
age_pivot.to_csv("age_year_general_household.csv", encoding="utf-8-sig")
# 9) 시각화: 성별 연도별 꺾은선 그래프
ax1 = sex_pivot.plot(title="남자/여자 연도별 일반가구원 (2015년 이후)", marker="o", figsize=(10,5))
ax1.set_xlabel("연도")
ax1.set_ylabel("일반가구원 (명)")
plt.show()
# 그래프를 화면에 표시하려면 실행 환경에서 자동으로 출력됨
# 10) 시각화: 연령별 연도별 꺾은선 그래프 (주요 연령대만 보여주려면 선택)
# 전체 연령 컬럼이 많으므로, 그래프에 표시할 연령대를 선택(예: '15세미만','15~19세','20~24세',... 등)
# 사용 가능한 연령 레이블을 자동으로 선택
age_cols = list(age_pivot.columns)
# 화면 과밀을 막기 위해 대표 연령대(모든 연령대가 필요하면 전체를 사용)
age_plot_cols = age_cols  # 전체 사용; 필요 시 슬라이싱 가능
ax2 = age_pivot[age_plot_cols].plot(title="연령별 연도별 일반가구원 (2015년 이후)", figsize=(12,8))
ax2.set_xlabel("year")
ax2.set_ylabel("일반가구원 (명)")
plt.show()


# --- 5. 간단 요약 리포트 출력 ---
total_per_year = df.groupby("연도", as_index=False)["일반가구원"].sum().set_index("연도")
print("\n== Total general household members per year ==")
print(total_per_year)
if "15세미만" in age_pivot.columns and "65세이상" in age_pivot.columns:
    start, end = age_pivot.index.min(), age_pivot.index.max()
    print(f"\n15세미만: {start} -> {end} : {int(age_pivot.loc[start,'15세미만']):,} -> {int(age_pivot.loc[end,'15세미만']):,}")
    print(f"65세이상: {start} -> {end} : {int(age_pivot.loc[start,'65세이상']):,} -> {int(age_pivot.loc[end,'65세이상']):,}")

print("\nSaved: sex_year_general_household.csv, age_year_general_household.csv, age_year_general_household_styles.png")




# # --- 4. 연령별 그래프: 다양한 마커와 선종류 ---
# markers = ["o", "s", "D", "^", "v", "<", ">", "P", "X", "*", "h", "H", "d", "+"]
# linestyles = ["-", "--", "-.", ":", (0, (3, 1)), (0, (5, 1)), (0, (1, 1))]
# cols = list(age_pivot.columns)
# plt.figure(figsize=(12, 8))
# for i, col in enumerate(cols):
#     plt.plot(age_pivot.index, age_pivot[col].fillna(0),
#              label=col,
#              marker=markers[i % len(markers)],
#              linestyle=linestyles[i % len(linestyles)],
#              linewidth=1.5,
#              markersize=5)
# plt.title("General Household Members by Age Group (Yearly)")
# plt.xlabel("Year")
# plt.ylabel("Number of General Household Members")
# plt.grid(alpha=0.3)
# plt.legend(title="Age Group", bbox_to_anchor=(1.02, 1), loc="upper left")
# plt.tight_layout()
# plt.savefig("age_year_general_household_styles.png", dpi=150, bbox_inches="tight")
# plt.show()
# plt.close()