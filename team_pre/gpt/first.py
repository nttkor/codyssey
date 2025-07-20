import pandas as pd

def process_data():
    """
    세 개의 CSV 파일을 불러와 병합 및 정렬하고, area 1에 대한 데이터를 필터링하여 출력합니다.
    (보너스) 구조물 종류별 요약 통계를 리포트로 출력합니다.
    """
    # [cite_start]1. CSV 파일 불러오기 [cite: 21]
    try:
        df_map = pd.read_csv('area_map.csv')
        df_struct = pd.read_csv('area_struct.csv')
        df_category = pd.read_csv('area_category.csv')
    except FileNotFoundError as e:
        print(f"Error: Missing CSV file. Make sure 'area_map.csv', 'area_struct.csv', and 'area_category.csv' are in the same directory.")
        print(e)
        return

    print("--- area_map.csv 내용 ---")
    print(df_map.head())
    print("\n--- area_struct.csv 내용 ---")
    print(df_struct.head())
    print("\n--- area_category.csv 내용 ---")
    print(df_category.head())

    # [cite_start]2. 구조물 ID를 이름으로 변환 [cite: 22]
    # area_category.csv를 딕셔너리로 변환하여 매핑에 사용
    category_mapping = dict(zip(df_category['struct_id'], df_category['struct_name']))
    df_struct['struct_name'] = df_struct['struct_id'].map(category_mapping)
    print("\n--- 구조물 ID가 이름으로 변환된 area_struct.csv 내용 ---")
    print(df_struct.head())

    # [cite_start]3. 세 데이터를 하나의 DataFrame으로 병합 [cite: 23]
    # area_map과 area_struct를 'area'와 'x', 'y'를 기준으로 병합
    df_merged = pd.merge(df_map, df_struct, on=['area', 'x', 'y'], how='left')

    # [cite_start]병합된 데이터를 'area' 기준으로 정렬 [cite: 23]
    df_merged = df_merged.sort_values(by='area').reset_index(drop=True)
    print("\n--- 병합 및 area 기준으로 정렬된 데이터 ---")
    print(df_merged.head())
    print(df_merged.tail())


    # [cite_start]4. area 1에 대한 데이터만 필터링 [cite: 24, 25]
    df_area_1 = df_merged[df_merged['area'] == 1].copy()
    print("\n--- area 1에 대한 필터링된 데이터 ---")
    print(df_area_1.head())
    print(df_area_1.tail())

    # [cite_start](보너스) 구조물 종류별 요약 통계 출력 [cite: 27]
    print("\n--- (보너스) 구조물 종류별 요약 통계 ---")
    if 'struct_name' in df_area_1.columns:
        struct_summary = df_area_1['struct_name'].value_counts().sort_index()
        print(struct_summary)
    else:
        print("구조물 이름(struct_name) 컬럼이 없습니다. 데이터 병합 및 변환을 확인하세요.")

    return df_area_1

if __name__ == "__main__":
    processed_data = process_data()
    if processed_data is not None:
        print("\n데이터 분석 및 필터링 완료. 추가 작업 수행 가능.")