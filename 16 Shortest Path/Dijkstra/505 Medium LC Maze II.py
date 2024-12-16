"""

505. The Maze II
Medium
Topics
Companies
There is a ball in a maze with empty spaces (represented as 0) and walls (represented as 1). The ball can go through the empty spaces by rolling up, down, left or right, but it won't stop rolling until hitting a wall. When the ball stops, it could choose the next direction.

Given the m x n maze, the ball's start position and the destination, where start = [startrow, startcol] and destination = [destinationrow, destinationcol], return the shortest distance for the ball to stop at the destination. If the ball cannot stop at destination, return -1.

The distance is the number of empty spaces traveled by the ball from the start position (excluded) to the destination (included).

You may assume that the borders of the maze are all walls (see examples).

 

Example 1:


Input: maze = [[0,0,1,0,0],[0,0,0,0,0],[0,0,0,1,0],[1,1,0,1,1],[0,0,0,0,0]], start = [0,4], destination = [4,4]
Output: 12
Explanation: One possible way is : left -> down -> left -> down -> right -> down -> right.
The length of the path is 1 + 1 + 3 + 1 + 2 + 2 + 2 = 12.
Example 2:


Input: maze = [[0,0,1,0,0],[0,0,0,0,0],[0,0,0,1,0],[1,1,0,1,1],[0,0,0,0,0]], start = [0,4], destination = [3,2]
Output: -1
Explanation: There is no way for the ball to stop at the destination. Notice that you can pass through the destination but you cannot stop there.
Example 3:

Input: maze = [[0,0,0,0,0],[1,1,0,0,1],[0,0,0,0,0],[0,1,0,0,1],[0,1,0,0,0]], start = [4,3], destination = [0,1]
Output: -1
 

Constraints:

m == maze.length
n == maze[i].length
1 <= m, n <= 100
maze[i][j] is 0 or 1.
start.length == 2
destination.length == 2
0 <= startrow, destinationrow < m
0 <= startcol, destinationcol < n
Both the ball and the destination exist in an empty space, and they will not be in the same position initially.
The maze contains at least 2 empty spaces.

"""



class Graph:
    def __init__(self, mz):
        self.m, self.n = len(mz), len(mz[0])
        self.V = self.m * self.n; self.mz = mz
        self.adj = {}; self.connect()

    def flat(self, p):          return p[0] * n + p[1]
    def unflat(self, k):        return k // n, k % n
    def val(self, p):           return self.mz[p[0]][p[1]]
    def fval(self, k):          return self.val(self.unflat(k))
    def clear(self, p):         return not self.val(p) == 1
    def inside(self, p):        return 0 <= p[0] < self.m and 0 <= p[1] < self.n
    def valid(self, p):         return self.inside(p) and self.clear(p)
    def l(self, p):             return p[0], p[1] - 1
    def r(self, p):             return p[0], p[1] + 1
    def u(self, p):             return p[0] - 1, p[1]
    def d(self, p):             return p[0] + 1, p[1]
    def lt(self, p, s):
        if not valid(p):        return r(p), s - 1
        return self.lt(self.l(p), s + 1)
    def rt(self, p, s):
        if not valid(p):        return l(p), s - 1
        return self.rt(self.r(p), s + 1)
    def up(self, p, s):
        if not valid(p):        return d(p), s - 1
        return self.up(self.u(p), s + 1)
    def dn(self, p, s):
        if not valid(p):        return u(p), s - 1
        return self.dn(self.d(p), s + 1)
    def flt(self, k):           return self.lt(self.unflat(k), 0)
    def frt(self, k):           return self.rt(self.unflat(k), 0)
    def fup(self, k):           return self.up(self.unflat(k), 0)
    def fdn(self, k):           return self.dn(self.unflat(k), 0)
    def join(self, k):
        if not (pl := self.flt(k)) == (k, 0): self.adj[k][pl[0]] = pl[1]
        if not (pr := self.frt(k)) == (k, 0): self.adj[k][pr[0]] = pr[1]
        if not (pu := self.fup(k)) == (k, 0): self.adj[k][pu[0]] = pu[1]
        if not (pd := self.fdn(k)) == (k, 0): self.adj[k][pd[0]] = pd[1]
    def connect(self):
        for k in range(self.V): self.join(k)

def dijkstra(g, s, t):
    































