from collections import deque
import pygame
import Graph as graph
import math

pygame.init()


class grid(object):
    def __init__(self, w, h, rows):
        self.w = w
        self.h = h
        self.rows = rows
        self.s = self.h // rows
        self.cols = self.w // self.s
        self.graph = self.generate_graph()

    def draw_grid(self, surface):
        w = self.h // self.rows

        # horizontal:
        for i in range(self.rows + 1):
            pygame.draw.line(surface, (105, 105, 105),
                             (0, i*w), (self.w, i*w), 1)

        # vertical:
        i = 0
        while (i*w < self.w):
            pygame.draw.line(surface, (105, 105, 105),
                             (i*w, 0), (i*w, self.h), 2)
            i += 1

    def generate_graph(self):
        # geneates a graph object representing the grid.
        g = graph.Graph()
        num_cells = self.rows * self.cols
        for i in range(num_cells):
            g.add_vertex(str(i))

        for i in range(num_cells):
            if i // self.cols == (i+1) // self.cols:
                g.add_edge(str(i), str(i+1))
            if i-1 >= 0 and i // self.cols == (i-1) // self.w:
                g.add_edge(str(i), str(i-1))
            if i + self.cols < num_cells:
                g.add_edge(str(i), str(i + self.cols))
            if i - self.cols >= 0:
                g.add_edge(str(i), str(i - self.cols))

        return g

    def draw_vertex(self, window, vertex, color):
        (r, c) = (int(vertex) // self.cols, int(vertex) % self.cols)
        pygame.draw.rect(window, color, (c*self.s, r *
                                         self.s, self.s-0.5, self.s-0.5))

    def manhattanDistance(self, v1, v2):
        (r1, c1) = (int(v1) // self.cols, int(v1) % self.cols)
        (r2, c2) = (int(v2) // self.cols, int(v2) % self.cols)
        return abs(r1-r2) + abs(c1-c2)

    def computeDistances(self, goal):
        vertices = self.graph.get_vertices()
        map = dict()
        for v in vertices:
            map[v] = self.manhattanDistance(v, goal)
        return map


running = True
# window dimensions:
w = 1200
h = 900
num_rows = 30

window = pygame.display.set_mode((w, h))
window.fill((255, 255, 255))
pygame.display.set_caption("Path Finder")
grid = grid(w, h, num_rows)
grph = grid.graph


finished = False
config = False

start = -1
end = -1

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    grid.draw_grid(window)
    pygame.display.update()
    mouse = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()

    if not config:
        if start == -1 or end == -1:
            if mouse[0]:
                (x, y) = pygame.mouse.get_pos()
                if x >= 0 and x < grid.w and y >= 0 and y < grid.h:
                    vertex = str((y // grid.s) * grid.cols + (x // grid.s))
                    grid.draw_vertex(window, vertex, (255, 0, 0))

                    pygame.display.update()

                if start == -1:
                    start = vertex
                elif vertex != start:
                    end = vertex

        else:
            if mouse[0]:
                (x, y) = pygame.mouse.get_pos()
                if x >= 0 and x < grid.w and y >= 0 and y < grid.h:
                    vertex = str((y // grid.s) * grid.cols + (x // grid.s))
                    if vertex != start and vertex != end:
                        grid.draw_vertex(window, vertex, (100, 100, 100))
                        grph.remove_vertex(vertex)
            if keys[pygame.K_RETURN]:
                config = True

    if config and not finished:
        distances = grid.computeDistances(end)
        #path = grph.a_star(start,end, distances)
        path, order = grph.a_star(start, end, distances)

        if path:
            for vertex in order:
                if vertex != start and vertex != end:
                    grid.draw_vertex(window, vertex, (247, 247, 89))
                pygame.time.delay(50)
                pygame.display.update()
            for vertex in path:
                if vertex != start and vertex != end:
                    grid.draw_vertex(window, vertex, (115, 194, 4))
                pygame.time.delay(50)
                pygame.display.update()
            print("The cost of the shortest path is " + str(len(path)-1))
        else:
            print("No path has been found!")
        finished = True
