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
        """
        This function returns a list of edges contained within the MST.
        The basis by which this works is using a union-find structure.
        If two nodes don't share a parent, they'll be connected.
        The edges are sorted by their weight so they are added to the mst from smallest to largest
        The structure of the Graph object helps to implement this.
        Because the first for loop is graph.V, the number of edges added to the MST will only be V-1
        """

        edges = []
        uf = DisjointSet(graph.V)

        for u in range(graph.V):
            for v, weight in graph.graph[u]:
                if u != v:  # Avoid duplicating edges
                    edges.append((u, v, weight))

        edges.sort(key=lambda item: item[2]) #sorts the edges by their weight

        min_span_tree = []

        for u, v, weight in edges:
            if uf.find(u) != uf.find(v): # evaluates if the two nodes are connected in the same tree
                uf.union(u,v) # connects the nodes if they aren't already
                min_span_tree.append((u, v, weight)) # appends edge to result
                # This will prevent cyclical MSTs

        return min_span_tree


    def is_cyclic_util(self, graph : Graph, v, visited : list, parent):
        """
        This function is used to aid in the implementation of the below function.
        As the other function is working through each node, this function marks the node as visited.
        It will then determin if a cycle is present by iterating through all connected nodes.
        If it is able to go through all nodes without revisiting one, no cycle will be found and the function will return 'False'
        """
        visited[v] = True
        for x, weight in graph.graph[v]: # weight isn't used, it's just need to extract x from the graph, can't perform these operations with a tuple
            
            if not visited[x]: #recursivly calls nodes connected to v which haven't been visited using DFS
                if self.is_cyclic_util(graph, x, visited, v):
                    return True
                
            elif parent != x: # this means that the two nodes aren't a part of the same tree so a cycle would be impossible.
                return True

        return False

    def is_cyclic(self, graph : Graph) -> bool:
        """
        This function creates a list of nodes all marked 'False'
        It iterates through each node and detects if there is a cycle present anywhere in it's connected vertices
        If there is a cycle present it will return 'True'
        Otherwise the function will return 'False'
        """

        visited = [False] * graph.V
        for i in range(graph.V):
            if not visited[i]:
                if self.is_cyclic_util(graph, i, visited, -1):
                    return True
        return False

    def detect_deadlock(self, graph : Graph):
        return self.is_cyclic(graph)