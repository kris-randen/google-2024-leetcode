"""

323. Number of Connected Components in an Undirected Graph
Solved
Medium
Topics
Companies
You have a graph of n nodes. You are given an integer n and an array edges where edges[i] = [ai, bi] indicates that there is an edge between ai and bi in the graph.

Return the number of connected components in the graph.



Example 1:


Input: n = 5, edges = [[0,1],[1,2],[3,4]]
Output: 2
Example 2:


Input: n = 5, edges = [[0,1],[1,2],[2,3],[3,4]]
Output: 1


Constraints:

1 <= n <= 2000
1 <= edges.length <= 5000
edges[i].length == 2
0 <= ai <= bi < n
ai != bi
There are no repeated edges.

"""

from typing import List

class Graph:
    def __init__(self, n, es):
        self.adj = {i: set() for i in range(n)}
        self.n = n; self.adds(es)

    def add(self, e):
        self.adj[e[0]].add(e[1])
        self.adj[e[1]].add(e[0])

    def adds(self, es):
        for e in es: self.add(e)


def dfs(g):
    def visit(g, u):
        visited.add(u)
        for v in g.adj[u]:
            if v not in visited: visit(g, v)
        return 1

    visited = set()
    return sum(visit(g, v) for v in range(g.n) if v not in visited)


class UnionFind:
    def __init__(self, n, es):
        self.id = [i for i in range(n)]
        self.sz = {i: 1 for i in range(n)}
        self.es = es; self.connect()

    def size(self, r):
        return self.sz[r]

    def root(self, p):
        if p == self.id[p]: return p
        self.id[p] = self.root(self.id[p])
        return self.id[p]

    def find(self, p, q):
        return self.root(p) == self.root(q)

    def split(self, p, q):
        s, l = self.root(p), self.root(q)
        return (s, l) if self.size(s) < self.size(l) else (l, s)

    def union(self, p, q):
        if self.find(p, q): return
        s, l = self.split(p, q)
        self.id[s] = l
        self.sz[l] += self.sz.pop(s)

    def connect(self):
        for p, q in self.es: self.union(p, q)

    def count(self):
        return len(self.sz)

class Solution:
    def countComponents(self, n: int, es: List[List[int]]) -> int:
        return UnionFind(n, es).count()
