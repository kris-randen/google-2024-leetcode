"""

743. Network Delay Time
Medium
You are given a network of n nodes, labeled from 1 to n. You are also given times, a list of travel times as directed edges times[i] = (ui, vi, wi), where ui is the source node, vi is the target node, and wi is the time it takes for a signal to travel from source to target.

We will send a signal from a given node k. Return the minimum time it takes for all the n nodes to receive the signal. If it is impossible for all the n nodes to receive the signal, return -1.

 

Example 1:


Input: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
Output: 2
Example 2:

Input: times = [[1,2,1]], n = 2, k = 1
Output: 1
Example 3:

Input: times = [[1,2,1]], n = 2, k = 2
Output: -1
 

Constraints:

1 <= k <= n <= 100
1 <= times.length <= 6000
times[i].length == 3
1 <= ui, vi <= n
ui != vi
0 <= wi <= 100
All the pairs (ui, vi) are unique. (i.e., no multiple edges.)

Performance with heapq

Runtime 362 ms Beats 86.90%
Memory 20.10 MB Beats 5.54%

Performance with IndexHeap (completed successfully in first attempt: kudos!)

Runtime 374 ms Beats 60.18%
Memory 20.49 MB Beats 5.54%

"""

from heapq import heappush as push, \
                  heappop as pop


class IndexHeap:
    def __init__(self, kvs, cmp=lambda x, y: x < y):
        self.kvs = kvs; self.pq = [None] + list(self.kvs.keys())
        self.qp = {v: i for i, v in enumerate(self.pq) if i >= 1}
        self.cmp = cmp; self.heapify()

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

    def unbalup(self, c):   return self.parent(c) if not self.balup(c) else None
    def unbaldn(self, p):   return self.child(p) if not self.baldn(p) else None
    def balup(self, c):     return self.pref(p := self.parent(c), c) == p
    def baldn(self, p):     return self.pref(c := self.child(p), p) == p
    def parent(self, c):    return self.valid(self.up(c))
    def child(self, p):     return self.pref(self.left(p), self.right(p))
    def left(self, p):      return self.valid(self.lt(p))
    def right(self, p):     return self.valid(self.rt(p))
    def up(self, i):        return i // 2
    def lt(self, i):        return i * 2
    def rt(self, i):        return i * 2 + 1
    def valid(self, i):     return i if self.isval(i) else None
    def isval(self, i):     return 1 <= i <= len(self)
    def prior(self, i, j):  return i if self.cmp(self.val(i), self.val(j)) else j
    def val(self, i):       return self.kvs(self.key(i))
    def key(self, i):       return self.pq[i]
    def kval(self, i):      return self.key(i), self.val(i)
    def peek(self):         return self.kval(1) if self else None

    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j
    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]], self.qp[self.pq[j]] = i, j
        return j
    def pop(self):
        if (top := self.peek()) is None: return None
        self.swap(1, len(self)); k, v = top
        self.pq.pop(); self.qp.pop(k)
        self.kvs.pop(k); self.sink(1)
        return top
    def push(self, k, v):
        if k in self.kvs: self.update(k, v)
        self.pq.append(k); self.qp[k] = len(self)
        self.kvs[k] = v; self.swim(len(self))
    def update(self, k, v):
        if k not in self.kvs: return
        i = self.qp[k]; self.kvs[k] = v
        self.sink(i); self.swim(i)
    def delete(self, k):
        i = self.qp[k]; self.swap(i, len(self))
        self.pq.pop(); self.qp.pop(k); self.kvs.pop(k)
        if i <= len(self): self.sink(i); self.swim(i)



class Graph:
    def __init__(self, V, es, start=1):
        self.Vs = range(start, V + start)        
        self.adj = defaultdict(dict)
        for u, v, w in es: self.adj[u][v] = w

def dijkstra(g, s):
    def connected(v): return not dist[v] == float('inf')

    dist = {v: float('inf') for v in g.Vs}
    dist[s] = 0; pq = IndexHeap(dist)
    while pq:
        u, du = pq.pop()
        for v in g.adj[u]:
            if dist[v] > (duv := dist[u] + g.adj[u][v]):
                dist[v] = duv; pq.update(v, duv)
    return dist, all(connected(v) for v in g.Vs)

def dijkstrad(g, s):
    def connected(v): return not dist[v] == float('inf')

    dist = {v: float('inf') for v in g.Vs}
    dist[s] = 0; pq = [(0, s)]
    while pq:
        du, u = pop(pq)
        if du > dist[u]: continue
        for v in g.adj[u]:
            if dist[v] > (duv := dist[u] + g.adj[u][v]):
                dist[v] = duv; push(pq, (duv, v))
    return dist, all(connected(v) for v in g.Vs)

def minT(n, es, s):
    times, connected = dijkstra(Graph(n, es), s)
    return max(times) if connected else -1

class Solution:
    def networkDelayTime(self, es: List[List[int]], n: int, s: int) -> int:
        return minT(n, es, s)


























