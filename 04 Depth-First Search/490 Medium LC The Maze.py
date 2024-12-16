"""

490. The Maze
Solved
Medium
Topics
Companies
There is a ball in a maze with empty spaces (represented as 0) and walls (represented as 1). The ball can go through the empty spaces by rolling up, down, left or right, but it won't stop rolling until hitting a wall. When the ball stops, it could choose the next direction.

Given the m x n maze, the ball's start position and the destination, where start = [startrow, startcol] and destination = [destinationrow, destinationcol], return true if the ball can stop at the destination, otherwise return false.

You may assume that the borders of the maze are all walls (see examples).



Example 1:


Input: maze = [[0,0,1,0,0],[0,0,0,0,0],[0,0,0,1,0],[1,1,0,1,1],[0,0,0,0,0]], start = [0,4], destination = [4,4]
Output: true
Explanation: One possible way is : left -> down -> left -> down -> right -> down -> right.
Example 2:


Input: maze = [[0,0,1,0,0],[0,0,0,0,0],[0,0,0,1,0],[1,1,0,1,1],[0,0,0,0,0]], start = [0,4], destination = [3,2]
Output: false
Explanation: There is no way for the ball to stop at the destination. Notice that you can pass through the destination but you cannot stop there.
Example 3:

Input: maze = [[0,0,0,0,0],[1,1,0,0,1],[0,0,0,0,0],[0,1,0,0,1],[0,1,0,0,0]], start = [4,3], destination = [0,1]
Output: false


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

from typing import List


def solve(mz, st, dt):
    def val(p):
        return mz[p[0]][p[1]]

    def reached(p):
        return p[0] == dt[0] and p[1] == dt[1]

    def clear(p):
        return not val(p) == 1

    def visited(p):
        return val(p) == 2

    def mark(p):
        mz[p[0]][p[1]] = 2

    def inside(p):
        return (
                0 <= p[0] < m and
                0 <= p[1] < n
        )

    def valid(p):
        return inside(p) and clear(p)

    def invalid(p):
        return not valid(p)

    def l(p):
        return p[0], p[1] - 1

    def r(p):
        return p[0], p[1] + 1

    def u(p):
        return p[0] - 1, p[1]

    def d(p):
        return p[0] + 1, p[1]

    def lt(p):
        if invalid(p):  return r(p)
        return lt(l(p))

    def rt(p):
        if invalid(p):  return l(p)
        return rt(r(p))

    def up(p):
        if invalid(p):  return d(p)
        return up(u(p))

    def dn(p):
        if invalid(p):  return u(p)
        return dn(d(p))

    def dfs(p):
        if reached(p):  return True
        mark(p)
        if not visited(pl := lt(p)) and dfs(pl): return True
        if not visited(pr := rt(p)) and dfs(pr): return True
        if not visited(pu := up(p)) and dfs(pu): return True
        if not visited(pd := dn(p)) and dfs(pd): return True
        return False

    m, n = len(mz), len(mz[0])
    return dfs(st)


class Solution:
    def hasPath(self, mz: List[List[int]], st: List[int], dt: List[int]) -> bool:
        return solve(mz, st, dt)
