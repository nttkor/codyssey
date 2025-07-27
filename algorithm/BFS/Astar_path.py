import pygame
import sys
import heapq

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
pygame.display.set_caption("A* Pathfinding Visualization")
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 16, bold=True)

def create_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def heuristic(a, b):
    # 맨해튼 거리
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def draw_grid(grid, cost_so_far, current, path, start, end, queued):
    max_cost = max(cost_so_far.values(), default=1)

    screen.fill(WHITE)
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, GRAY, (0, y * CELL_SIZE), (WINDOW_WIDTH, y * CELL_SIZE))
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, GRAY, (x * CELL_SIZE, 0), (x * CELL_SIZE, WINDOW_HEIGHT))

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pos = (y, x)
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if pos in path:
                color = YELLOW
            elif pos == current:
                color = VIOLET
            elif pos in queued:
                color = GREEN
            elif pos in cost_so_far:
                cost = cost_so_far[pos]
                alpha = cost / max_cost
                shade = int(255 * (1 - alpha))
                color = (shade, shade, 255)
            else:
                color = WHITE

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

            text = None
            if pos == current:
                text = font.render("C", True, BLACK)
            elif pos in path:
                pass
            elif pos in queued:
                text = font.render("Q", True, BLACK)
            elif pos in cost_so_far and pos not in queued:
                text = font.render(f"{cost_so_far[pos]}", True, BLACK)

            if text:
                screen.blit(text, (x * CELL_SIZE + 8, y * CELL_SIZE + 7))

    sx, sy = start[1], start[0]
    ex, ey = end[1], end[0]
    pygame.draw.rect(screen, RED, (sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (ex * CELL_SIZE, ey * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def a_star(grid, start, end):
    frontier = []
    heapq.heappush(frontier, (0, start))
    parent = {}
    cost_so_far = {start: 0}

    while frontier:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        _, current = heapq.heappop(frontier)

        # 타이틀에 현재 좌표 및 FPS 표시 (고정 폭 포맷)
        fps = clock.get_fps()
        pygame.display.set_caption(
            f"A* - Current: ({current[0]:02},{current[1]:02}) | FPS: {fps:05.2f}"
        )

        if current == end:
            break

        y, x = current
        for dy, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
            ny, nx = y + dy, x + dx
            neighbor = (ny, nx)
            if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                new_cost = cost_so_far[current] + 1  # 모든 간선 비용 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, end)
                    heapq.heappush(frontier, (priority, neighbor))
                    parent[neighbor] = current

        # frontier 내 좌표들
        queued = {pos for _, pos in frontier}

        draw_grid(grid, cost_so_far, current, [], start, end, queued)
        pygame.display.update()
        clock.tick(60)

    # 경로 추적
    path = []
    node = end
    while node in parent:
        path.append(node)
        node = parent[node]
    path.reverse()

    return path, cost_so_far, queued

def main():
    start = (GRID_HEIGHT // 2, GRID_WIDTH // 2)
    end = (GRID_HEIGHT // 2 - 1, GRID_WIDTH - 3)

    grid = create_grid()
    path, cost_so_far, queued = a_star(grid, start, end)

    for i, node in enumerate(path):
        draw_grid(grid, cost_so_far, node, path[:i+1], start, end, queued)
        pygame.display.update()
        clock.tick(20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

main()
