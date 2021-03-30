from collections import deque


class Graph(object):
    # A graph is represented as a map:
    # Key: Name of the vertex.
    # Value: Set of its neighbours and their respective distance.

    #E.g: edges = {"a" : [("b",2), ("c",3)], "b": [("c",5)]}

    def __init__(self, edges={}):
        """ initialize graph with given dictionay and coordinates.
        """
        self.edges = edges
        self.vertices = self.get_vertices()

    def get_vertices(self):
        result = set()
        for e in self.edges:
            result.add(e)
            for i in self.edges[e]:
                result.add(i[0])

        return result

    def get_edges(self):
        s = []
        for e in self.edges:
            for i in self.edges[e]:
                s.append(str(e) + " -> " + str(i[0]) + ", cost = " + str(i[1]))

        return '\n'.join(s)

    def __str__(self):
        return "Vetices: " + str(self.vertices) + "\nEdges:\n" + self.get_edges()

    def add_vertex(self, vertex):
        if vertex in self.vertices:
            return
        self.vertices.add(vertex)

    def add_edge(self, src, dest, cost=1):
        if src not in self.vertices:
            return
        if src not in self.edges:
            self.edges[src] = []
        if dest not in self.vertices:
            self.vertices.add(dest)
        self.edges[src].append((dest, cost))

    def get_neighbours(self, vertex):
        if vertex not in self.vertices:
            print("Error: Vertex does not exist!\n")
            return []
        if vertex not in self.edges:
            return []
        return self.edges[vertex]

    def remove_vertex(self, vertex):
        if vertex in self.vertices:
            self.vertices.remove(vertex)
        if vertex in self.edges:
            self.edges.pop(vertex)
        for e in self.edges:
            for i in self.edges[e]:
                if i[0] == vertex:
                    self.edges[e].remove(i)

    def remove_edge(self, src, dest):
        if src not in self.edges:
            return
        for e in self.edges[src]:
            if e[0] == dest:
                self.edges[src].remove(e)

    def dfs_traversal(self, src, visited=[]):
        print(src)
        for node in self.get_neighbours(src):
            if (node[0] not in visited):
                visited.append(node[0])
                self.dfs_traversal(node[0], visited)

    # performs a dfs search and returns the path
    def dfs(self, src, des):
        stack = [(src, [src])]
        visited = set()
        visited_ordered = [src]
        while stack:
            (vertex, path) = stack.pop()
            if vertex not in visited:
                if vertex == des:
                    return [path, visited_ordered]
                visited.add(vertex)
                visited_ordered.append(vertex)
                for node in self.get_neighbours(vertex):
                    stack.append((node[0], path + [node[0]]))

        print("No path has been found")
        return None

    # performs bfs search and returns the path
    def bfs(self, src, des):
        queue = [(src, [src])]
        visited = set()
        visited_ordered = [src]

        while queue:
            (vertex, path) = queue.pop(0)
            if vertex not in visited:
                if vertex == des:
                    return [path, visited_ordered]
                visited.add(vertex)
                visited_ordered.append(vertex)
                for (node, cost) in self.get_neighbours(vertex):
                    queue.append((node, path + [node]))

        print("No path has been found")
        return None

    def search(self, src, dest, heuristic):
        if src not in self.vertices or dest not in self.vertices:
            return None

        inf = float('inf')

        # distance to source = 0; distance to rest nodes = infinity
        dist = {vertex: inf for vertex in self.vertices}
        dist[src] = 0
        # initialize previous:
        prev = {vertex: None for vertex in self.vertices}
        # neighbours of each vertex:
        neighbours = {vertex: self.get_neighbours(
            vertex) for vertex in self.vertices}

        # set of visited nodes
        visited = set()
        visited.add(src)
        visited_ordered = [src]
        q = [src]

        while q:
            next = min(q, key=heuristic(dist))
            # remove element with shortest distance
            q.remove(next)
            # if we reached destination or smallest distance is infinite then break
            if next == dest:
                break

            for v, cost in neighbours[next]:
                if v not in visited:
                    visited.add(v)
                    visited_ordered.append(v)
                    q.append(v)
                    new_dist = dist[next] + cost
                    if new_dist < dist[v]:
                        dist[v] = new_dist
                        prev[v] = next

            if len(q) == 0:
                print("Cannot reach destination!")
                return ""

        # build the path
        path = deque()

        while prev[dest]:
            path.appendleft(dest)
            dest = prev[dest]

        # add source to beginning of the path
        path.appendleft(src)

        #print("The shortest path is: " + " -> ".join(path) + "\ncost = "+ str(dist[next]))
        return [path, visited_ordered]

    def dijkstra(self, src, dest):
        def heuristic(dist):
            def h(v):
                return dist[v]
            return h
        return self.search(src, dest, heuristic)

    def a_star(self, src, dest, distances):
        def heuristic(dist):
            def h(v):
                return dist[v] + distances[v]
            return h
        return self.search(src, dest, heuristic)

    def greedy_BFS(self, src, dest, distances):
        def heuristic(dist):
            def h(v):
                return distances[v]
            return h
        return self.search(src, dest, heuristic)

#####################################################################################################################


g = Graph({"a": [("b", 7), ("c", 9), ("f", 14)], "b":  [("c", 10),
                                                        ("d", 15)], "c": [("d", 11), ("f", 2), ("x", 9)],  "d": [("e", 6)],
           "e": [("f", 9)]})

# print(g.get_neighbours("a"))
#print(g.dfs("a", "e"))
