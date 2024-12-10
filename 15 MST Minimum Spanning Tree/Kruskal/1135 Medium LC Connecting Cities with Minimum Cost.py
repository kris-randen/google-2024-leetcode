"""

1135. Connecting Cities With Minimum Cost
Medium
There are n cities labeled from 1 to n. You are given the integer n and an array connections where connections[i] = [xi, yi, costi] indicates that the cost of connecting city xi and city yi (bidirectional connection) is costi.

Return the minimum cost to connect all the n cities such that there is at least one path between each pair of cities. If it is impossible to connect all the n cities, return -1,

The cost is the sum of the connections' costs used.

Example 1:


Input: n = 3, connections = [[1,2,5],[1,3,6],[2,3,1]]
Output: 6
Explanation: Choosing any 2 edges will connect all cities so we choose the minimum 2.
Example 2:


Input: n = 4, connections = [[1,2,3],[3,4,4]]
Output: -1
Explanation: There is no way to connect all cities even if all edges are used.
 

"""

from heapq import *


class Heap:
    def __init__(self, vs, cmp=lambda x, y: x < y):
        self.pq = [None] + (vs if vs else [])
        self.cmp = cmp; self.heapify()

    def __len__(self):
        return len(self.pq) - 1
    def __bool__(self):
        return len(self) > 0
    def __iter__(self):
        heap = Heap(self.pq[1:], self.cmp)
        while heap:
            yield heap.pop()

    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j

    def isval(self, i):     return 1 <= i <= len(self)
    def valid(self, i):     return i if self.isval(i) else None
    def val(self, i):       return self.pq[i][2]
    def prior(self, i, j):  return i if self.cmp(self.val(i), self.val(j)) else j

    def heapify(self):
        for p in reversed(range(1, len(self) // 2 + 1)):
            self.sink(p)
    def peek(self):
        return self.pq[1] if self else None
    def pop(self):
        if (top := self.peek()) is None: return None
        self.swapend(); self.pq.pop()
        self.sinktop(); return top
    def sorted(self):
        return list(self)



    def swim(self, c):
        while p := self.unbalup(c):
            c = self.swap(c, p)
    def sink(self, p):
        while c := self.unbaldn(p):
            p = self.swap(p, c)
    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        return j
    def swapend(self):
        self.swap(1, len(self))
    def swimbot(self):
        self.swim(len(self))
    def sinktop(self):
        self.sink(1)

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

class UnionFind:
    def __init__(self, n, es):
        self.id = [None] + [i for i in range(1, n + 1)]
        self.sz = {i: 1 for i in range(1, n + 1)}

    def connect(self, es):
        for e in es: self.add(e)

    def add(self, e):
        self.union(e[0], e[1])

    def union(self, p, q):
        self.update(*self.split(p, q)) if not self.find(p, q) else None

    def unione(self, e):
        self.union(e[0], e[1])

    def find(self, p, q):
        return self.root(p) == self.root(q)

    def finde(self, e):
        return self.find(e[0], e[1])

    def isroot(self, p):
        return p == self.id[p]

    def nroot(self, p):
        return not self.isroot(p)

    def update(self, s, l):
        self.assign(s, l); self.sizeup(s, l)

    def assign(self, s, l):
        self.id[s] = l

    def sizeup(self, s, l):
        self.sz[l] += self.sz.pop(s, 0)

    def split(self, p, q):
        return self.pair(*self.roots(p, q))

    def roots(self, p, q):
        return self.root(p), self.root(q)

    def pair(self, s, l):
        return (s, l) if self.sz[s] < self.sz[l] else (l, s)

    def root(self, p):
        if not self.isroot(p): self.id[p] = self.root(self.id[p])
        return self.id[p]

def kruskalMST(n, wes):
    uf, hs, mst = UnionFind(n, wes), Heap(wes), set()
    while hs and len(mst) < n - 1:
        if not uf.finde(we := tuple(hs.pop())): 
            uf.unione(we); mst.add(we)
    return sum(wt for _, _, wt in mst) if len(uf.sz) == 1 else -1



def kruskalMSTheapq(n, wes):
    uf = UnionFind(n, wes)
    tes = [(wt, x, y) for x, y, wt in wes]
    heapify(tes); mst = set()
    while len(mst) < n - 1:
        we = heappop(tes); x, y, _ = we
        if not uf.find(x, y):
            uf.add(we); mst.add(we)
    if len(uf.sz) > 1: return -1
    return sum(wt for _, _, wt in mst)












