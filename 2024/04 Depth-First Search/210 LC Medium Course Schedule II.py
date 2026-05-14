"""



"""

from typing import List
from collections import defaultdict, deque


class Graph:
    def __init__(self, V=0, es=None):
        self.V, self.Vs, self.es = V, range(V), es if es else []
        self.adj = defaultdict(set); self.connect()

    def add(self, e):
        self.adj[e[1]].add(e[0])

    def connect(self):
        if not self.es: return
        for e in self.es: self.add(e)


def torder(g):
    def dfs(g, u):
        visited.add(u)
        for v in g.adj[u]:
            if v not in visited: dfs(g, v)
        order.appendleft(u)

    visited = set(); order = deque()
    for v in g.Vs:
        if v not in visited: dfs(g, v)
    return order


def cycle(g):
    def dfs(g, u):
        visited[u] = -1
        for v in g.adj[u]:
            if visited[v] == -1:
                return True
            elif not visited[v] and dfs(g, v):
                return True
        visited[u] = 1
        return False

    visited = {v: 0 for v in g.Vs}
    for v in g.Vs:
        if visited[v] == 1:
            continue
        elif dfs(g, v):
            return True
    return False


def order(V, es):
    if cycle(g := Graph(V, es)): return []
    return torder(g)


class Solution:
    def findOrder(self, V: int, es: List[List[int]]) -> List[int]:
        return list(order(V, es))