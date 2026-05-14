"""

347. Top K Frequent Elements
Medium
Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.



Example 1:

Input: nums = [1,1,1,2,2,3], k = 2
Output: [1,2]
Example 2:

Input: nums = [1], k = 1
Output: [1]


Constraints:

1 <= nums.length <= 105
-104 <= nums[i] <= 104
k is in the range [1, the number of unique elements in the array].
It is guaranteed that the answer is unique.


Follow up: Your algorithm's time complexity must be better than O(n log n), where n is the array's size.

Second Attempt

Runtime 30 ms Beats 5.24%
Memory 20.79 MB Beats 42.93%

"""
from functools import reduce
from heapq import *
from collections import Counter, defaultdict
from typing import List


def topKFreq(vs, k):
    return [v[0] for v in Counter(vs).most_common(k)]


def topk(vs, k):
    us = [-v for v in vs]; heapify(us); ms = []
    for _ in range(k): m = heappop(us); ms.append(-m)
    return ms


def vfilter(cs, vs):
    return [k for k, v in cs.items() if v in vs]


def topKF(vs, k):
    cs = Counter(vs)
    return vfilter(cs, topk(cs.values(), k))

# 20241208 8th Dec 2024 Re-solved

class HeapDict:
    def __init__(self, kvs=None, cmp=lambda x, y: x < y):
        self.kvs = kvs if kvs else {}
        self.pq = [None] + list(self.kvs.keys())
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

    def lt(self, i):
        return i * 2

    def rt(self, i):
        return i * 2 + 1

    def up(self, i):
        return i // 2

    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        return j

    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j

    def prior(self, i, j):
        return i if self.cmp(self.val(i), self.val(j)) else j

    def val(self, i):
        return self.kvs[self.pq[i]]

    def valid(self, i):
        return i if self.isvalid(i) else None

    def isvalid(self, i):
        return 1 <= i <= len(self)

    def peek(self):
        return self.pq[1] if self else None

    def pop(self):
        if (top := self.peek()) is None: return None
        self.swap(1, len(self))
        self.pq.pop()
        self.kvs.pop(top)
        self.sink(1)
        return top

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


def topkf(vs, k):
    kvs = defaultdict(int)
    for v in vs: kvs[v] += 1
    hs = HeapDict(kvs, cmp=lambda x, y: x > y)
    return reduce(lambda acc, _: acc.append(hs.pop()) or acc, range(k), [])


class Solution:
    def topKFrequent(self, vs: List[int], k: int) -> List[int]:
        return topkf(vs, k)
