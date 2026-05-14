"""

547. Number of Provinces
Solved
Medium
Topics
Companies
There are n cities. Some of them are connected, while some are not. If city a is connected directly with city b, and city b is connected directly with city c, then city a is connected indirectly with city c.

A province is a group of directly or indirectly connected cities and no other cities outside of the group.

You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city and the jth city are directly connected, and isConnected[i][j] = 0 otherwise.

Return the total number of provinces.



Example 1:


Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
Output: 2
Example 2:


Input: isConnected = [[1,0,0],[0,1,0],[0,0,1]]
Output: 3


Constraints:

1 <= n <= 200
n == isConnected.length
n == isConnected[i].length
isConnected[i][j] is 1 or 0.
isConnected[i][i] == 1
isConnected[i][j] == isConnected[j][i]

Runtime 221 ms Beats 8.83%
Memory 17.27 MB Beats 70.38%

"""


class UnionFinds:
    def __init__(self, n):
        self.id = [i for i in range(n)]
        self.comps = {i: {i} for i in range(n)}
        self.max = 1

    @property
    def count(self):
        return len(self.comps)

    def size(self, i):
        return len(self.comps[i])

    def parent(self, i):
        return self.id[i]

    def is_root(self, i):
        return i == self.parent(i)

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

    def union(self, i, j):
        p, q = self.find(i), self.find(j)
        if p == q: return
        self.join(p, q)

    def split(self, p, q):
        return (p, q) if self.size(p) > self.size(q) else (q, p)

    def merge(self, s, l):
        self.comps[l] = self.comps[l].union(self.comps.pop(s))

    def join(self, p, q):
        l, s = self.split(p, q)
        self.assign(s, l)
        self.merge(s, l)
        self.max = max(self.max, len(self.comps[l]))

def province(isConnected):
    n = len(isConnected)
    uf = UnionFinds(n)
    for i in range(n):
        for j in range(n):
            if isConnected[i][j]:
                uf.union(i, j)
    return uf.count

# 20241130 30th Nov 2024 Re-solved.

class UnionFind:
    def __init__(self, n):
        self.id = [i for i in range(n)]
        self.sz = {i: 1 for i in range(n)}

    def root(self, p):
        if not p == self.id[p]:
            self.id[p] = self.root(self.id[p])
        return self.id[p]

    def find(self, p, q):
        return self.root(p) == self.root(q)

    def split(self, p, q):
        s, l = self.root(p), self.root(q)
        return (s, l) if self.sz[s] < self.sz[l] else (l, s)

    def union(self, p, q):
        if self.find(p, q): return
        s, l = self.split(p, q)
        self.id[s] = l
        self.sz[l] += self.sz.pop(s)

    def count(self):
        return len(self.sz)


def provinces(rs):
    def nbs(v):
        return (w for w, c in enumerate(rs[v]) if c == 1)

    uf = UnionFind(n := len(rs))
    for u in range(n):
        for v in nbs(u):
            uf.union(u, v)

    return uf.count()