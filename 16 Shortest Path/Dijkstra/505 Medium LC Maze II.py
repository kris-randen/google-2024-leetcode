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

Runtime 2022 ms Beats 5.57%
Memory 23.65 MB Beats 5.18%

"""

from typing import List
from math import log, exp
from collections import defaultdict

class IndexHeap:
    def __init__(self, kvs=None, cmp=lambda x, y: x < y):
        self.kvs = kvs if kvs else {}
        self.pq = [None] + list(self.kvs.keys())
        self.qp = {v: i for i, v in enumerate(self.pq) if i >= 1}
        self.cmp = cmp; self.heapify()

    def __iter__(self):
        hs = IndexHeap(self.kvs, self.cmp)
        while hs: yield hs.pop()

    def __len__(self):          return len(self.pq) - 1
    def __bool__(self):         return len(self) > 0
    def sorted(self):           return list(self)

    def heapify(self):
        for p in reversed(range(1, len(self) // 2 + 1)): self.sink(p)
    def swim(self, c):
        while p := self.unbalup(c): c = self.swap(c, p)
    def sink(self, p):
        while c := self.unbaldn(p): p = self.swap(p, c)
    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]], self.qp[self.pq[j]] = i, j
        return j

    def unbalup(self, c):       return self.parent(c) if not self.balup(c) else None
    def unbaldn(self, p):       return self.child(p) if not self.baldn(p) else None
    def balup(self, c):         return self.pref(p := self.parent(c), c) == p
    def baldn(self, p):         return self.pref(c := self.child(p), p) == p
    def parent(self, c):        return self.valid(self.up(c))
    def child(self, p):         return self.pref(self.left(p), self.right(p))
    def left(self, p):          return self.valid(self.lt(p))
    def right(self, p):         return self.valid(self.rt(p))
    def up(self, i):            return i // 2
    def lt(self, i):            return i * 2
    def rt(self, i):            return i * 2 + 1
    def valid(self, i):         return i if self.isval(i) else None
    def isval(self, i):         return 1 <= i <= len(self)
    def prior(self, i, j):      return i if self.cmp(self.val(i), self.val(j)) else j
    def val(self, i):           return self.kvs[self.pq[i]]
    
    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j

    def peek(self):
        return self.pq[1] if self else None
    def pop(self):
        if (top := self.peek()) is None: return None
        self.swap(1, len(self))
        self.pq.pop();
        self.qp.pop(top)
        self.sink(1);
        return top, self.kvs.pop(top)
    def push(self, k, v):
        self.pq.append(k)
        self.kvs[k] = v
        self.qp[k] = len(self)
        self.swim(len(self))
    def update(self, k, v):
        if k not in self.kvs: return
        self.kvs[k] = v
        i = self.qp[k]
        self.swim(i); self.sink(i)


class Graph:
    def __init__(self, mz):
        self.m, self.n = len(mz), len(mz[0])
        self.V = self.m * self.n; self.mz = mz
        self.adj = defaultdict(dict); self.connect()

    def flat(self, p):          return p[0] * self.n + p[1]
    def unflat(self, k):        return k // self.n, k % self.n
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
        if not self.valid(p):   return self.r(p), s - 1
        return self.lt(self.l(p), s + 1)
    def rt(self, p, s):
        if not self.valid(p):   return self.l(p), s - 1
        return self.rt(self.r(p), s + 1)
    def up(self, p, s):
        if not self.valid(p):   return self.d(p), s - 1
        return self.up(self.u(p), s + 1)
    def dn(self, p, s):
        if not self.valid(p):   return self.u(p), s - 1
        return self.dn(self.d(p), s + 1)
    def flt(self, k):           
        p, d = self.lt(self.unflat(k), 0)
        return self.flat(p), d
    def frt(self, k):           
        p, d = self.rt(self.unflat(k), 0)
        return self.flat(p), d
    def fup(self, k):           
        p, d = self.up(self.unflat(k), 0)
        return self.flat(p), d
    def fdn(self, k):
        p, d = self.dn(self.unflat(k), 0)
        return self.flat(p), d
    def join(self, k):
        if not (pl := self.flt(k)) == (k, 0):
            if pl[1] > 0: self.adj[k][pl[0]] = pl[1]
        if not (pr := self.frt(k)) == (k, 0):
            if pr[1] > 0: self.adj[k][pr[0]] = pr[1]
        if not (pu := self.fup(k)) == (k, 0):
            if pu[1] > 0: self.adj[k][pu[0]] = pu[1]
        if not (pd := self.fdn(k)) == (k, 0):
            if pd[1] > 0: self.adj[k][pd[0]] = pd[1]

    def connect(self):
        for k in range(self.V): self.join(k)


def dijkstra(g, s):
    dist, parent = {v: (0 if v == s else float('inf')) for v in range(g.V)}, [None] * g.V
    hs = IndexHeap(dist)
    while hs:
        u, du = hs.pop()
        dist[u] = du
        for v in g.adj[u]:
            if dist[v] > (duv := dist[u] + g.adj[u][v]): 
                dist[v] = duv
                hs.update(v, dist[v])
    return dist, parent

def maze(mz, s, t):
    g = Graph(mz); ks, kt = g.flat(s), g.flat(t)
    dist, _ = dijkstra(g, ks)
    return dist[kt] if not dist[kt] == float('inf') else -1

class Solution:
    def shortestDistance(self, mz: List[List[int]], s: List[int], t: List[int]) -> int:
        return maze(mz, s, t)






























