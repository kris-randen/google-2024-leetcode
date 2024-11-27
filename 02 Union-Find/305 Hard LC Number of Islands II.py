"""

305. Number of Islands II
Solved
Hard
Topics
Companies
You are given an empty 2D binary grid grid of size m x n. The grid represents a map where 0's represent water and 1's represent land. Initially, all the cells of grid are water cells (i.e., all the cells are 0's).

We may perform an add land operation which turns the water at position into a land. You are given an array positions where positions[i] = [ri, ci] is the position (ri, ci) at which we should operate the ith operation.

Return an array of integers answer where answer[i] is the number of islands after turning the cell (ri, ci) into a land.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.



Example 1:


Input: m = 3, n = 3, positions = [[0,0],[0,1],[1,2],[2,1]]
Output: [1,1,2,3]
Explanation:
Initially, the 2d grid is filled with water.
- Operation #1: addLand(0, 0) turns the water at grid[0][0] into a land. We have 1 island.
- Operation #2: addLand(0, 1) turns the water at grid[0][1] into a land. We still have 1 island.
- Operation #3: addLand(1, 2) turns the water at grid[1][2] into a land. We have 2 islands.
- Operation #4: addLand(2, 1) turns the water at grid[2][1] into a land. We have 3 islands.
Example 2:

Input: m = 1, n = 1, positions = [[0,0]]
Output: [1]


Constraints:

1 <= m, n, positions.length <= 104
1 <= m * n <= 104
positions[i].length == 2
0 <= ri < m
0 <= ci < n


Follow up: Could you solve it in time complexity O(k log(mn)), where k == positions.length?

"""

class UnionFind:
    def __init__(self, n):
        self.id = [i for i in range(n)]
        self.cp = {i: {i} for i in range(n)}

    def size(self, i):
        return len(self.cp[i])

    def root(self, i):
        if i == self.id[i]: return i
        self.id[i] = self.root(self.id[i])
        return self.id[i]

    def find(self, i, j):
        return self.root(i) == self.root(j)

    def split(self, i, j):
        p, q = self.root(i), self.root(j)
        return (p, q) if self.size(p) < self.size(q) else (q, p)

    def union(self, i, j):
        if self.find(i, j): return
        s, l = self.split(i, j); self.id[s] = l
        self.cp[l].update(self.cp.pop(s))


class DynamicUnionFind:
    def __init__(self, n=0):
        self.id = {i: i for i in range(n)}
        self.cp = {i: {i} for i in range(n)}

    def add(self, k):
        self.id[k] = k; self.cp[k] = {k}

    def size(self, k):
        return len(self.cp[k])

    def root(self, k):
        if k == self.id[k]: return k
        self.id[k] = self.root(self.id[k])
        return self.id[k]

    def split(self, p, q):
        r, s = self.root(p), self.root(q)
        return (r, s) if self.size(r) < self.size(s) else (s, r)

    def find(self, p, q):
        return self.root(p) == self.root(q)

    def union(self, p, q):
        if self.find(p, q): return
        s, l = self.split(p, q)
        self.id[s] = l
        self.cp[l].update(self.cp.pop(s))


def islands(m, n, ps):
    def flat(p):        return p[0] * n + p[1]
    def unflat(k):      return k // n, k % n
    def up(p):          return p[0] - 1, p[1]
    def dn(p):          return p[0] + 1, p[1]
    def lt(p):          return p[0], p[1] - 1
    def rt(p):          return p[0], p[1] + 1
    def fup(k):         return flat(up(unflat(k)))
    def fdn(k):         return flat(dn(unflat(k)))
    def flt(k):         return flat(lt(unflat(k)))
    def frt(k):         return flat(rt(unflat(k)))
    def valid(p):       return 0 <= p[0] < m and 0 <= p[1] < n
    def fvalid(k):      return valid(unflat(k))
    def near(p):        return [up(p), dn(p), lt(p), rt(p)]
    def nbs(p):         return [nb for nb in near(p) if valid(nb)]
    def fnbs(k):        return [flat(nb) for nb in nbs(unflat(k))]

    uf = DynamicUnionFind(); islands = []
    for i, p in enumerate(ps):
        uf.add(k := flat(p))
        adj = [fnb for fnb in fnbs(k) if fnb in uf.id]

        # if adj is empty append number of cps to islands
        if not adj:    islands.append(len(uf.cp)); continue

        # otherwise union k with any of the adj and union each adj to adj[0]
        uf.union(k, adj[0])
        for l in adj[1:]: uf.union(l, adj[0])
        islands.append(len(uf.cp))

    return islands