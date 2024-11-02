import pygame
import heapq
import sys
import time

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_edge(self, start, end, weight):
        if start not in self.adjacency_list:
            self.adjacency_list[start] = []
        if end not in self.adjacency_list:
            self.adjacency_list[end] = []
        self.adjacency_list[start].append((end, weight))

def dijkstra(graph, start, draw_callback):
    distances = {node: float('infinity') for node in graph.adjacency_list}
    distances[start] = 0
    priority_queue = [(0, start)]
    predecessors = {}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        draw_callback(distances, current_node)
        time.sleep(0.5)

        for neighbor, weight in graph.adjacency_list.get(current_node, []):
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node 
                heapq.heappush(priority_queue, (distance, neighbor))
                draw_callback(distances, neighbor)
                time.sleep(0.5)

    return distances, predecessors

def get_shortest_path(predecessors, start, target):
    path = []
    current = target
    while current != start:
        path.append(current)
        current = predecessors.get(current)
        if current is None:
            return []
    path.append(start)
    return path[::-1]

pygame.init()
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Animated Dijkstra's Algorithm with Shortest Path Highlight")
clock = pygame.time.Clock()

node_positions = {
    'A': (100, 100), 'B': (300, 100), 'C': (500, 100),
    'D': (700, 100), 'E': (900, 100), 'F': (200, 300),
    'G': (400, 300), 'H': (600, 300), 'I': (800, 300),
    'J': (150, 500), 'K': (350, 500), 'L': (550, 500),
    'M': (750, 500), 'N': (950, 500)
}

# Function to draw the graph with current distances and highlight path
def draw_graph(graph, distances, current_node=None, highlight_path=None):
    screen.fill((255, 255, 255))  # White background
    
    # Draw edges with weights
    for node, neighbors in graph.adjacency_list.items():
        x1, y1 = node_positions[node]
        for neighbor, weight in neighbors:
            x2, y2 = node_positions[neighbor]
            color = (0, 255, 0) if highlight_path and (node, neighbor) in highlight_path else (0, 0, 255)
            pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
            font = pygame.font.Font(None, 24)
            weight_text = font.render(str(weight), True, (0, 0, 0))
            screen.blit(weight_text, (mid_x, mid_y))

    for node, (x, y) in node_positions.items():
        color = (0, 255, 0) if node == current_node else (255, 0, 0)
        pygame.draw.circle(screen, color, (x, y), 20)
        font = pygame.font.Font(None, 24)
        text = font.render(node, True, (255, 255, 255))
        screen.blit(text, (x - 10, y - 10))

        distance_text = font.render(f"{distances.get(node, '∞')}", True, (0, 0, 0))
        screen.blit(distance_text, (x - 10, y + 25))

    pygame.display.flip()

def main():
    graph = Graph()

    graph.add_edge('A', 'B', 2)
    graph.add_edge('A', 'F', 4)
    graph.add_edge('B', 'C', 1)
    graph.add_edge('B', 'G', 3)
    graph.add_edge('C', 'D', 7)
    graph.add_edge('C', 'H', 6)
    graph.add_edge('D', 'E', 2)
    graph.add_edge('D', 'I', 5)
    graph.add_edge('E', 'I', 1)
    graph.add_edge('F', 'G', 2)
    graph.add_edge('F', 'J', 4)
    graph.add_edge('G', 'H', 3)
    graph.add_edge('G', 'K', 5)
    graph.add_edge('H', 'I', 2)
    graph.add_edge('H', 'L', 4)
    graph.add_edge('I', 'M', 6)
    graph.add_edge('J', 'K', 1)
    graph.add_edge('K', 'L', 2)
    graph.add_edge('L', 'M', 3)
    graph.add_edge('M', 'N', 2)

    start_node = 'A'
    target_node = 'N'

    def draw_callback(distances, current_node):
        draw_graph(graph, distances, current_node)

    distances, predecessors = dijkstra(graph, start_node, draw_callback)

    shortest_path = get_shortest_path(predecessors, start_node, target_node)
    highlight_edges = [(shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path)-1)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_graph(graph, distances, highlight_path=highlight_edges)
        clock.tick(60)

    pygame.quit()
    sys.exit()

main()
