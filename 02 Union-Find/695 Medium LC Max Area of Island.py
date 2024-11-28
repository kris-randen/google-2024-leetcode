"""

695. Max Area of Island
Solved
Medium
Topics
Companies
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
Seen this question in a real interview before?
1/5
Yes
No
Accepted
892.7K
Submissions
1.2M
Acceptance Rate
72.3%

Runtime 230 ms Beats 5.02%
Memory 18.93 MB Beats 5.04%

"""


class UnionFind:
    def __init__(self, n):
        self.id = [i for i in range(n)]; self.max = 1
        self.comps = {i: {i} for i in range(n)}

    @property
    def count(self):
        return len(self.comps)

    def size(self, p):
        return len(self.comps[p])

    def is_greater(self, p, q):
        return self.size(p) > self.size(q)

    def merge(self, s, l):
        self.comps[l].update(self.comps.pop(s))

    def parent(self, i):
        return self.id[i]

    def assign(self, i, p):
        self.id[i] = p

    def is_root(self, i):
        return i == self.id[i]

    def is_not_root(self, i):
        return not self.is_root(i)

    def path(self, i):
        p = [i]
        while not i == self.parent(i):
            i = self.parent(i)
            p += [i]
        return p

    def compress(self, path):
        root = path[-1]
        for p in path: self.assign(p, root)
        return root

    def find(self, i):
        return self.compress(self.path(i))

    def split(self, p, q):
        return (p, q) if self.is_greater(p, q) else (q, p)

    def union(self, i, j):
        p, q = self.find(i), self.find(j)
        if not p == q: self.join(p, q)

    def join(self, p, q):
        l, s = self.split(p, q)
        self.assign(s, l)
        self.merge(s, l)
        self.max = max(self.max, self.size(l))


def flatten(i, j, m, n):
    return (i * n) + j


def project(l, m, n):
    return divmod(l, m)


def right(p):
    return p[0], p[1] + 1


def left(p):
    return p[0], p[1] - 1


def down(p):
    return p[0] + 1, p[1]


def up(p):
    return p[0] - 1, p[1]


def neighbors(p):
    return left(p), right(p), up(p), down(p)


def valid(p, m, n):
    return 0 <= p[0] < m and 0 <= p[1] < n


def land(p, m, n, grid):
    assert valid(p, m, n)
    return grid[p[0]][p[1]] == 1


def valid_and_land(p, m, n, grid):
    return valid(p, m, n) and land(p, m, n, grid)


def valid_neighbors(p, m, n, grid):
    return filter(lambda q: valid_and_land(q, m, n, grid), neighbors(p))


def max_area_of_island(grid):
    if not grid or not grid[0]: return 0
    m, n = len(grid), len(grid[0]); edges = []; count = 0
    for i in range(m):
        for j in range(n):
            l = flatten(i, j, m, n)
            if grid[i][j] == 1:
                count += 1
                nbrs = valid_neighbors((i, j), m, n, grid)
                for nbr in nbrs:
                    s = flatten(nbr[0], nbr[1], m, n)
                    edges.append((l, s))
    uf = UnionFind(m * n)
    for u, v in edges:
        uf.union(u, v)
    return uf.max if count > 0 else 0


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

