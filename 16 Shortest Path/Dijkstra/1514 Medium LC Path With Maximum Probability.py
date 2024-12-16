"""

1514. Path with Maximum Probability
Solved
Medium
You are given an undirected weighted graph of n nodes (0-indexed), represented by an edge list where edges[i] = [a, b] is an undirected edge connecting the nodes a and b with a probability of success of traversing that edge succProb[i].

Given two nodes start and end, find the path with the maximum probability of success to go from start to end and return its success probability.

If there is no path from start to end, return 0. Your answer will be accepted if it differs from the correct answer by at most 1e-5.

 

Example 1:



Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.2], start = 0, end = 2
Output: 0.25000
Explanation: There are two paths from start to end, one having a probability of success = 0.2 and the other has 0.5 * 0.5 = 0.25.
Example 2:



Input: n = 3, edges = [[0,1],[1,2],[0,2]], succProb = [0.5,0.5,0.3], start = 0, end = 2
Output: 0.30000
Example 3:



Input: n = 3, edges = [[0,1]], succProb = [0.5], start = 0, end = 2
Output: 0.00000
Explanation: There is no path between 0 and 2.
 

Constraints:

2 <= n <= 10^4
0 <= start, end < n
start != end
0 <= a, b < n
a != b
0 <= succProb.length == edges.length <= 2*10^4
0 <= succProb[i] <= 1
There is at most one edge between every two nodes.

Runtime 1644 ms Beats 5.03%
Memory 30.69 MB Beats 5.39%

"""

from typing import List
from math import log, exp
from collections import defaultdict


class IndexHeap:
    def __init__(self, kvs=None, cmp=lambda x, y: x < y):
        self.kvs = kvs if kvs else {}
        self.pq = [None] + list(self.kvs.keys())
        self.qp = {v: i for i, v in enumerate(self.pq) if i >= 1}
        self.cmp = cmp;
        self.heapify()

    def __iter__(self):
        hs = IndexHeap(self.kvs, self.cmp)
        while hs: yield hs.pop()

    def __len__(self):
        return len(self.pq) - 1

    def __bool__(self):
        return len(self) > 0

    def sorted(self):
        return list(self)

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

    def unbalup(self, c):
        return self.parent(c) if not self.balup(c) else None

    def unbaldn(self, p):
        return self.child(p) if not self.baldn(p) else None

    def balup(self, c):
        return self.pref(p := self.parent(c), c) == p

    def baldn(self, p):
        return self.pref(c := self.child(p), p) == p

    def parent(self, c):
        return self.valid(self.up(c))

    def child(self, p):
        return self.pref(self.left(p), self.right(p))

    def left(self, p):
        return self.valid(self.lt(p))

    def right(self, p):
        return self.valid(self.rt(p))

    def up(self, i):
        return i // 2

    def lt(self, i):
        return i * 2

    def rt(self, i):
        return i * 2 + 1

    def valid(self, i):
        return i if self.isval(i) else None

    def isval(self, i):
        return 1 <= i <= len(self)

    def prior(self, i, j):
        return i if self.cmp(self.val(i), self.val(j)) else j

    def val(self, i):
        return self.kvs[self.pq[i]]

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
        self.kvs[k] = v;
        i = self.qp[k]
        self.swim(i);
        self.sink(i)


class Graph:
    def __init__(self, V, es=None):
        self.V = V;
        self.es = es if es else []
        self.adj = defaultdict(dict);
        self.connect(es)

    def add(self, e):
        self.adj[e[0]][e[1]] = e[2]
        self.adj[e[1]][e[0]] = e[2]

    def connect(self, es):
        for e in es: self.add(e)


def dijkstra(g, s):
    dist = {v: (0 if v == s else float('inf')) for v in range(g.V)}
    parent = [None] * g.V; hs = IndexHeap(dist)
    while hs:
        u, du = hs.pop()
        dist[u] = du
        for v in g.adj[u]:
            if dist[v] > (dv := dist[u] + g.adj[u][v]):
                hs.update(v, dv)
                parent[v] = u
    return dist, parent


def edges(ds, ps):
    return [(d[0], d[1], (-log(p) if p > 0 else float('inf'))) for d, p in zip(ds, ps)]


def maxprob(n, ds, ps, s, t):
    g = Graph(n, edges(ds, ps))
    dist, _ = dijkstra(g, s)
    return exp(-dist[t]) if not dist[t] == float('inf') else 0


class Solution:
    def maxProbability(self, n: int, ds: List[List[int]], ps: List[float], s: int, t: int) -> float:
        return maxprob(n, ds, ps, s, t)
