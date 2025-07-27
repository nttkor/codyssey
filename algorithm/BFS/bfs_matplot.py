import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import time

def bfs_visualize(graph, start):
    visited = set()
    queue = deque([start])
    order = []  # 방문 순서 기록

    pos = nx.spring_layout(graph)  # 노드 위치 자동 배치

    while queue:
        current = queue.popleft()
        if current not in visited:
            visited.add(current)
            order.append(current)
            
            # 그래프 그리기
            plt.clf()
            node_colors = ['skyblue' if node not in visited else 'orange' for node in graph.nodes()]
            nx.draw(graph, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=800, font_weight='bold')
            plt.title(f"BFS Step: Visiting {current}")
            plt.pause(1)  # 1초 대기
            
            for neighbor in graph.neighbors(current):
                if neighbor not in visited:
                    queue.append(neighbor)

    plt.show()

# 예시 그래프 만들기
G = nx.Graph()
edges = [
    ('A', 'B'), ('A', 'C'), 
    ('B', 'D'), ('C', 'E'), 
    ('D', 'F'), ('E', 'F')
]
G.add_edges_from(edges)

# BFS 시각화 실행
plt.ion()  # 인터랙티브 모드 on
bfs_visualize(G, 'A')
plt.ioff()  # 인터랙티브 모드 off
