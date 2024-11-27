"""

200. Number of Islands
Solved
Medium
Topics
Companies
Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.



Example 1:

Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1
Example 2:

Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3

"""


class Graph:
    def __init__(self, board):
        self.b = board; self.count = 0
        self.m, self.n = len(board), len(board[0])

    def valid(self, p):
        return 0 <= p[0] < self.m and 0 <= p[1] < self.n

    def cc(self):
        for i in range(self.m):
            for j in range(self.n):
                if self.b[i][j] == "1":
                    self.dfs((i, j))
                    self.count += 1
        return self.count

    def adj(self, p):
        return [(p[0] - 1, p[1]), (p[0] + 1, p[1]), (p[0], p[1] - 1), (p[0], p[1] + 1)]

    def land(self, p):
        return self.b[p[0]][p[1]] == "1"

    def nbrs(self, p):
        return filter(self.land, filter(self.valid, self.adj(p)))

    def dfs(self, p):
        self.b[p[0]][p[1]] = "2"
        for nbr in self.nbrs(p):
            self.dfs(nbr)


from itertools import product


def dfs(g):
    def valid(i, j):
        return 0 <= i < m and 0 <= j < n and g[i][j] == '1'

    def visit(i, j):
        if not valid(i, j): return 0
        g[i][j] = '2'
        visit(i - 1, j)
        visit(i + 1, j)
        visit(i, j - 1)
        visit(i, j + 1)
        return 1

    m, n = len(g), len(g[0])
    return sum(visit(i, j) for i, j in product(range(m), range(n)))


class DynamicUnionFind:
    def __init__(self, n=0):
        self.id = {i: i for i in range(n)}
        self.sz = {i: 1 for i in range(n)}

    def size(self, p):
        return self.sz[p]

    def count(self):
        return len(self.sz)

    def find(self, p, q):
        return self.root(p) == self.root(q)

    def add(self, p):
        if p in self.id: return
        self.id[p] = p
        self.sz[p] = 1

    def root(self, p):
        if p == self.id[p]: return p
        self.id[p] = self.root(self.id[p])
        return self.id[p]

    def split(self, p, q):
        s, l = self.root(p), self.root(q)
        return (s, l) if self.size(s) < self.size(l) else (l, s)

    def union(self, p, q):
        if self.find(p, q): return
        s, l = self.split(p, q)
        self.id[s] = l
        self.sz[l] += self.sz.pop(s)

def islands(g):
    def flat(p):
        return p[0] * n + p[1]

    def unflat(k):
        return k // n, k % n

    def valid(p):
        return 0 <= p[0] < m and 0 <= p[1] < n

    def land(p):
        return g[p[0]][p[1]] == '1'

    def fland(k):
        return land(unflat(k))

    def lvalid(p):
        return valid(p) and land(p)

    def flvalid(k):
        return lvalid(unflat(k))

    def fvalid(k):
        return valid(unflat(k))

    def up(p):
        return p[0] - 1, p[1]

    def dn(p):
        return p[0] + 1, p[1]

    def lt(p):
        return p[0], p[1] - 1

    def rt(p):
        return p[0], p[1] + 1

    def fu(k):
        return flat(up(unflat(k)))

    def fd(k):
        return flat(dn(unflat(k)))

    def fl(k):
        return flat(lt(unflat(k)))

    def fr(k):
        return flat(rt(unflat(k)))

    def adj(p):
        return p, up(p), dn(p), lt(p), rt(p)

    def nbs(p):
        return (nb for nb in adj(p) if lvalid(nb))

    def fns(k):
        return [flat(nb) for nb in nbs(unflat(k))]

    m, n = len(g), len(g[0])
    uf = DynamicUnionFind()
    for i, j in product(range(m), range(n)):
        if not land(p := (i, j)): continue
        uf.add(k := flat(p))
        for nb in fns(k):
            uf.add(nb)
            uf.union(k, nb)
    return uf.count()


