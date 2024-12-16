"""

2593. Find Score of an Array After Marking All Elements
Solved
Medium
Topics
Companies
Hint
You are given an array nums consisting of positive integers.

Starting with score = 0, apply the following algorithm:

Choose the smallest integer of the array that is not marked. If there is a tie, choose the one with the smallest index.
Add the value of the chosen integer to score.
Mark the chosen element and its two adjacent elements if they exist.
Repeat until all the array elements are marked.
Return the score you get after applying the above algorithm.



Example 1:

Input: nums = [2,1,3,4,5,2]
Output: 7
Explanation: We mark the elements as follows:
- 1 is the smallest unmarked element, so we mark it and its two adjacent elements: [2,1,3,4,5,2].
- 2 is the smallest unmarked element, so we mark it and its left adjacent element: [2,1,3,4,5,2].
- 4 is the only remaining unmarked element, so we mark it: [2,1,3,4,5,2].
Our score is 1 + 2 + 4 = 7.
Example 2:

Input: nums = [2,3,5,1,3,2]
Output: 5
Explanation: We mark the elements as follows:
- 1 is the smallest unmarked element, so we mark it and its two adjacent elements: [2,3,5,1,3,2].
- 2 is the smallest unmarked element, since there are two of them, we choose the left-most one, so we mark the one at index 0 and its right adjacent element: [2,3,5,1,3,2].
- 2 is the only remaining unmarked element, so we mark it: [2,3,5,1,3,2].
Our score is 1 + 2 + 2 = 5.

"""

from heapq import *
from typing import List


class IndexHeap:
    def __init__(self, vs=None, cmp=lambda x, y: x < y):
        self.pq = [None] + (vs if vs else [])
        self.qp = {v: i for i, v in enumerate(self.pq) if i >= 1}
        self.cmp = cmp; self.heapify()

    def __len__(self):
        return len(self.pq) - 1

    def __bool__(self):
        return len(self) > 0

    def __iter__(self):
        hs = IndexHeap(self.pq[1:], self.cmp)
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
        self.qp[self.pq[i]], self.qp[self.pq[j]] = i, j
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

    def valid(self, i):
        return i if self.isval(i) else None

    def isval(self, i):
        return 1 <= i <= len(self)

    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j

    def prior(self, i, j):
        return i if self.cmp(self.val(i), self.val(j)) else j

    def val(self, i):
        return self.pq[i]

    def peek(self):
        return self.pq[1] if self else None

    def pop(self):
        if (top := self.peek()) is None: return None
        self.swap(1, len(self))
        self.pq.pop()
        self.qp.pop(top)
        self.sink(1)
        return top

    def delete(self, v):
        if not v in self.qp: return
        i = self.qp[v]
        self.swap(i, len(self))
        self.pq.pop()
        self.qp.pop(v)
        if i <= len(self):
            self.sink(i);
            self.swim(i)

    def sorted(self):
        return list(self)


def pheap(vs):
    hs = [(v, i) for i, v in enumerate(vs)]
    return vs, IndexHeap(hs)


def valid(iv, vs):
    return 0 <= iv < len(vs)


def nbns(iv, vs):
    return [(vs[i], i) for i in (iv - 1, iv + 1) if valid(i, vs)]


def scored(vs, hs):
    s = 0
    while hs:
        s += (hv := hs.pop())[0]
        for vn in nbns(hv[1], vs): hs.delete(vn)
    return s


def score(vs):
    seen, s = [0] * (n := len(vs)), 0
    us = sorted([(v, i) for i, v in enumerate(vs)])
    for u, i in us:
        if not seen[i]:
            s += u; seen[i] = 1
            if i - 1 >= 0: seen[i - 1] = 1
            if i + 1 < n: seen[i + 1] = 1
    return s


class Solution:
    def findScore(self, vs: List[int]) -> int:
        return score(vs)
