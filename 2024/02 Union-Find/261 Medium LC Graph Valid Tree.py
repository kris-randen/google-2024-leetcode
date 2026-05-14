"""

261. Graph Valid Tree
Medium
Topics
Companies
Hint
You have a graph of n nodes labeled from 0 to n - 1. You are given an integer n and a list of edges where edges[i] = [ai, bi] indicates that there is an undirected edge between nodes ai and bi in the graph.

Return true if the edges of the given graph make up a valid tree, and false otherwise.

Example 1:

Input: n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]
Output: true
Example 2:

Input: n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]
Output: false

Constraints:

1 <= n <= 2000
0 <= edges.length <= 5000
edges[i].length == 2
0 <= ai, bi < n
ai != bi
There are no self-loops or repeated edges.

Runtime 95 ms Beats 14.86%
Memory 18.60 MB Beats 19.20%

"""

class UnionFind:
    def __init__(self, n):
        self.id = [i for i in range(n)]
        self.comps = {i: {i} for i in range(n)}
        self.max = 1

    def size(self, p):
        return len(self.comps[p])

    def parent(self, i):
        return self.id[i]

    def is_root(self, i):
        return i == self.id[i]

    def not_root(self, i):
        return not self.is_root(i)

    def assign(self, i, p):
        self.id[i] = p

    def path(self, i):
        p = [i]
        while self.not_root(i):
            i = self.parent(i)
            p += [i]
        return p

    def compress(self, path):
        root = path[-1]
        for p in path: self.assign(p, root)
        return root

    def find(self, i):
        return self.compress(self.path(i))

    def roots(self, i, j):
        return self.find(i), self.find(j)

    def connected(self, i, j):
        p, q = self.roots(i, j)
        return p == q

    def union(self, i, j):
        p, q = self.roots(i, j)
        if not p == q: return self.join(p, q)

    def split(self, p, q):
        return (p, q) if self.size(p) > self.size(q) else (q, p)

    def merge(self, s, l):
        self.comps[l].update(self.comps.pop(s))

    def join(self, p, q):
        l, s = self.split(p, q)
        self.assign(s, l)
        self.merge(s, l)
        self.max = max(self.max, len(self.comps[l]))

    @property
    def count(self):
        return len(self.comps)


def valid_tree(n, edges):
    es = len(edges)
    if es != n - 1: return False
    uf = UnionFind(n)
    for u, v in edges:
        if uf.connected(u, v): return False
        uf.union(u, v)
    return True
