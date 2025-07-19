# mas_map.py
import pandas as pd
import os

# base path
base_dir = os.path.dirname(__file__)
data_dir = os.path.join(base_dir, 'data')

# CSV 읽기
area_map = pd.read_csv(os.path.join(data_dir, 'area_map.csv'))
area_struct = pd.read_csv(os.path.join(data_dir, 'area_struct.csv'))
area_category = pd.read_csv(os.path.join(data_dir, 'area_category.csv'))

# 컬럼 정리 (공백 제거)
area_category = area_category.rename(columns={
    'category': 'category',
    ' struct': 'struct_name',  # 공백 포함된 컬럼명 정제
})

# 병합: category 컬럼 기준으로 구조물 이름 매핑
struct_with_name = area_struct.merge(area_category, on='category', how='left')

# area_map과 struct 병합: x, y 좌표 기준으로 결합
merged = area_map.merge(struct_with_name, on=['x', 'y'], how='left')
print("\n=== 반단곰카페 카테고리로 소트된 구조물 종류별 통계 ===")
merged = merged.sort_values(by='category')
area1 = merged[merged['category'] == 4]
print("=== Area 1 데이터 ===")
print(area1)
# area 순으로 정렬
merged = merged.sort_values(by='area')
print("\n=== 에리어로 소트된 구조물 종류별 통계 ===")
print(merged)
# area == 1 필터링
area1 = merged[merged['area'] == 1]

# 결과 출력
print("=== Area 1 데이터 ===")
print(area1)

# 구조물 종류별 카운트 통계
print("\n=== 구조물 종류별 통계 ===")
print(area1['struct_name'].value_counts())

# (선택) 파일로 저장 원하면:
# area1.to_csv('area1_filtered.csv', index=False)