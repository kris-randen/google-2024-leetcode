"""

130. Surrounded Regions
Medium
Topics
Companies
You are given an m x n matrix board containing letters 'X' and 'O', capture regions that are surrounded:

Connect: A cell is connected to adjacent cells horizontally or vertically.
Region: To form a region connect every 'O' cell.
Surround: The region is surrounded with 'X' cells if you can connect the region with 'X' cells and none of the region cells are on the edge of the board.
A surrounded region is captured by replacing all 'O's with 'X's in the input matrix board.


Example 1:

Input: board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]

Output: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]

Explanation:

In the above diagram, the bottom region is not captured because it is on the edge of the board and cannot be surrounded.

Example 2:

Input: board = [["X"]]
Output: [["X"]]

Constraints:

m == board.length
n == board[i].length
1 <= m, n <= 200
board[i][j] is 'X' or 'O'.
Seen this question in a real interview before?
1/5
Yes
No
Accepted
742.3K
Submissions
1.8M
Acceptance Rate
40.1%

"""

from collections import defaultdict
from typing import Optional


class Point:
    def __init__(self, i, j):
        self.p = (i, j)

    @property
    def i(self):
        return self.p[0]

    @property
    def j(self):
        return self.p[1]

    def __iter__(self):
        yield self.i
        yield self.j

    def __eq__(self, other):
        return self.i == other.i and self.j == other.j

    def __hash__(self):
        return hash((self.i, self.j))

    def __repr__(self):
        return f"Point({self.i}, {self.j})"

    def up(self):
        return Point(self.i - 1, self.j)

    def dn(self):
        return Point(self.i + 1, self.j)

    def lt(self):
        return Point(self.i, self.j - 1)

    def rt(self):
        return Point(self.i, self.j + 1)

    def adj(self):
        return self.up(), self.dn(), self.lt(), self.rt()


def point(i, j):
    return Point(i, j)


class Board:
    def __init__(self, board):
        self.board = board
        self.m = len(board)
        self.n = len(board[0])

    def val(self, p: Point):
        return self.board[p.i][p.j]

    def mark(self, p: Point, val='X'):
        self.board[p.i][p.j] = val

    def flatten(self, p):
        return (p.i * self.n) + p.j

    def unflatten(self, k):
        return Point(k // self.n, k % self.n)

    def valid(self, p: Point):
        return 0 <= p.i < self.m and 0 <= p.j < self.n

    def ns(self, p: Point):
        return tuple(filter(self.valid, p.adj())) if self.is_flagged(p) else tuple()

    def ns_flagged(self, p: Point):
        return filter(self.is_flagged, self.ns(p))

    def ns_flagged_flat(self, p: Point):
        return set(map(self.flatten, self.ns_flagged(p)))

    def is_flagged(self, p, val='O'):
        return self.val(p) == val

    def flagged(self):
        return filter(self.is_flagged, self.points())

    def points(self):
        return (Point(i, j) for i in range(self.m) for j in range(self.n))

    def __iter__(self):
        return self.points()

    def boundary(self, p):
        return p.i == 0 or p.i == self.m - 1 or p.j == 0 or p.j == self.n - 1

    def graph(self):
        g = Graph(self.m * self.n, self)
        g.adj = dict(
            map(
                lambda p: (self.flatten(p),
                           self.ns_flagged_flat(p)),
                self.points()
            )
        )
        return g


class Graph:
    def __init__(self, V: int, board: Optional[Board] = None):
        self.V = V; self.board = board
        self.adj = {v: set() for v in range(self.V)}

    def boundary(self, v):
        return self.board.boundary(self.unflatten(v))

    def unflatten(self, v):
        return self.board.unflatten(v)

    def is_flagged(self, v):
        return self.board.is_flagged(self.unflatten(v))


class CC:
    def __init__(self, g):
        self.g = g
        self.marked = []
        self.cc = {}
        self.count = 0

    def connect(self):
        self.marked = [0 for _ in range(self.g.V)]
        self.cc = defaultdict(set)
        for v in range(self.g.V):
            if not self.marked[v]:
                self.dfs(self.g, v)
                self.count += 1

    def dfs(self, g, u):
        self.marked[u] = 1
        self.cc[self.count].add(u)
        for v in g.adj[u]:
            if not self.marked[v]:
                self.dfs(g, v)

    def is_linked(self, v):
        if not self.g.boundary(v): return True

    def is_surrounded(self, ind):
        cc = self.cc[ind]
        flag = True
        for v in cc:
            flag = flag and self.is_linked(v)
        return flag

    def surrounded(self):
        surr = []
        for ind in self.cc:
            if self.is_surrounded(ind):
                surr.append(ind)
        return surr

    def mark(self, val='X'):
        for ind in self.surrounded():
            for v in self.cc[ind]:
                p = self.g.unflatten(v)
                self.g.board.mark(p, val)


from toolz.curried import pipe, filter

def surrounded(b):
    comps, count, m, n = defaultdict(set), 0, len(b), len(b[0])

    def val(i, j):
        return b[i][j]

    def valid_ij(i, j):
        return 0 <= i < m and 0 <= j < n

    def flagged_ij(i, j, mark='O'):
        return val(i, j) == mark

    def valid(p):
        return valid_ij(p[0], p[1])

    def flagged(p):
        return flagged_ij(p[0], p[1])

    def adj(i, j):
        return (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)

    def nbrs(i, j):
        return pipe(
            adj(i, j),
            filter(valid),
            filter(flagged)
        )

    def cc(b):
        nonlocal count
        for i in range(m):
            for j in range(n):
                if flagged_ij(i, j):
                    dfs(b, i, j)
                    count += 1

    def dfs(b, i, j):
        b[i][j] = 'Y'
        for k, l in nbrs(i, j):
            if flagged_ij(k, l):
                dfs(b, k, l)
        comps[count].add((i, j))

    cc(b)
    return comps

if __name__ == '__main__':
    b = \
    [
        ["X","X","X","X"],
        ["X","O","O","X"],
        ["X","X","O","X"],
        ["X","O","X","X"]
    ]
    print(f"comps = {surrounded(b)}")
    print(b)