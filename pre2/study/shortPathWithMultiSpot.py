# 맵의 크기를 정의합니다.
map_size = 15

# 장애물 좌표들을 정의합니다.
obstacles = [(5, 5), (3, 7), (8, 4), (11, 12), (6, 8), (9, 4), (6, 11)]

# 커피숍 좌표들을 정의합니다.
coffee_shops = [(3, 5), (6, 4), (11, 7)]

# Home 좌표를 정의합니다.
home = (12, 3)

# 목표 좌표들을 정의합니다.
goals = [(2, 13), (3, 14)]

import heapq
import itertools

# Re-defining variables from the previous cell to ensure they are accessible
# 맵의 크기를 정의합니다.
map_size = 15

# 장애물 좌표들을 정의합니다.
obstacles = [(5, 5), (3, 7), (8, 4), (11, 12), (6, 8), (9, 4), (6, 11)]

# 커피숍 좌표들을 정의합니다.
coffee_shops = [(3, 5), (6, 4), (11, 7)]

# Home 좌표를 정의합니다.
home = (12, 3)

# 목표 좌표들을 정의합니다.
goals = [(2, 13), (3, 14)]


# 1. 장애물을 고려하여 두 지점 간의 최단 경로를 찾는 함수 (A* 알고리즘 사용)
def heuristic(a, b):
    # 맨해튼 거리 휴리스틱
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_shortest_path(start, goal, obstacles, map_size):
    # 우선순위 큐를 사용하여 탐색할 노드를 관리 (f_score, 현재_좌표)
    open_set = [(0 + heuristic(start, goal), start)]
    # 이미 탐색한 노드를 저장하고 최단 경로를 재구성하기 위한 딕셔너리
    came_from = {}
    # 시작점에서 각 노드까지의 실제 비용
    g_score = {start: 0}
    # 시작점에서 각 노드까지의 예상 총 비용 (g_score + heuristic)
    f_score = {start: heuristic(start, goal)}

    while open_set:
        # f_score가 가장 낮은 노드를 가져옴
        current_f, current = heapq.heappop(open_set)

        # 목표에 도달하면 경로를 재구성하여 반환
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        # 현재 노드의 이웃 노드들을 탐색
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)

            # 맵 범위를 벗어나거나 장애물이 있는 경우 스킵
            if not (0 <= neighbor[0] < map_size and 0 <= neighbor[1] < map_size):
                continue
            if neighbor in obstacles:
                continue

            # 이웃 노드까지의 새로운 g_score 계산
            tentative_g_score = g_score[current] + 1

            # 새로운 g_score가 기존 g_score보다 작거나, 이웃 노드를 처음 방문하는 경우
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                # 이웃 노드를 open_set에 추가하거나 업데이트
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    # 경로를 찾지 못한 경우 None 반환
    return None

# 3. 주어진 순열에 대한 총 경로 거리를 계산하는 함수
def calculate_total_distance(permutation, start, goals, obstacles, map_size):
    current_location = start
    total_distance = 0
    path_segments = []

    # Home에서 첫 번째 방문 지점까지의 경로
    first_stop = permutation[0]
    path = find_shortest_path(current_location, first_stop, obstacles, map_size)
    if path is None:
        return float('inf'), [] # 경로를 찾지 못한 경우 무한대 반환
    total_distance += len(path) - 1
    path_segments.append(path)
    current_location = first_stop

    # 방문 지점들 간의 경로
    for i in range(len(permutation) - 1):
        path = find_shortest_path(current_location, permutation[i+1], obstacles, map_size)
        if path is None:
            return float('inf'), []
        total_distance += len(path) - 1
        path_segments.append(path)
        current_location = permutation[i+1]

    # 마지막 방문 지점에서 목표 지점까지의 경로 (두 목표 중 최단 경로 선택)
    min_goal_distance = float('inf')
    best_goal_path = None
    final_goal = None

    for goal in goals:
        path = find_shortest_path(current_location, goal, obstacles, map_size)
        if path is not None:
            goal_distance = len(path) - 1
            if goal_distance < min_goal_distance:
                min_goal_distance = goal_distance
                best_goal_path = path
                final_goal = goal

    if best_goal_path is None:
         return float('inf'), []

    total_distance += min_goal_distance
    path_segments.append(best_goal_path)

    return total_distance, path_segments

# 2. 모든 커피숍을 방문하는 순열 생성 및 목표 지점 포함
# 목표 지점은 마지막에 추가되므로 커피숍 순열만 생성하고 목표는 calculate_total_distance에서 처리
coffee_shop_permutations = list(itertools.permutations(coffee_shops))

# 모든 가능한 전체 순열 (Home -> 커피숍 순열 -> 목표) 을 직접 생성하지 않고
# calculate_total_distance 함수에서 각 커피숍 순열에 대해 Home과 최단 목표까지의 경로를 계산합니다.
# coffee_shop_permutations 변수에 커피숍 방문 순서만 저장합니다.
# 계산된 총 거리와 해당 경로 정보를 저장할 리스트를 초기화합니다.
all_possible_paths = []

# 각 커피숍 순열에 대해 총 거리를 계산하고 경로 정보를 저장합니다.
for perm in coffee_shop_permutations:
    total_dist, path_segments = calculate_total_distance(perm, home, goals, obstacles, map_size)

    # 경로를 찾은 경우 (거리가 무한대가 아닌 경우) 저장합니다.
    if total_dist != float('inf'):
        all_possible_paths.append({
            'permutation': perm,
            'total_distance': total_dist,
            'path_segments': path_segments
        })

# 결과 확인 (옵션)
# print(f"Found {len(all_possible_paths)} valid paths.")
# for path_info in all_possible_paths:
#     print(f"Permutation: {path_info['permutation']}, Distance: {path_info['total_distance']}")

# 1. all_possible_paths 리스트가 비어 있는지 확인합니다.
if not all_possible_paths:
    print("유효한 경로를 찾을 수 없습니다.")
else:
    # 2. all_possible_paths 리스트에서 'total_distance' 키의 값을 기준으로 최소 거리를 가진 경로 정보를 찾습니다.
    shortest_path_info = min(all_possible_paths, key=lambda item: item['total_distance'])

    # 3. 찾은 최소 거리 경로 정보를 shortest_path_info 변수에 저장합니다. (이미 위에서 수행됨)

    # 결과 확인 (옵션)
    # print("\n최단 경로 정보:")
    # print(f"순열: {shortest_path_info['permutation']}")
    # print(f"총 거리: {shortest_path_info['total_distance']}")
    # print(f"경로 세그먼트 수: {len(shortest_path_info['path_segments'])}")
    
    import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정
# 시스템에 따라 폰트 경로 또는 이름이 다를 수 있습니다.
# 예시: 'NanumGothic' 또는 시스템에 설치된 다른 한글 폰트 이름
try:
    # 나눔 고딕 설치 여부 확인 및 사용
    font_path = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    nanum_font = next((font for font in font_path if 'NanumGothic' in font or 'NanumSquare' in font), None)
    if nanum_font:
        plt.rcParams['font.family'] = fm.FontProperties(fname=nanum_font).get_name()
        print(f"Using font: {plt.rcParams['font.family']}")
    else:
        plt.rcParams['font.family'] = 'Malgun Gothic' # Windows 기본 폰트
        print("NanumGothic not found, trying Malgun Gothic.")
except:
    plt.rcParams['font.family'] = 'AppleGothic' # macOS 기본 폰트
    print("Could not find NanumGothic or Malgun Gothic, trying AppleGothic.")


plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지

# 15x15 크기의 맵을 그리기 위해 figure와 axes 객체를 생성합니다.
fig, ax = plt.subplots(figsize=(8, 8))

# 맵의 배경을 나타내기 위해 빈 격자를 그립니다.
ax.set_xlim([0, map_size])
ax.set_ylim([0, map_size])
ax.set_xticks(range(map_size + 1))
ax.set_yticks(range(map_size + 1))
ax.grid(True)

# 장애물 좌표를 'X' 마커를 사용하여 맵에 표시합니다.
obstacle_x = [obs[0] for obs in obstacles]
obstacle_y = [obs[1] for obs in obstacles]
ax.plot(obstacle_x, obstacle_y, 'X', color='red', markersize=10, label='Obstacles')

# 커피숍 좌표를 'C' 마커를 사용하여 맵에 표시합니다.
coffee_x = [c[0] for c in coffee_shops]
coffee_y = [c[1] for c in coffee_shops]
ax.plot(coffee_x, coffee_y, 'o', color='brown', markersize=10, label='Coffee Shops')

# Home 좌표를 'H' 마커를 사용하여 맵에 표시합니다.
ax.plot(home[0], home[1], 's', color='blue', markersize=10, label='Home')

# 목표 좌표를 'G' 마커를 사용하여 맵에 표시합니다.
goal_x = [g[0] for g in goals]
goal_y = [g[1] for g in goals]
ax.plot(goal_x, goal_y, '*', color='green', markersize=12, label='Goals')

# 맵의 x축과 y축 범위를 0부터 map_size까지 설정합니다. (이미 위에서 설정됨)

# 맵의 제목을 "맵 시각화"와 같이 설정합니다.
ax.set_title("맵 시각화")
ax.set_xlabel("X 좌표")
ax.set_ylabel("Y 좌표")

# 범례를 표시합니다.
ax.legend()

# y축을 위로 향하게 설정 (일반적인 맵 좌표계)
plt.gca().invert_yaxis()

# 최단 경로 정보를 가져옵니다.
# shortest_path_info 변수가 정의되어 있어야 합니다.
if 'shortest_path_info' in locals() or 'shortest_path_info' in globals():
    path_segments = shortest_path_info['path_segments']

    # 각 경로 세그먼트를 순회하며 맵에 그립니다.
    for segment in path_segments:
        # 경로 세그먼트의 x, y 좌표를 추출합니다.
        segment_x = [point[0] for point in segment]
        segment_y = [point[1] for point in segment]

        # 맵 위에 빨간색 선으로 경로를 그립니다.
        ax.plot(segment_x, segment_y, '-', color='red', linewidth=2)
else:
    print("최단 경로 정보를 찾을 수 없습니다. 이전 단계를 실행했는지 확인해주세요.")


# 플롯을 화면에 표시합니다.
plt.show()

# 최단 경로로 방문하는 커피숍 순서를 출력합니다.
print(f"최단 경로 커피숍 방문 순서: {shortest_path_info['permutation']}")

# 최단 경로의 총 거리를 출력합니다.
print(f"최단 경로 총 거리: {shortest_path_info['total_distance']}")