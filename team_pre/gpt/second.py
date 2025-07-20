import pandas as pd
import matplotlib.pyplot as plt

def draw_map(data_frame, file_name='map.png'):
    """
    분석된 데이터를 기반으로 지역 지도를 시각화하고 PNG 파일로 저장합니다.
    지도는 좌측 상단이 (1, 1), 우측 하단이 가장 큰 좌표가 되도록 시각화하며,
    그리드 라인, 다양한 구조물 표현 (아파트/빌딩, 반달곰 커피, 내 집, 건설 현장) 및
    (보너스) 범례를 포함합니다.
    """
    if data_frame.empty:
        print("시각화할 데이터가 없습니다. 1단계에서 데이터 처리가 올바르게 되었는지 확인하세요.")
        return

    # 맵의 최대 X, Y 좌표 계산
    x_max = data_frame['x'].max()
    y_max = data_frame['y'].max()

    plt.figure(figsize=(x_max + 1, y_max + 1)) # 지도 크기 설정
    ax = plt.gca() # 현재 축 가져오기

    # 좌표계 설정: (1,1)이 좌상단, (x_max, y_max)가 우하단
    ax.set_xlim(0.5, x_max + 0.5)
    ax.set_ylim(y_max + 0.5, 0.5) # y축을 역순으로 설정하여 (1,1)이 좌상단이 되도록 함

    # [cite_start]그리드 라인 그리기 [cite: 32]
    plt.grid(True, which='both', color='lightgray', linestyle='-', linewidth=0.5)
    plt.xticks(range(1, x_max + 1))
    plt.yticks(range(1, y_max + 1))

    # [cite_start]구조물 시각화 (겹침 우선순위 적용: 건설 현장 > 기타 구조물) [cite: 38]
    # [cite_start]1. 건설 현장 (회색 사각형) [cite: 36]
    construction_sites = data_frame[data_frame['struct_name'] == '건설현장']
    plt.scatter(construction_sites['x'], construction_sites['y'],
                marker='s', s=500, color='gray', label='건설 현장', alpha=0.9, zorder=3) # zorder를 높여 겹침 우선순위 확보

    # [cite_start]2. 반달곰 커피점 (녹색 사각형) [cite: 34]
    bandalgom_coffee = data_frame[data_frame['struct_name'] == '반달곰 커피']
    plt.scatter(bandalgom_coffee['x'], bandalgom_coffee['y'],
                marker='s', s=500, color='green', label='반달곰 커피', zorder=2)

    # [cite_start]3. 내 집 (녹색 삼각형) [cite: 35]
    my_home = data_frame[data_frame['struct_name'] == '내집']
    plt.scatter(my_home['x'], my_home['y'],
                marker='^', s=500, color='green', label='내 집', zorder=2)

    # [cite_start]4. 아파트와 빌딩 (갈색 원형) [cite: 33]
    apartments_buildings = data_frame[data_frame['struct_name'].isin(['아파트', '빌딩'])]
    plt.scatter(apartments_buildings['x'], apartments_buildings['y'],
                marker='o', s=500, color='saddlebrown', label='아파트/빌딩', zorder=1)

    # [cite_start](보너스) 범례 삽입 [cite: 8, 41]
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.title('Area 1 지도 시각화')
    plt.xlabel('X 좌표')
    plt.ylabel('Y 좌표')

    # [cite_start]이미지 저장 [cite: 39]
    plt.savefig(file_name, bbox_inches='tight')
    print(f"지도가 '{file_name}'으로 저장되었습니다.")
    plt.close()

if __name__ == "__main__":
    # 이 부분은 map_draw.py 단독 실행 시 테스트를 위한 코드입니다.
    # 실제 프로젝트에서는 1단계에서 생성된 DataFrame을 인자로 전달받아 사용합니다.
    # 테스트를 위해 가상의 DataFrame을 생성하거나, mas_map.py의 결과를 로드할 수 있습니다.
    # 여기서는 간단한 테스트 데이터를 생성합니다.

    # 가정: mas_map.py에서 필터링된 area 1 데이터가 있다고 가정합니다.
    # 실제 사용 시에는 mas_map.py에서 반환된 DataFrame을 사용해야 합니다.
    # 예:
    # from mas_map import process_data
    # df_area_1 = process_data()

    # 테스트용 가상 데이터 (실제 데이터와 동일한 컬럼명을 사용해야 함)
    test_data = {
        'area': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'x': [1, 2, 3, 4, 5, 2, 4, 1, 3, 5],
        'y': [1, 2, 3, 4, 5, 1, 2, 3, 5, 1],
        'struct_id': [100, 100, 200, 300, 400, 100, 200, 300, 400, 100],
        'struct_name': ['아파트', '아파트', '반달곰 커피', '내집', '건설현장', '아파트', '반달곰 커피', '내집', '건설현장', '아파트']
    }
    df_area_1_test = pd.DataFrame(test_data)

    print("--- 2단계 지도 시각화 시작 ---")
    draw_map(df_area_1_test, 'map.png')
    print("--- 2단계 지도 시각화 완료 ---")