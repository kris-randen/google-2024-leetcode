"""

1631. Path With Minimum Effort
Medium

You are a hiker preparing for an upcoming hike. You are given heights, a 2D array of size rows x columns, where heights[row][col] represents the height of cell (row, col). You are situated in the top-left cell, (0, 0), and you hope to travel to the bottom-right cell, (rows-1, columns-1) (i.e., 0-indexed). You can move up, down, left, or right, and you wish to find a route that requires the minimum effort.

A route's effort is the maximum absolute difference in heights between two consecutive cells of the route.

Return the minimum effort required to travel from the top-left cell to the bottom-right cell.

 

Example 1:



Input: heights = [[1,2,2],[3,8,2],[5,3,5]]
Output: 2
Explanation: The route of [1,3,5,3,5] has a maximum absolute difference of 2 in consecutive cells.
This is better than the route of [1,2,2,2,5], where the maximum absolute difference is 3.
Example 2:



Input: heights = [[1,2,3],[3,8,4],[5,3,5]]
Output: 1
Explanation: The route of [1,2,3,4,5] has a maximum absolute difference of 1 in consecutive cells, which is better than route [1,3,5,3,5].
Example 3:


Input: heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]
Output: 0
Explanation: This route does not require any effort.
 

Constraints:

rows == heights.length
columns == heights[i].length
1 <= rows, columns <= 100
1 <= heights[i][j] <= 106


Performance with heapq

Runtime 1061 ms Beats 20.56%
Memory 24.35 MB Beats 5.37%

Performance with IndexHeap

Runtime 6562 ms Beats 5.01%
Memory 26.20 MB Beats 5.37%

"""

from heapq import heappush as push, \
                  heappop as pop


def path(hs):
    def flat(p):        return p[0] * n + p[1]
    def unflat(v):      return v // n, v % n
    def val(p):         return hs[p[0]][p[1]]
    def dist(p, q):     return abs(val(p) - val(q))
    def fdst(u, v):     return dist(unflat(u), unflat(v))
    def valid(p):       return 0 <= p[0] < m and 0 <= p[1] < n
    def up(p):          return p[0] - 1, p[1]
    def dn(p):          return p[0] + 1, p[1]
    def lt(p):          return p[0], p[1] - 1
    def rt(p):          return p[0], p[1] + 1
    def adj(p):         return up(p), dn(p), lt(p), rt(p)
    def nbs(p):         return [q for q in adj(p) if valid(q)]
    def fbs(v):         return [flat(q) for q in nbs(unflat(v))]

    def dijkstra(s):
        dist = {v: float('inf') for v in range(V)}
        dist[s] = 0; pq = IndexHeap(dist)
        while pq:
            u, du = pq.pop()
            for v, w in g[u]:
                if dist[v] > (duv := max(fdst(u, v), dist[u])):
                    dist[v] = duv; pq.update(v, duv)
        return dist


    def dijkstrad(s):
        dist = [float('inf')] * V
        dist[s] = 0; pq = [(0, s)]
        while pq:
            du, u = pop(pq)
            if du > dist[u]: continue
            for v, w in g[u]:
                if dist[v] > (duv := max(fdst(u, v), dist[u])):
                    dist[v] = duv; push(pq, (duv, v))
        return dist

    m, n = len(hs), len(hs[0]); V = m * n
    g = [[] for _ in range(V)]
    for u in range(V):
        for v in fbs(u):
            g[u].append((v, fdst(u, v)))

    ps, pd = (0, 0), (m - 1, n - 1)
    st, dt = flat(ps), flat(pd)
    return dijkstra(st)[dt]


class IndexHeap:
    def __init__(self, kvs, cmp=lambda x, y: x < y):
        self.kvs = kvs; self.pq = [None] + list(self.kvs.keys())
        self.qp = {k: i for i, k in enumerate(self.pq) if i >= 1}
        self.cmp = cmp; self.heapify()

    def __iter__(self):
        hs = IndexHeap(self.kvs.copy(), self.cmp)
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
    def unbalup(self, c):       return self.parent(c) if not self.balup(c) else None
    def unbaldn(self, p):       return self.child(p) if not self.baldn(c) else None
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
    def val(self, i):           return self.kvs[self.key(i)]
    def key(self, i):           return self.pq[i]
    def kval(self, i):          return self.key(i), self.val(i)
    def prior(self, i, j):      return i if self.cmp(self.val(i), self.val(j)) else j
    def peek(self):             return self.kval(1) if self else None
    def pop(self):
        if (top := self.peek()) is None: return None
        self.swap(1, len(self)); k, v = top
        self.pq.pop(); self.qp.pop(k)
        self.sink(1); return top
    def update(self, k, v):
        i = self.qp[k]; self.kvs[k] = v
        self.sink(i); self.swim(i)


    def pref(self, i, j):
        if i and j:             return self.prior(i, j)
        return i if not j else j
    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]], self.qp[self.pq[j]] = i, j
        return j












