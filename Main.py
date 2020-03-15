from collections import deque
import pygame
import Graph as graph

pygame.init()

class grid(object):
    def __init__ (self, w, h, rows):
        self.w = w
        self.h = h
        self.rows = rows
        self.s = self.h // rows
        self.cols = self.w // self.s

    def draw_grid (self,surface):
        w = self.h // self.rows 

        #horizontal:
        for i in range (self.rows + 1):
           pygame.draw.line(surface,(105,105,105),(0,i*w), (self.w,i*w),2)
        
        #vertical:
        i = 0
        while (i*w < self.w):
            pygame.draw.line(surface,(105,105,105),(i*w,0), (i*w,self.h),2)
            i+=1


    def generate_graph(self):
        #geneates a graph object representing the grid.
        g = graph.Graph()
        num_cells = self.rows * self.cols
        for i in range (num_cells):
            g.add_vertex(str(i))

        for i in range (num_cells):
            if i // self.cols == (i+1) // self.cols:
                g.add_edge(str(i),str(i+1))
            if i-1 >= 0 and i // self.cols == (i-1) // self.w:
                g.add_edge(str(i),str(i-1))
            if i + self.cols < num_cells:
                g.add_edge(str(i),str(i + self.cols))
            if i - self.cols >= 0:
                g.add_edge(str(i),str(i - self.cols))

        return g

    def draw_vertex(self,window,vertex,color):
        (r,c) = (int(vertex) // self.cols, int(vertex) % self.cols)
        pygame.draw.rect(window, color, (c*self.s,r*self.s,self.s,self.s))


running = True
#window dimensions:
w = 1020
h = 600
num_rows = 30

window = pygame.display.set_mode((w,h))
window.fill((255,255,255))
pygame.display.set_caption("Path Finder")
grid = grid(w,h,num_rows)
grph = grid.generate_graph()


finished = False
config = False

start = -1
end = -1

while running:
    pygame.time.delay(120)
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
                (x,y) = pygame.mouse.get_pos()
                if x >= 0 and x < grid.w and y >= 0 and y < grid.h:
                    vertex = str((y // grid.s) * grid.cols + (x // grid.s))
                    grid.draw_vertex(window,vertex,(255,0,0))
                    pygame.display.update()
                
                if start == -1:
                    start = vertex
                elif vertex != start:
                    end = vertex
        else:
            if mouse[0]:
                (x,y) = pygame.mouse.get_pos()
                if x >= 0 and x < grid.w and y >= 0 and y < grid.h:
                    vertex = str((y // grid.s) * grid.cols + (x // grid.s))
                    if vertex != start and vertex != end:    
                        grid.draw_vertex(window,vertex,(0,0,0))
                        grph.remove_vertex(vertex)
            if keys[pygame.K_RETURN]:
                config = True


    if config and not finished:
        path = grph.dijkstra(start,end)
        
        if path:
            for vertex in path:
                if vertex != start and vertex != end:
                    grid.draw_vertex(window,vertex,(0,0,255))
                pygame.time.delay(60)
                pygame.display.update()
            print("The cost of the shortest path is " + str(len(path)-1))
        else:
            print("No path has been found!")
        finished = True

    
    

    
    


