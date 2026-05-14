"""

Problem 1: Classic Single-Source Shortest Path in a Directed Graph

Description:
You are given a directed graph with N nodes labeled from 0 to N-1 and M weighted edges. Each edge (u, v, w) indicates a directed edge from u to v with a non-negative cost w. Given a source node S, find the minimum distance from S to every other node. If a node is not reachable, output -1 for that node.

Input Format:

First line: N M S
Next M lines: u v w describing each edge.
Output Format:

Print N integers on a single line, where the i-th integer is the distance from S to i, or -1 if unreachable.
Test Case 1:

Copy code
4 4 0
0 1 1
0 2 4
1 2 2
2 3 1
Expected Output: 0 1 3 4

Test Case 2:

Copy code
5 3 2
2 0 5
2 1 2
1 3 3
Unreachable nodes expected.
Expected Output: 5 2 -1 5 -1
(Here, 0 reachable with cost 5, 1 with cost 2, 3 with cost 5, and 4 is unreachable.)

"""


class IndexHeap:
    def __init__(self, kvs, cmp=lambda x, y: x < y):
        self.pq = [None] + list(kvs.keys()); self.kvs = kvs
        self.qp = {v: i for i, v in enumerate(self.pq) if i >= 1}
        self.cmp = cmp; self.heapify()

    def __iter__(self):
        hs = IndexHeap(self.kvs, self.cmp)
        while hs: yield hs.pop()
    def __len__(self):      return len(self.pq) - 1
    def __bool__(self):     return len(self) > 0
    def sorted(self):       return list(self)

    def heapify(self):      for p in reversed(range(1, len(self) // 2 + 1)): self.sink(p)
    def swim(self, c):      while p := self.unbalup(c): c = self.swap(c, p)
    def sink(self, p):      while c := self.unbaldn(p): p = self.swap(p, c)
    def unbalup(self, c):   return self.parent(c) if not self.balup(c) else None
    def unbaldn(self, p):   return self.child(p) if not self.baldn(p) else None
    def balup(self, c):     return self.pref(p := self.parent(c), c) == p
    def baldn(self, p):     return self.pref(c := self.child(p), p) == p
    def parent(self, c):    return self.valid(self.up(c))
    def child(self, p):     return self.pref(self.left(p), self.right(p))
    def left(self, p):      return self.valid(self.lt(p))
    def right(self, p):     return self.valid(self.rt(p))
    def valid(self, i):     return i if self.isval(i) else None
    def isval(self, i):     return 1 <= i <= len(self)
    def prior(self, i, j):  return i if self.cmp(self.val(i), self.val(j)) else j
    def key(self, i):       return self.pq[i]
    def val(self, i):       return self.kvs[self.key(i)]
    def kval(self, i):      return self.key(i), self.val(i)
    def pref(self, i, j):
        if i and j:         return self.prior(i, j)
        return i if not j else j
    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]], self.qp[self.pq[j]] = i, j
        return j
    def peek(self):         return self.kval(1) if self else None
    def pop(self):
        if (top := self.peek()) is None: return None
        self.swap(1, len(self)); k, v = top
        self.pq.pop(); self.qp.pop(k)
        self.kvs.pop(k); self.sink(1)
        return top
    def push(self, k, v):
        if k in self.kvs: return
        self.kvs[k] = v
        self.pq.append(k)
        self.qp[k] = len(self)
        self.swim(len(self))
    def update(self, k, v):
        if k not in self.kvs: self.push(k, v)
        self.kvs[k] = v; i = self.qp[k]
        self.swim(i); self.sink(i)

class DiGraph:
    def __init__(self, V, es=None):
        self.V = V; self.Vs = range(self.V)
        self.adj = defaultdict(dict)
        for e in es: self.add(e)

    def add(self, e):
        self.adj[e[0]][e[1]] = e[2]

def dijkstra(g, s):
    dist, prns = {v: (0 if v == s else float('inf')) for v in g.Vs}, [None] * g.V
    dheap = IndexHeap(dist)
    while dheap:
        u, du = dheap.pop(); dist[u] = du
        for v in g.adj[u]:
            if dist[v] > (duv := dist[u] + g.adj[u][v]):
                dist[v] = duv; prns[v] = u
                dheap.update(v, dist[v])
    return dist, prns



from heapq import heappush as push, \
                  heappop as pop

graph = {v: {} for v in range(n)}
for u, v, w in es: graph[u][v] = w

def dijkstra(graph, s):
    dist = [float('inf')] * len(graph)
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        du, u = pop(pq)
        if du > dist[u]: continue
        for v in graph[u]:
            if dist[v] > (duv := dist[u] + graph[u][v]):
                dist[v] = duv
                push(pq, (dist[v], v))
    return dist

from heapq import heappush as push, \
                  heappop as pop

g = [[] for _ in range(n)]
for u, v, w in es: g[u].append((v, w))

def dijkstra(g, s):
    dist = [float('inf')] * len(g)
    dist[s] = 0; pq = [(0, s)]
    while pq:
        du, u = pop(pq)
        if du > dist[u]: continue
        for v, w in g[u]:
            if dist[v] > (duv := dist[u] + w):
                dist[v] = duv; push(pq, (duv, v))
    return dist



























