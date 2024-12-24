"""

499. The Maze III
Hard
Topics
There is a ball in a maze with empty spaces (represented as 0) and walls (represented as 1). The ball can go through the empty spaces by rolling up, down, left or right, but it won't stop rolling until hitting a wall. When the ball stops, it could choose the next direction. There is also a hole in this maze. The ball will drop into the hole if it rolls onto the hole.

Given the m x n maze, the ball's position ball and the hole's position hole, where ball = [ballrow, ballcol] and hole = [holerow, holecol], return a string instructions of all the instructions that the ball should follow to drop in the hole with the shortest distance possible. If there are multiple valid instructions, return the lexicographically minimum one. If the ball can't drop in the hole, return "impossible".

If there is a way for the ball to drop in the hole, the answer instructions should contain the characters 'u' (i.e., up), 'd' (i.e., down), 'l' (i.e., left), and 'r' (i.e., right).

The distance is the number of empty spaces traveled by the ball from the start position (excluded) to the destination (included).

You may assume that the borders of the maze are all walls (see examples).

 

Example 1:


Input: maze = [[0,0,0,0,0],[1,1,0,0,1],[0,0,0,0,0],[0,1,0,0,1],[0,1,0,0,0]], ball = [4,3], hole = [0,1]
Output: "lul"
Explanation: There are two shortest ways for the ball to drop into the hole.
The first way is left -> up -> left, represented by "lul".
The second way is up -> left, represented by 'ul'.
Both ways have shortest distance 6, but the first way is lexicographically smaller because 'l' < 'u'. So the output is "lul".
Example 2:


Input: maze = [[0,0,0,0,0],[1,1,0,0,1],[0,0,0,0,0],[0,1,0,0,1],[0,1,0,0,0]], ball = [4,3], hole = [3,0]
Output: "impossible"
Explanation: The ball cannot reach the hole.
Example 3:

Input: maze = [[0,0,0,0,0,0,0],[0,0,1,0,0,1,0],[0,0,0,0,1,0,0],[0,0,0,0,0,0,1]], ball = [0,4], hole = [3,5]
Output: "dldr"
 

Constraints:

m == maze.length
n == maze[i].length
1 <= m, n <= 100
maze[i][j] is 0 or 1.
ball.length == 2
hole.length == 2
0 <= ballrow, holerow <= m
0 <= ballcol, holecol <= n
Both the ball and the hole exist in an empty space, and they will not be in the same position initially.
The maze contains at least 2 empty spaces.

"""

from collections import defaultdict

class Graph:
    def __init__(self, V, es=None):
        self.V = V; self.adj = defaultdict(dict)
        self.es = es if es else None
        self.connect()

    def add(self, e):   self.adj[e[0]][e[1]] = e[2]
    def connect(self):  
        for e in es: self.add(e)

class IndexHeap:
    def __init__(self, kvs, cmp=lambda x, y: x < y):
        self.pq = [None] + list(kvs.keys())
        self.qp = {v: i for i, v in enumerate(self.pq) if i >= 1}
        self.kvs = kvs; self.cmp = cmp; self.heapify()

    def __iter__(self):
        hs = IndexHeap(self.kvs.copy(), self.cmp)
        while hs: yield hs.pop()
    def __len__(self):      return len(self.pq) - 1
    def __bool__(self):     return len(self) > 0
    def sorted(self):       return list(self)

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
        if i and j:             return self.prior(i, j)
        return i if not j else j

    def peek(self):             return self.pq[1] if self else None
    def pop(self):
        if (top := self.peek()) is None: return None
        self.swap(1, len(self))
        self.pq.pop()
        self.qp.pop(top)
        self.sink(1)
        return top, self.kvs.pop(top)
    def push(self, k, v):
        if k in self.kvs: self.update(k, v)
        self.kvs[k] = v; self.qp[k] = len(self)
        self.pq.append(k); self.swim(len(self))
    def update(self, k, v):
        if not k in self.kvs: return
        i = self.qp[k]; self.kvs[k] = v
        self.sink(i); self.swim(i)


def solve(mz, s, t):
    def flat(p):        return p[0] * n + p[1]
    def unflat(k):      return k // n, k % n
    def inside(p):      return 0 <= p[0] < m and 0 <= p[1] < n
    def val(p):         return mz[p[0]][p[1]]
    def clear(p):       return val(p) == 0
    def wall(p):        return val(p) == 1
    def valid(p):       return inside(p) and clear(p)
    def invalid(p):     return not valid(p)
    def l(p):           return p[0], p[1] - 1
    def r(p):           return p[0], p[1] + 1
    def u(p):           return p[0] - 1, p[1]
    def d(p):           return p[0] + 1, p[1]
    def lt(p, w):
        if invalid(p):  return r(p), w - 1
        return lt(l(p), w + 1)
    def rt(p, w):
        if invalid(p):  return l(p), w - 1
        return rt(r(p), w + 1)
    def up(p, w):
        if invalid(p):  return d(p), w - 1
        return up(u(p), w + 1)
    def dn(p, w):
        if invalid(p):  return u(p), w - 1
        return dn(d(p), w + 1)
    def flt(k):
        pl, w = lt(unflat(k), 0)
        return flat(pl), w
    def frt(k):
        pr, w = rt(unflat(k), 0)
        return flat(pr), w
    def fup(k):
        pu, w = up(unflat(k), 0)
        return flat(pu), w
    def fdn(k):
        pd, w = dn(unflat(k), 0)
        return flat(pd), w
    def edges(p):
        dls = [lt(p, 0), rt(p, 0), up(p, 0), dn(p, 0)]
        return [(p, pd, wd) for pd, wd in dls if wd > 0]
    def fedges(k):
        return [(k, flat(pd), wd) for _, pd, wd in edges(unflat(k))]
    def edgesall():
        return reduce(
                        lambda acc, w: acc + fedges(w), 
                        (v for v in range(g.V) if valid(v)), 
                        []
                     )

    def dijkstra(s):
        dist = {v: (0 if v == s else float('inf')) for v in range(g.V)}
        parents, hs = defaultdict(list), IndexHeap(dist)

        while hs:
            u, du = hs.pop()
            dist[u] = du
            for v in g.adj[u]:
                if dist[v] >= (duv := dist[u] + g.adj[u][v]):
                    if dist[v] == duv: 
                        parents.append(u)
                    else: 
                        parents[v] = [u]
                    dist[v] = duv
                    hs.update(v, dist[v])

        return dist, parents

    def paths(s, t):
        def path(t):
            ps = deque(); ps.append(t)
            

        _, parents = dijkstra(s)
        ps = parents[t]



    m, n = len(mz), len(mz[0])
    g = Graph(m * n, edges())
































