"""

973. K Closest Points to Origin
Solved
Medium
Topics
Companies
Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, return the k closest points to the origin (0, 0).

The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)2 + (y1 - y2)2).

You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).



Example 1:


Input: points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]
Explanation:
The distance between (1, 3) and the origin is sqrt(10).
The distance between (-2, 2) and the origin is sqrt(8).
Since sqrt(8) < sqrt(10), (-2, 2) is closer to the origin.
We only want the closest k = 1 points from the origin, so the answer is just [[-2,2]].
Example 2:

Input: points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]]
Explanation: The answer [[-2,4],[3,3]] would also be accepted.


Constraints:

1 <= k <= points.length <= 104
-104 <= xi, yi <= 104

"""

from heapq import *


class Heap:
    def __init__(self, vs=None, cmp=lambda a, b: a < b):
        self.vs = [None] + (vs if vs else [])
        self.cmp = cmp; self.N = None; self.heapify()

    def heapify(self):
        for p in reversed(range(1, self.size)): self.sink(p)

    def sink(self, p):
        while c := self.unbal_dn(p): p = self.swap(p, c)

    def swim(self, c):
        while p := self.unbal_up(c): c = self.swap(c, p)

    def swap(self, i, j):
        self.vs[i], self.vs[j] = self.vs[j], self.vs[i]
        return j

    def unbal_dn(self, p):
        return (c := self.child(p)) if not self.bal_dn(p) else None

    def unbal_up(self, c):
        return (p := self.parent(c)) if not self.bal_up(c) else None

    def bal_dn(self, p):
        return (c := self.child(p)) is None or self.pref(p, c) == p

    def bal_up(self, c):
        return (p := self.parent(c)) is None or self.pref(c, p) == p

    def pref(self, i, j):
        if i and j: return i if self.comp(i, j) else j
        return i if not j else j

    def parent(self, c):
        return self.valid(self.up(c))

    def left(self, p):
        return self.valid(self.lt(p))

    def right(self, p):
        return self.valid(self.rt(p))

    def child(self, p):
        return self.pref(self.left(p), self.right(p))

    def up(self, i):
        return i // 2

    def lt(self, i):
        return 2 * i

    def rt(self, i):
        return 2 * i + 1

    def comp(self, i, j):
        return self.cmp(self.val(i), self.val(j))

    def val(self, i):
        return self.vs[i] if self.valid(i) else None

    def valid(self, i):
        return i if self.is_valid(i) else None

    def is_valid(self, i):
        return i and 1 <= i <= self.size

    @property
    def size(self):
        return len(self.vs) - 1 if self.N is None else self.N

    def pop(self):
        self.swap(1, self.size)
        top = self.vs.pop()
        self.sink(1)
        return top

    def sort(self):
        self.N = self.size
        while self.N > 0:
            self.swap(1, self.N)
            self.N -= 1
            self.sink(1)
        self.N = None

class IndexHeap:
    def __init__(self, kvs=None, cmp=lambda a, b: a < b):
        self.kvs = kvs if kvs else {}
        self.pq = [None] + list(self.kvs.keys())
        self.qp = {v: i for i, v in enumerate(self.pq)}
        self.cmp = cmp; self.N = None; self.heapify()

    def heapify(self):
        for p in reversed(range(1, self.size)): self.sink(p)

    def sink(self, p):
        while c := self.unbal_dn(p): p = self.swap(p, c)

    def swim(self, p):
        while p := self.unbal_up(c): c = self.swap(c, p)

    def unbal_dn(self, p):
        return self.child(p) if not self.bal_dn(p) else None

    def unbal_up(self, c):
        return self.parent(c) if not self.bal_up(c) else None

    def bal_dn(self, p):
        return (c := self.child(p)) is None or self.pref(p, c) == p

    def bal_up(self, c):
        return (p := self.parent(c)) is None or self.pref(c, p) == p

    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        self.qp[self.pq[i]], self.qp[self.pq[j]] = i, j
        return j

    def parent(self, c):
        return self.valid(self.up(c))

    def child(self, p):
        return self.pref(self.left(p), self.right(p))

    def left(self, p):
        return self.valid(self.lt(p))

    def right(self, p):
        return self.valid(self.rt(p))

    def up(self, i): return i // 2

    def lt(self, i): return 2 * i

    def rt(self, i): return 2 * i + 1

    def pref(self, i, j):
        if i and j: return i if self.comp(i, j) else j
        return i if not j else j

    def comp(self, i, j):
        return self.cmp(self.val(i), self.val(j))

    def val(self, i):
        return self.kvs[self.pq[i]] if self.valid(i) else None

    def valid(self, i):
        return i if self.is_valid(i) else None

    def is_valid(self, i):
        return i and 1 <= i <= self.size

    @property
    def size(self):
        return len(self.kvs) if not self.N else self.N

    def pop(self):
        self.swap(1, self.size)
        topk = self.pq.pop()
        topv = self.kvs[topk]
        self.kvs.pop(topk)
        self.qp.pop(topk)
        self.sink(1)
        return (topk, topv)

def kcih(ps, k):
    ihd = IndexHeap({i: rad(p) for i, p in enumerate(ps)}); ms = []
    for _ in range(k): ms.append(ps[ihd.pop()[0]])
    return ms


def kch(ps, k):
    hd = Heap([(rad(p), p) for p in ps]); ms = []
    for _ in range(k): ms.append(hd.pop()[1])
    return ms


def rad(p): return p[0] ** 2 + p[1] ** 2


def kc(ps, k):
    hd = [(rad(p), p) for p in ps]
    heapify(hd); ms = []
    for _ in range(k): ms.append(heappop(hd)[1])
    return ms

if __name__ == '__main__':
    h = Heap([2, 9, 1, 3, 0, 5, 4])
    h.sort()
    print(h.vs)