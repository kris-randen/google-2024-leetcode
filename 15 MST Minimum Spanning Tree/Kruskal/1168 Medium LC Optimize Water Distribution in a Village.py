"""

1168. Optimize Water Distribution in a Village
Solved
Hard
Topics
Companies
Hint
There are n houses in a village. We want to supply water for all the houses by building wells and laying pipes.

For each house i, we can either build a well inside it directly with cost wells[i - 1] (note the -1 due to 0-indexing), or pipe in water from another well to it. The costs to lay pipes between houses are given by the array pipes where each pipes[j] = [house1j, house2j, costj] represents the cost to connect house1j and house2j together using a pipe. Connections are bidirectional, and there could be multiple valid connections between the same two houses with different costs.

Return the minimum total cost to supply water to all houses.


Example 1:


Input: n = 3, wells = [1,2,2], pipes = [[1,2,1],[2,3,1]]
Output: 3
Explanation: The image shows the costs of connecting houses using pipes.
The best strategy is to build a well in the first house with cost 1 and connect the other houses to it with cost 2 so the total cost is 3.
Example 2:

Input: n = 2, wells = [1,1], pipes = [[1,2,1],[1,2,2]]
Output: 2
Explanation: We can supply water with cost two using one of the three options:
Option 1:
  - Build a well inside house 1 with cost 1.
  - Build a well inside house 2 with cost 1.
The total cost will be 2.
Option 2:
  - Build a well inside house 1 with cost 1.
  - Connect house 2 with house 1 with cost 1.
The total cost will be 2.
Option 3:
  - Build a well inside house 2 with cost 1.
  - Connect house 1 with house 2 with cost 1.
The total cost will be 2.
Note that we can connect houses 1 and 2 with cost 1 or with cost 2 but we will always choose the cheapest option.


Constraints:

2 <= n <= 104
wells.length == n
0 <= wells[i] <= 105
1 <= pipes.length <= 104
pipes[j].length == 3
1 <= house1j, house2j <= n
0 <= costj <= 105
house1j != house2j

"""
from typing import List


class UF:
    def __init__(self, n):
        self.id = [None] + [i for i in range(1, n + 1)]
        self.sz = {i: 1 for i in range(1, n + 1)}

    def unione(self, e):        self.union(e[0], e[1])

    def union(self, p, q):      self.update(*self.split(p, q))

    def update(self, s, l):     self.assign(s, l); self.sizeup(s, l)

    def assign(self, s, l):     self.id[s] = l

    def sizeup(self, s, l):     self.sz[l] += self.sz.pop(s)

    def split(self, p, q):      return self.pair(*self.roots(p, q))

    def pair(self, s, l):       return (s, l) if self.sz[s] < self.sz[l] else (l, s)

    def roots(self, p, q):      return self.root(p), self.root(q)

    def find(self, p, q):       return self.root(p) == self.root(q)

    def finde(self, e):         return self.find(e[0], e[1])

    def root(self, p):
        if not self.id[p] == p:
            self.id[p] = self.root(self.id[p])
        return self.id[p]


class Heap:
    def __init__(self, es=None, cmp=lambda x, y: x < y):
        self.pq = [None] + (es if es else [])
        self.cmp = cmp; self.heapify()

    def __len__(self):
        return len(self.pq) - 1

    def __bool__(self):
        return len(self) > 0

    def __iter__(self):
        hs = Heap(self.pq[1:], self.cmp)
        while hs:
            yield hs.pop()

    def heapify(self):
        for p in reversed(range(1, len(self) // 2 + 1)): self.sink(p)

    def sink(self, p):
        while c := self.unbaldn(p):
            p = self.swap(p, c)

    def swim(self, c):
        while p := self.unbalup(c):
            c = self.swap(c, p)

    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        return j

    def unbaldn(self, p):
        return self.child(p) if not self.baldn(p) else None

    def unbalup(self, c):
        return self.parent(c) if not self.balup(c) else None

    def baldn(self, p):
        return self.pref(c := self.child(p), p) == p

    def balup(self, c):
        return self.pref(p := self.parent(c), c) == p

    def child(self, p):
        return self.pref(self.left(p), self.right(p))

    def left(self, p):
        return self.valid(self.lt(p))

    def right(self, p):
        return self.valid(self.rt(p))

    def parent(self, c):
        return self.valid(self.up(c))

    def lt(self, i):
        return i * 2

    def rt(self, i):
        return i * 2 + 1

    def up(self, i):
        return i // 2

    def val(self, i):
        return self.pq[i][2]

    def isval(self, i):
        return 1 <= i <= len(self)

    def valid(self, i):
        return i if self.isval(i) else None

    def prior(self, i, j):
        return i if self.cmp(self.val(i), self.val(j)) else j

    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j

    def peek(self):
        return self.pq[1] if self else None

    def pop(self):
        if (top := self.peek()) is None: return None
        self.swap(1, len(self))
        self.pq.pop(); self.sink(1)
        return top


def edges(n, ws, ps):
    return [tuple(p) for p in ps] + [(n + 1, i + 1, ws[i]) for i, w in enumerate(ws)]


def water(n, ws, ps):
    uf = UF(n + 1); mst = set()
    es = edges(n, ws, ps); hs = Heap(es)
    while hs and len(mst) < n + 1:
        if not uf.finde(e := hs.pop()):
            uf.unione(e); mst.add(e)
    return sum(e[2] for e in mst)


class Solution:
    def minCostToSupplyWater(self, n: int, ws: List[int], ps: List[List[int]]) -> int:
        return water(n, ws, ps)
