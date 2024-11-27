"""



"""

from typing import List

def dfsc(g):
    def dfs(g, u):
        visited[u] = -1
        for v in g.adj[u]:
            if visited[v] == -1: return True
            elif not visited[v] and dfs(g, v): return True
        visited[u] = 1
        return False

    visited = {v: 0 for v in range(g.V)}

    for v in range(g.V):
        if visited[v] == 1: continue
        elif dfs(g, v): return True
    return False


from collections import defaultdict


class Graph:
    def __init__(self, V=0, es=None):
        self.V, self.es = V, es if es else None
        self.adj = defaultdict(set); self.connect()

    def add(self, e):
        self.adj[e[1]].add(e[0])

    def connect(self):
        if not self.es: return
        for e in self.es: self.add(e)


class Solution:
    def canFinish(self, V: int, es: List[List[int]]) -> bool:
        g = Graph(V, es)
        return not dfsc(g)