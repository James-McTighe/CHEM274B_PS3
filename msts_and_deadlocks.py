class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)] # this will end up being a list of lists, each index will be [u, (v, weight)]
    
    def add_edge(self, u, v, weight):
        """
        Edges are represented by having a tuple with the connected node and it's associated weight
        connected at the same index of the node
        """
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

class DisjointSet:
    def __init__(self, vertices):
        self.parent = list(range(vertices))
        self.rank = [0] * vertices

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, x, y):
        xroot = self.find(x)
        yroot = self.find(y)
        if self.rank[xroot] < self.rank[yroot]:
            self.parent[xroot] = yroot
        elif self.rank[xroot] > self.rank[yroot]:
            self.parent[yroot] = xroot
        else:
            self.parent[yroot] = xroot
            self.rank[xroot] += 1

class Solution:
    def kruskal_mst(self, graph : Graph):
        edges = []
        uf = DisjointSet(graph.V)

        for u in range(graph.V):
            for v, weight in graph.graph[u]:
                if u < v:  # Avoid duplicating edges
                    edges.append((weight, u, v))

        edges.sort()

        min_span_tree = []

        for weight, u, v in edges:
            if uf.find(u) != uf.find(v):
                uf.union(u,v)
                min_span_tree.append((u, v, weight))

        return min_span_tree


    def is_cyclic_util(self, graph : Graph, v, visited : list, parent):
        visited[v] = True
        for x in graph.graph[v]:
            if not visited[x]:
                if self.is_cyclic_util(graph, x, visited, v):
                    return True
            elif parent != x:
                return True
        return False

    def is_cyclic(self, graph : Graph) -> bool:
        visited = [False] * graph.V
        for i in range(graph.V):
            if not visited[i]:
                if self.is_cyclic_util(graph, i, visited, -1):
                    return True
        return False

    def detect_deadlock(self, graph : Graph):
        return self.is_cyclic(graph)