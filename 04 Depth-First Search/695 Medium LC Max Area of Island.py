"""

695. Max Area of Island
Medium
You are given an m x n binary matrix grid. An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.

The area of an island is the number of cells with a value 1 in the island.

Return the maximum area of an island in grid. If there is no island, return 0.



Example 1:


Input: grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
Output: 6
Explanation: The answer is not 11, because the island must be connected 4-directionally.
Example 2:

Input: grid = [[0,0,0,0,0,0,0,0]]
Output: 0

Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 50
grid[i][j] is either 0 or 1.

"""

from itertools import product
from typing import List


def dfs_2D(g):
    def land(i, j):
        return g[i][j] == 1

    def bound(i, j):
        return 0 <= i < m and 0 <= j < n

    def valid(i, j):
        return bound(i, j) and land(i, j)

    def visit(i, j):
        if not valid(i, j): return
        visited[0] += 1
        g[i][j] = 2
        visit(i - 1, j)
        visit(i + 1, j)
        visit(i, j - 1)
        visit(i, j + 1)

    m, n, visited, maxs = len(g), len(g[0]), [0], float('-inf')
    for i, j in product(range(m), range(n)):
        if g[i][j] == 2: continue
        start = visited[0]
        visit(i, j)
        end = visited[0]
        maxs = max(maxs, end - start)
    return maxs


class DynamicUnionFind:
    def __init__(self, n=0):
        self.id = {i: i for i in range(n)}
        self.sz = {i: 1 for i in range(n)}

    def add(self, p):
        if p in self.id: return
        self.id[p] = p; self.sz[p] = 1

    def size(self, r):
        return self.sz[r]

    def root(self, p):
        if not p == self.id[p]:
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


def islands(g):
    def flat(p):
        return p[0] * n + p[1]

    def unflat(k):
        return k // n, k % n

    def valid(p):
        return 0 <= p[0] < m and 0 <= p[1] < n

    def land(p):
        return g[p[0]][p[1]] == 1

    def lvalid(p):
        return valid(p) and land(p)

    def up(p):
        return p[0] - 1, p[1]

    def dn(p):
        return p[0] + 1, p[1]

    def lt(p):
        return p[0], p[1] - 1

    def rt(p):
        return p[0], p[1] + 1

    def adj(p):
        return p, up(p), dn(p), lt(p), rt(p)

    def nbs(p):
        return (nb for nb in adj(p) if lvalid(nb))

    def fns(k):
        return (flat(nb) for nb in nbs(unflat(k)))

    m, n, uf = len(g), len(g[0]), DynamicUnionFind()
    for i, j in product(range(m), range(n)):
        if not land(p := (i, j)): continue
        uf.add(k := flat(p))
        for fb in fns(k):
            uf.add(fb)
            uf.union(k, fb)

    return max(uf.sz.values()) if uf.sz else 0


class Solution:
    def maxAreaOfIsland(self, g: List[List[int]]) -> int:
        # return dfs_2D(g)
        return islands(g)
