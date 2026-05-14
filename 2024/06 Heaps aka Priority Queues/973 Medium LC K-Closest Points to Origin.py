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

Runtime 1643 ms Beats 5.79%
Memory 22.55 MB Beats 24.18%

"""

from functools import reduce
from typing import List

class HeapDict:
    def __init__(self, kvs=None, cmp=lambda x, y: x < y):
        self.kvs = kvs if kvs else {}
        self.pq = [None] + (list(self.kvs.keys()))
        self.cmp = cmp; self.heapify()

    def heapify(self):
        for p in reversed(range(1, len(self) // 2 + 1)):
            self.sink(p)

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

    def parent(self, c):
        return self.valid(self.up(c))

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
        return i if self.isvalid(i) else None

    def isvalid(self, i):
        return 1 <= i <= len(self)

    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j

    def prior(self, i, j):
        return i if self.cmp(self.val(i), self.val(j)) else j

    def val(self, i):
        return self.kvs[self.pq[i]]

    def peek(self):
        return self.pq[1] if self else None

    def pop(self):
        if (top := self.peek()) is None: return None
        self.swap(1, len(self))
        self.pq.pop()
        self.kvs.pop(top)
        self.sink(1)
        return top

    def push(self, k, v):
        self.kvs[k] = v
        self.pq.append(k)
        self.swim(len(self))

    def sorted(self):
        return list(self)

    def __len__(self):
        return len(self.pq) - 1

    def __bool__(self):
        return len(self) > 0

    def __iter__(self):
        heap = HeapDict(self.kvs.copy(), self.cmp)
        while heap:
            yield heap.pop()


def rad(p):
    return p[0] ** 2 + p[1] ** 2

def kcs(ps, k):
    kvs = {i: rad(p) for i, p in enumerate(ps)}
    hs = HeapDict(kvs)
    return reduce(lambda acc, x: acc.append(ps[x]), hs, [])


class Solution:
    def kClosest(self, ps: List[List[int]], k: int) -> List[List[int]]:
        return kcs(ps, k)

if __name__ == '__main__':

    pass

