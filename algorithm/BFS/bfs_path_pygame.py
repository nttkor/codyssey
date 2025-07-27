import pygame
import sys
from collections import deque

# 설정
CELL_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT

# 색상 정의
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 50, 50)
VIOLET = (180, 50, 255)
GREEN = (150, 255, 150)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("BFS Pathfinding with Queue Visualization")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 16, bold=True)

# 빈 격자 생성 (장애물 없음)
def create_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# 그리드 및 상태 시각화 함수
def draw_grid(grid, visit_time, current, path, start, end, queued):
    max_time = max(visit_time.values(), default=1)
    queued_set = set(queued)

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pos = (y, x)
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            # 셀 색상 우선순위
            if pos in path:
                color = YELLOW
            elif pos == current:
                color = VIOLET
            elif pos in queued_set:
                color = GREEN
            elif pos in visit_time:
                t = visit_time[pos]
                alpha = t / max_time
                shade = int(255 * (1 - alpha))  # 진한 파랑 → 연한 파랑
                color = (shade, shade, 255)
            else:
                color = WHITE

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)  # 테두리

            # 텍스트 (C, Q, 방문 순서 숫자)
            text = None
            if pos == current:
                text = font.render("C", True, BLACK)
            elif pos in path:
                pass  # 경로엔 텍스트 없음
            elif pos in queued_set:
                text = font.render("Q", True, BLACK)
            elif pos in visit_time:
                text = font.render(f"{visit_time[pos]}", True, BLACK)

            if text:
                screen.blit(text, (x * CELL_SIZE + 8, y * CELL_SIZE + 7))

    # 시작점과 끝점 빨간색으로 칠하기
    sx, sy = start[1], start[0]
    ex, ey = end[1], end[0]
    pygame.draw.rect(screen, RED, (sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (ex * CELL_SIZE, ey * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# BFS 알고리즘
def bfs(grid, start, end):
    queue = deque([start])
    parent = {}
    visit_time = {start: 0}
    time = 0

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = queue.popleft()

        # 타이틀에 현재 좌표 및 FPS 표시 (고정 폭 포맷)
        fps = clock.get_fps()
        pygame.display.set_caption(
            f"BFS - Current: ({current[0]:02},{current[1]:02}) | FPS: {fps:05.2f}"
        )


        if current == end:
            break

        y, x = current
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y + dy, x + dx
            neighbor = (ny, nx)

            if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                if neighbor not in visit_time:
                    visit_time[neighbor] = time = time + 1
                    parent[neighbor] = current
                    queue.append(neighbor)

        # 큐 상태 포함해서 그리드 업데이트
        draw_grid(grid, visit_time, current, [], start, end, queue)
        pygame.display.update()
        clock.tick(30)

    # 최단 경로 추적
    path = []
    node = end
    while node in parent:
        path.append(node)
        node = parent[node]
    path.reverse()

    return path, visit_time, queue

# 메인 루프
def main():
    start = (GRID_HEIGHT // 2, GRID_WIDTH // 2)
    end = (GRID_HEIGHT // 2 - 1, GRID_WIDTH - 3)

    grid = create_grid()
    path, visit_time, queue = bfs(grid, start, end)

    # 최단 경로 애니메이션
    for i, node in enumerate(path):
        draw_grid(grid, visit_time, node, path[:i+1], start, end, queue)
        pygame.display.update()
        clock.tick(60)

    # 종료 대기 루프
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# 실행
main()
