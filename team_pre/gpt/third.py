import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

def find_shortest_path(grid_data, start, end, obstacles):
    """
    BFS 알고리즘을 사용하여 최단 경로를 찾습니다.
    건설 현장은 통과할 수 없습니다.

    Args:
        grid_data (pd.DataFrame): 전체 지도 데이터 (area 1 필터링된 데이터).
        start (tuple): 시작점 (x, y).
        end (tuple): 도착점 (x, y).
        obstacles (set): 지나갈 수 없는 건설 현장 좌표들의 집합.

    Returns:
        list: 시작점에서 도착점까지의 최단 경로 좌표 목록. 경로가 없으면 빈 리스트.
    """
    # 맵의 경계 정의
    max_x = grid_data['x'].max()
    max_y = grid_data['y'].max()

    queue = deque([(start, [start])]) # (현재 위치, 지금까지의 경로)
    visited = {start} # 방문한 좌표 기록

    # 8방향 이동 (대각선 포함)
    directions = [
        (0, 1), (0, -1), (1, 0), (-1, 0),  # 상하좌우
        (1, 1), (1, -1), (-1, 1), (-1, -1) # 대각선
    ]

    while queue:
        (curr_x, curr_y), path = queue.popleft()

        if (curr_x, curr_y) == end:
            return path

        for dx, dy in directions:
            next_x, next_y = curr_x + dx, curr_y + dy

            # 맵 범위 내에 있고, 방문하지 않았으며, 장애물이 아닌지 확인
            if (1 <= next_x <= max_x and 1 <= next_y <= max_y and
                    (next_x, next_y) not in visited and
                    (next_x, next_y) not in obstacles):
                visited.add((next_x, next_y))
                queue.append(((next_x, next_y), path + [(next_x, next_y)]))

    return [] # 경로를 찾지 못한 경우

def save_path_to_csv(path, filename='home_to_cafe.csv'):
    """
    찾은 경로를 CSV 파일로 저장합니다.

    Args:
        path (list): 경로 좌표 목록.
        filename (str): 저장할 CSV 파일 이름.
    """
    if not path:
        print("저장할 경로가 없습니다.")
        return

    df_path = pd.DataFrame(path, columns=['x', 'y'])
    df_path.to_csv(filename, index=False)
    print(f"경로가 '{filename}'으로 저장되었습니다.")

def visualize_final_map(data_frame, path, start_point, end_point, file_name='map_final.png'):
    """
    분석된 지도 데이터와 최단 경로를 함께 시각화하여 PNG 파일로 저장합니다.

    Args:
        data_frame (pd.DataFrame): 전체 지도 데이터 (area 1 필터링된 데이터).
        path (list): 최단 경로 좌표 목록.
        start_point (tuple): 시작점 (x, y).
        end_point (tuple): 도착점 (x, y).
        file_name (str): 저장할 이미지 파일 이름.
    """
    if data_frame.empty:
        print("시각화할 데이터가 없습니다. 1단계에서 데이터 처리가 올바르게 되었는지 확인하세요.")
        return

    x_max = data_frame['x'].max()
    y_max = data_frame['y'].max()

    plt.figure(figsize=(x_max + 1, y_max + 1))
    ax = plt.gca()

    ax.set_xlim(0.5, x_max + 0.5)
    ax.set_ylim(y_max + 0.5, 0.5)
    plt.grid(True, which='both', color='lightgray', linestyle='-', linewidth=0.5)
    plt.xticks(range(1, x_max + 1))
    plt.yticks(range(1, y_max + 1))

    # 구조물 시각화 (map_draw.py와 동일)
    construction_sites = data_frame[data_frame['struct_name'] == '건설현장']
    plt.scatter(construction_sites['x'], construction_sites['y'],
                marker='s', s=500, color='gray', label='건설 현장', alpha=0.9, zorder=3)

    bandalgom_coffee = data_frame[data_frame['struct_name'] == '반달곰 커피']
    plt.scatter(bandalgom_coffee['x'], bandalgom_coffee['y'],
                marker='s', s=500, color='green', label='반달곰 커피', zorder=2)

    my_home = data_frame[data_frame['struct_name'] == '내집']
    plt.scatter(my_home['x'], my_home['y'],
                marker='^', s=500, color='green', label='내 집', zorder=2)

    apartments_buildings = data_frame[data_frame['struct_name'].isin(['아파트', '빌딩'])]
    plt.scatter(apartments_buildings['x'], apartments_buildings['y'],
                marker='o', s=500, color='saddlebrown', label='아파트/빌딩', zorder=1)

    # 최단 경로 시각화 (빨간 선)
    if path:
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        plt.plot(path_x, path_y, color='red', linewidth=2, linestyle='-', marker='o', markersize=5, label='최단 경로', zorder=4)

    # 시작점과 도착점 명확히 표시
    plt.scatter(start_point[0], start_point[1], marker='*', s=800, color='blue', label='시작점 (내 집)', zorder=5)
    plt.scatter(end_point[0], end_point[1], marker='X', s=800, color='purple', label='도착점 (반달곰 커피)', zorder=5)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.title('Area 1 지도 및 최단 경로')
    plt.xlabel('X 좌표')
    plt.ylabel('Y 좌표')

    plt.savefig(file_name, bbox_inches='tight')
    print(f"최종 지도가 '{file_name}'으로 저장되었습니다.")
    plt.close()

if __name__ == "__main__":
    # 1단계에서 생성된 mas_map.py의 process_data 함수를 import하여 사용합니다.
    # 만약 mas_map.py가 실행 가능한 파일로 되어 있다면, 해당 파일을 먼저 실행하여
    # area 1 필터링된 데이터를 생성해야 합니다.
    # 여기서는 편의를 위해 mas_map.py의 내용을 직접 포함하거나, 테스트 데이터를 사용합니다.

    # 실제 사용 시에는 아래와 같이 1단계 모듈을 import 하여 df_area_1을 가져오는 것이 좋습니다.
    # from mas_map import process_data
    # df_area_1 = process_data()

    # 테스트를 위한 더미 데이터 (실제 프로젝트에서는 1단계의 결과물을 사용해야 합니다)
    # 이 데이터는 process_data() 함수의 결과를 모방해야 합니다.
    test_data_for_pathfinding = {
        'area': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        'x': [1, 2, 3, 4, 5, 2, 4, 1, 3, 5, 3, 1, 5, 2, 4],
        'y': [1, 2, 3, 4, 5, 1, 2, 3, 5, 1, 2, 5, 3, 4, 5],
        'struct_id': [100, 100, 200, 300, 400, 100, 200, 300, 400, 100, 500, 500, 500, 500, 500],
        'struct_name': ['아파트', '아파트', '반달곰 커피', '내집', '건설현장', '아파트', '반달곰 커피', '내집', '건설현장', '아파트', '아파트', '아파트', '아파트', '아파트', '아파트']
    }
    df_area_1_final = pd.DataFrame(test_data_for_pathfinding)

    print("--- 3단계 최단 경로 탐색 시작 ---")

    # 내 집과 반달곰 커피 지점 좌표 찾기
    home_location = df_area_1_final[df_area_1_final['struct_name'] == '내집'][['x', 'y']].iloc[0]
    cafe_location = df_area_1_final[df_area_1_final['struct_name'] == '반달곰 커피'][['x', 'y']].iloc[0]

    start_point = (int(home_location['x']), int(home_location['y']))
    end_point = (int(cafe_location['x']), int(cafe_location['y']))

    # 건설 현장 좌표 (장애물)
    obstacle_coords_df = df_area_1_final[df_area_1_final['struct_name'] == '건설현장'][['x', 'y']]
    obstacles = set(tuple(row) for row in obstacle_coords_df.values)

    print(f"시작점 (내 집): {start_point}")
    print(f"도착점 (반달곰 커피): {end_point}")
    print(f"건설 현장 (장애물): {obstacles}")

    # 최단 경로 탐색
    shortest_path = find_shortest_path(df_area_1_final, start_point, end_point, obstacles)

    if shortest_path:
        print(f"\n최단 경로 발견: {shortest_path}")
        # 경로 CSV 저장
        save_path_to_csv(shortest_path, 'home_to_cafe.csv')
    else:
        print("\n최단 경로를 찾을 수 없습니다.")

    # 최종 지도 시각화 (경로 포함)
    visualize_final_map(df_area_1_final, shortest_path, start_point, end_point, 'map_final.png')

    print("--- 3단계 최단 경로 탐색 완료 ---")