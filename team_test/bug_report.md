cafe_map.csv->cafe_map_org.csv 파일명 수정하고 제걸 업로딩했습니다.
## cafe_map.csv
    how = left
    struct_df = struct_df.merge(category_df, on = 'category', how = 'inner')
    del struct_df['category']  # category 열 제거, 필요 없으므로

    map과 병합 => ConstructionSite 추가 이건 how=left로 했습니다. 안그러면 contruct site이지만 struct가 아닌게 다 지워져요
    merged_df = map_df.merge(struct_df, on = ['x','y'], how = 'left')

## cafe_map_bonus.py
    merged_df를 불러서 처리했습니다.
    # --- 1. 데이터 불러오기 --------------------------------------------------
    df = pd.read_csv('merged.csv')
    df['struct'] = df['struct'].apply(lambda x: x.strip() if isinstance(x, str) else x)
    화면에도 출력하고 리포트파일로도 출력합니다. (판독하기는 좀 어렵습니다. 엑셀로는 문제 없을듯 )
    summary.to_csv('struct_summary_report.csv') 

# map_direct_save_bonus.py
    파일 머지부분을 머지된 파일을 로딩하는 걸로 간단하게 했습니다.
    그림이 늦게 나오는 부분 수정했습니다.

