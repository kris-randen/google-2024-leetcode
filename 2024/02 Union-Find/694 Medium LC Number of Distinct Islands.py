"""

694. Number of Distinct Islands
Medium
You are given an m x n binary matrix grid. An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.

An island is considered to be the same as another if and only if one island can be translated (and not rotated or reflected) to equal the other.

Return the number of distinct islands.

Example 1:

Input: grid = [[1,1,0,0,0],[1,1,0,0,0],[0,0,0,1,1],[0,0,0,1,1]]
Output: 1
Example 2:


Input: grid = [[1,1,0,1,1],[1,0,0,0,0],[0,0,0,0,1],[1,1,0,1,1]]
Output: 3


Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 50
grid[i][j] is either 0 or 1.

"""

from itertools import product
from typing import List


class UnionFind:
    def __init__(self, n=0):
        self.id = {i: i for i in range(n)}
        self.sz = {i: {i} for i in range(n)}

    def size(self, k):
        return len(self.sz[k])

    def add(self, k):
        self.id[k] = k; self.sz[k] = {k}

    def root(self, k):
        if k == self.id[k]: return k
        self.id[k] = self.root(self.id[k])
        return self.id[k]

    def find(self, p, q):
        return self.root(p) == self.root(q)

    def split(self, p, q):
        s, l = self.root(p), self.root(q)
        return (s, l) if self.size(s) < self.size(l) else (l, s)

    def union(self, p, q):
        if self.find(p, q): return
        s, l = self.split(p, q)
        self.id[s] = l
        self.sz[l].update(self.sz.pop(s))


def count(g):
    def flat(p):        return p[0] * n + p[1]
    def unflat(k):      return k // n, k % n
    def valid(p):       return 0 <= p[0] < m and 0 <= p[1] < n
    def fvalid(k):      return valid(unflat(k))
    def row(k):         return unflat(k)[0]
    def col(k):         return unflat(k)[1]

    def up(p):          return p[0] - 1, p[1]
    def dn(p):          return p[0] + 1, p[1]
    def lt(p):          return p[0], p[1] - 1
    def rt(p):          return p[0], p[1] + 1

    def fup(k):         return flat(up(unflat(k)))
    def fdn(k):         return flat(dn(unflat(k)))
    def flt(k):         return flat(lt(unflat(k)))
    def frt(k):         return flat(rt(unflat(k)))

    def adj(p):         return [up(p), dn(p), lt(p), rt(p)]
    def nbs(p):         return [nb for nb in adj(p) if valid(nb)]
    def fnbs(k):        return [flat(nb) for nb in nbs(unflat(k))]

    def origin(k):
        uislands = [unflat(l) for l in islands.sz[k]]
        r, c = min(uislands, key=lambda x: x[0])[0], min(uislands, key=lambda x: x[1])[1]
        return r, c

    def translate(p, rc):
        return tuple(sorted([(row(q) - rc[0], col(q) - rc[1]) for q in islands.sz[p]]))

    def translated():
        return {translate(p, origin(p)) for p in islands.sz}

    m, n = len(g), len(g[0])
    islands = UnionFind()

    for i, j in product(range(m), range(n)):
        if not g[i][j] == 1:    continue
        islands.add(k := flat((i, j)))
        ps = [l for l in fnbs(k) if l in islands.id]
        if not ps:              continue
        islands.union(k, ps[0])
        for p in ps: islands.union(p, ps[0])
    td = translated()
    return len(td)


class Solution:
    def numDistinctIslands(self, g: List[List[int]]) -> int:
        return count(g)
