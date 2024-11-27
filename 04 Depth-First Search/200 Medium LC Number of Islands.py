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


Constraints:

m == grid.length
n == grid[i].length
1 <= m, n <= 300
grid[i][j] is '0' or '1'.
Seen this question in a real interview before?
1/5
Yes
No
Accepted
2.8M
Submissions
4.7M
Acceptance Rate
59.9%

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