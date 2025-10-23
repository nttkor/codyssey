import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
#%matplotlib inline 주피터노트북
os.chdir(os.path.dirname(__file__))
# 1) CSV 읽기
df = pd.read_csv("data.csv", dtype=str)

# 2) 숫자형 컬럼들을 정리: 쉼표 제거 후 숫자로 변환
def to_num(s):
    if pd.isna(s): 
        return pd.NA
    s = str(s).replace(",", "").replace("X", "")
    return pd.to_numeric(s, errors="coerce")

# 컬럼명 확인
print("원본 컬럼:", list(df.columns))

# 3) 필요한 기본 컬럼만 남김: '행정구역별(시군구)','성별','연령별','시점','일반가구원'
keep_cols = ["행정구역별(시군구)", "성별", "연령별", "시점", "일반가구원"]
df = df.loc[:, df.columns.isin(keep_cols)].copy()

# 4) '시점'을 연도로 정리하고 숫자형 '일반가구원'으로 변환
df["시점"] = df["시점"].str.strip()
df = df[df["시점"].notna()]
df["연도"] = df["시점"].astype(str).str.replace(r'\D','', regex=True).astype(int)
df["일반가구원"] = df["일반가구원"].apply(to_num)

# 5) 2015년 이후 데이터만 사용 (요구사항)
df = df[df["연도"] >= 2015].reset_index(drop=True)

# 6) 전국(전체) 자료만 사용 (행정구역별이 '전국'인 행)
df = df[df["행정구역별(시군구)"] == "전국"].copy()

# 7) 성별별(남자/여자) 연도별 일반가구원 통계
# '성별'이 '남자','여자'로 표기된 경우만 선택. '계' 제외
sex_df = df[df["성별"].isin(["남자", "여자"])].copy()
sex_pivot = sex_df.pivot_table(index="연도", columns="성별", values="일반가구원", aggfunc="sum").sort_index()
print("\n성별(남자/여자) 연도별 일반가구원")
print(sex_pivot)

# 8) 연령별(모든 성별 합산) 연도별 일반가구원 통계
age_df = df.copy()
# 연령별로 합치려면 성별 구분을 제거하고 연령별 합계 계산
age_agg = age_df.groupby(["연도", "연령별"], as_index=False)["일반가구원"].sum()
age_pivot = age_agg.pivot(index="연도", columns="연령별", values="일반가구원").sort_index()
print("\n연령별 연도별 일반가구원 (연령별 컬럼들이 열로 표시됨)")
print(age_pivot)

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
# 11) 결과 저장(옵션): 전처리된 성별/연령별 테이블을 CSV로 저장
sex_pivot.to_csv("sex_year_general_household.csv", encoding="utf-8-sig")
age_pivot.to_csv("age_year_general_household.csv", encoding="utf-8-sig")
print("\nCSV로 저장 완료: sex_year_general_household.csv, age_year_general_household.csv")

# 12) 간단한 수치 기반 요약 리포트(자동 생성)
# 전체 연도별 합계 추세 (계열 합)
total_per_year = df.groupby("연도", as_index=False)["일반가구원"].sum().set_index("연도")
print("\n연도별 전국 일반가구원 합계")
print(total_per_year)

# 연령대별(예: 15세미만 / 65세이상) 추세 비교
trend_young = age_pivot.get("15세미만") if "15세미만" in age_pivot.columns else None
trend_old = age_pivot.get("65세이상") if "65세이상" in age_pivot.columns else None

if trend_young is not None and trend_old is not None:
    recent = age_pivot.index.max()
    older = age_pivot.index.min()
    print(f"\n요약: 15세미만: {older}년 {trend_young.loc[older]:,.0f}명 -> {recent}년 {trend_young.loc[recent]:,.0f}명")
    print(f"요약: 65세이상: {older}년 {trend_old.loc[older]:,.0f}명 -> {recent}년 {trend_old.loc[recent]:,.0f}명")

# 끝
