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

"""

class UnionFind2D:
    def __init__(self, board):
        self.board = board; self.m, self.n = len(board), len(board[0])
        self.id = [[(i,j) for j in range(self.n)] for i in range(self.m)]
        self.sz = [[1 for _ in range(self.n)] for _ in range(self.m)]
        self.count = self.m * self.n

    def get_val(self, p):
        return self.board[p[0]][p[1]]

    def set_val(self, p, a):
        self.board[p[0]][p[1]] = a

    def get_id(self, p):
        return self.id[p[0]][p[1]]

    def set_id(self, p, q):
        self.id[p[0]][p[1]] = q

    def get_size(self, p):
        return self.sz[p[0]][p[1]]

    def set_size(self, p, a):
        self.sz[p[0]][p[1]] = a

    def path(self, s):
        p = [s]
        while s != self.get_id(s):
            s = self.get_id(s)
            p.append(s)
        return p

    def compress(self, path):
        root = path[-1]
        for p in path: self.set_id(p, root)
        return root

    def find(self, p):
        return self.compress(self.path(p))

    def split(self, p, q):
        return (p, q) if self.get_size(p) > self.get_size(q) else (q, p)

    def union(self, p, q):
        r, s = self.find(p), self.find(q)
        if r == s: return
        self.union_roots(r, s)

    def union_roots(self, p, q):
        l, s = self.split(p, q)
        self.set_id(s, l)
        size_l, size_s = self.get_size(l), self.get_size(s)
        self.set_size(l, size_l + size_s)
        self.count -= 1

    def is_region(self, p):
        return self.get_val(p) == "O"

    def is_valid(self, p):
        return 0 <= p[0] < self.m and 0 <= p[1] < self.n

    def right(self, p):
        return p[0], p[1] + 1

    def left(self, p):
        return p[0], p[1] - 1

    def up(self, p):
        return p[0] - 1, p[1]

    def down(self, p):
        return p[0] + 1, p[1]

    def neighbors(self, p):
        return [self.left(p), self.right(p), self.up(p), self.down(p)]

    def valid_neighbors(self, p):
        return list(filter(self.is_valid, self.neighbors(p)))

    def connect(self):
        for i in range(self.m):
            for j in range(self.n):
                p = (i, j)
                if self.is_region(p):
                    nbrs = self.valid_neighbors(p)
                    for nbr in nbrs:
                        self.union(p, nbr)

    def capture(self):
        pass