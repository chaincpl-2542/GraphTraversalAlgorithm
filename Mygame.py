import pygame
import sys
from collections import deque

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Graph Traversal in Rooted Tree Structure")
clock = pygame.time.Clock()

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_edge(self, start, end, weight=1):
        if start not in self.adjacency_list:
            self.adjacency_list[start] = []
        self.adjacency_list[start].append((end, weight))

def dfs(graph, start, visited=None, visited_order=None):
    if visited is None:
        visited = set()
    if visited_order is None:
        visited_order = []

    visited.add(start)
    visited_order.append(start)

    for neighbor, _ in graph.adjacency_list.get(start, []):
        if neighbor not in visited:
            dfs(graph, neighbor, visited, visited_order)

    return visited_order

def bfs(graph, start):
    visited = set()
    visited_order = []
    queue = deque([start])

    while queue:
        current = queue.popleft()
        if current not in visited:
            visited.add(current)
            visited_order.append(current)
            for neighbor, _ in graph.adjacency_list.get(current, []):
                if neighbor not in visited:
                    queue.append(neighbor)

    return visited_order

def build_tree_positions(graph, root, x, y, x_offset, y_offset, positions, level=0):
    positions[root] = (x, y)
    children = graph.adjacency_list.get(root, [])

    for i, (child, _) in enumerate(children):
        new_x = x + (i - (len(children) - 1) / 2) * x_offset
        new_y = y + y_offset
        build_tree_positions(graph, child, new_x, new_y, x_offset / 2, y_offset, positions, level + 1)

def draw_tree(graph, positions, visited):
    screen.fill((255, 255, 255))  

    for node, edges in graph.adjacency_list.items():
        x, y = positions[node]
        for neighbor, _ in edges:
            nx, ny = positions[neighbor]
            pygame.draw.line(screen, (0, 0, 255), (x, y), (nx, ny), 2)

    for node, (x, y) in positions.items():
        color = (0, 255, 0) if node in visited else (0, 0, 0)
        pygame.draw.circle(screen, color, (int(x), int(y)), 20)
        font = pygame.font.Font(None, 24)
        text = font.render(node, True, (255, 255, 255))
        screen.blit(text, (x - 10, y - 10))

    pygame.display.flip()

def main():

    graph = Graph()
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('B', 'D')
    graph.add_edge('B', 'E')
    graph.add_edge('C', 'F')
    graph.add_edge('C', 'G')
    graph.add_edge('D', 'H')
    graph.add_edge('D', 'I')
    graph.add_edge('E', 'J')
    graph.add_edge('E', 'K')
    graph.add_edge('F', 'L')
    graph.add_edge('F', 'M')
    graph.add_edge('G', 'N')
    graph.add_edge('G', 'O')

    root = 'A'
    positions = {}
    build_tree_positions(graph, root, width // 2, 50, 200, 80, positions) 
    traversal_started = False
    visited_order = []
    visited = set()
    index = 0

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_q and not traversal_started:
                    visited_order = dfs(graph, root)
                    traversal_started = True
                    visited.clear()
                    index = 0
                    print("Depth First Search")

                elif event.key == pygame.K_w and not traversal_started:
                    visited_order = bfs(graph, root)
                    traversal_started = True
                    visited.clear()
                    index = 0
                    print("Breadth First Search")

        if traversal_started and index < len(visited_order):
            visited.add(visited_order[index])
            index += 1
        elif index >= len(visited_order):
            traversal_started = False

        draw_tree(graph, positions, visited)
        clock.tick(1)

    pygame.quit()
    sys.exit()

main()
