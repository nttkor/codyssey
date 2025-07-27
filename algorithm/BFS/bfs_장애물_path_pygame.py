import pygame
import sys
from collections import deque
import random

# 설정
CELL_SIZE = 32
GRID_WIDTH = 20
GRID_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT

# 색상
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 50, 50)
VIOLET = (180, 50, 255)
GREEN = (150, 255, 150)
YELLOW = (255, 255, 0)
BLUE = (50, 50, 255)
BLACK = (0, 0, 0)

# 초기화
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("BFS Pathfinding with Obstacles and Queue Visualization")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 16, bold=True)

def create_grid(obstacle_ratio=0.2):
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if random.random() < obstacle_ratio:
                grid[y][x] = 1  # 장애물 표시
    return grid

def draw_grid(grid, visit_time, current, path, start, end, queued):
    max_time = max(visit_time.values(), default=1)

    # 배경 하얀색으로 전체 채우기
    screen.fill(WHITE)

    # 격자 그리기
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, GRAY, (0, y * CELL_SIZE), (WINDOW_WIDTH, y * CELL_SIZE))
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, GRAY, (x * CELL_SIZE, 0), (x * CELL_SIZE, WINDOW_HEIGHT))

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pos = (y, x)
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if grid[y][x] == 1:
                color = BLACK  # 장애물은 검정색 칠하기
            elif pos in path:
                color = YELLOW
            elif pos == current:
                color = VIOLET
            elif pos in queued:
                color = GREEN
            elif pos in visit_time:
                t = visit_time[pos]
                alpha = t / max_time
                shade = int(255 * (1 - alpha))  # 진한 파랑 → 연한 파랑
                color = (shade, shade, 255)
            else:
                color = WHITE

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

            # 텍스트 레이어
            text = None
            if pos == current:
                text = font.render("C", True, BLACK)
            elif pos in path:
                pass  # 최단 경로에는 숫자/문자 없음
            elif pos in queued:
                text = font.render("Q", True, BLACK)
            elif pos in visit_time and pos not in queued:
                text = font.render(f"{visit_time[pos]}", True, BLACK)

            if text:
                screen.blit(text, (x * CELL_SIZE + 8, y * CELL_SIZE + 7))

    # 시작과 끝 표시 (빨간색 사각형)
    sx, sy = start[1], start[0]
    ex, ey = end[1], end[0]
    pygame.draw.rect(screen, RED, (sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (ex * CELL_SIZE, ey * CELL_SIZE, CELL_SIZE, CELL_SIZE))

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
                if grid[ny][nx] == 1:
                    continue  # 장애물은 무시
                if neighbor not in visit_time:
                    time += 1
                    visit_time[neighbor] = time
                    parent[neighbor] = current
                    queue.append(neighbor)

        draw_grid(grid, visit_time, current, [], start, end, queue)
        pygame.display.update()
        clock.tick(10)

    path = []
    node = end
    while node in parent:
        path.append(node)
        node = parent[node]
    path.reverse()

    return path, visit_time, queue

def main():
    start = (GRID_HEIGHT // 2, GRID_WIDTH // 2)
    end = (GRID_HEIGHT // 2 - 1, GRID_WIDTH - 3)

    grid = create_grid(obstacle_ratio=0.2)
    grid[start[0]][start[1]] = 0  # 시작점 장애물 없애기
    grid[end[0]][end[1]] = 0      # 도착점 장애물 없애기

    path, visit_time, queue = bfs(grid, start, end)

    # 경로 표시 애니메이션
    for i, node in enumerate(path):
        draw_grid(grid, visit_time, node, path[:i+1], start, end, queue)
        pygame.display.update()
        clock.tick(20)

    # 종료 대기
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

main()
