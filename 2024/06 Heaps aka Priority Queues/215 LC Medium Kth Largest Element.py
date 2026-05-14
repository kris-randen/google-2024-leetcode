"""

215. Kth Largest Element in an Array
Medium
Given an integer array nums and an integer k, return the kth largest element in the array.

Note that it is the kth largest element in the sorted order, not the kth distinct element.

Can you solve it without sorting?



Example 1:

Input: nums = [3,2,1,5,6,4], k = 2
Output: 5
Example 2:

Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4


"""

class Heap:
    def __init__(self, vs=None, cmp=lambda a, b: a < b):
        self.vs = [None] + (list(vs) if vs else [])
        self.cmp = cmp; self.N = None
        self.heapify()
        print(self.vs)

    def heapify(self):
        for p in reversed(range(1, self.size)): self.sink(p)

    @property
    def size(self):
        return len(self.vs) - 1 if self.N is None else self.N

    def sink(self, p):
        while c := self.unbal_dn(p): p = self.swap(p, c)

    def swim(self, c):
        while p := self.unbal_up(c): c = self.swap(c, p)

    def unbal_dn(self, p):
        return self.child(p) if not self.bal_dn(p) else None

    def unbal_up(self, c):
        return self.parent(c) if not self.bal_up(c) else None

    def swap(self, i, j):
        self.vs[i], self.vs[j] = self.vs[j], self.vs[i]
        return j

    def bal_dn(self, p):
        return not (c := self.child(p)) or self.pref(p, c) == p

    def bal_up(self, c):
        return not (p := self.parent(c)) or self.pref(c, p) == p

    def pref(self, i, j):
        if i and j: return i if self.comp(i, j) else j
        return i if not j else j

    def comp(self, i, j):
        return self.cmp(self.val(i), self.val(j))

    def val(self, i):
        return self.vs[i] if self.valid(i) else None

    def valid(self, i):
        return i if self.is_valid(i) else None

    def is_valid(self, i):
        return i and 1 <= i <= self.size

    def up(self, i):
        return i // 2

    def lt(self, i):
        return 2 * i

    def rt(self, i):
        return 2 * i + 1

    def parent(self, c):
        return self.valid(self.up(c))

    def left(self, p):
        return self.valid(self.lt(p))

    def right(self, p):
        return self.valid(self.rt(p))

    def child(self, p):
        return self.pref(self.left(p), self.right(p))

    def push(self, v):
        self.vs.append(v)
        self.swim(self.size)

    def top(self):
        return self.vs[1]

    def pop(self):
        self.swap(1, self.size)
        v = self.vs.pop()
        self.sink(1)
        return v

    def sort(self):
        self.N = self.size
        while self.N > 0:
            print(self.vs)
            self.swap(1, self.N)
            self.N -= 1
            self.sink(1)
        self.N = None
        print(self.vs)
        self.heapify()

from heapq import *

def kthlarge(vs, k):
    if (n := len(vs)) < k or not vs: return float('-inf')
    kl = [min(vs)]
    for v in vs:
        if v > kl[0]: heappush(kl, v)
        if len(kl) > k: heappop(kl)
    return kl[0]


def kthlargeheap(vs, k):
    if (n := len(vs)) < k or not vs: return float('-inf')
    hs = Heap(); hs.push(min(vs))
    for v in vs:
        if v > hs.top(): hs.push(v)
        if hs.size > k: hs.pop()
    return hs.top()


if __name__ == '__main__':
    vs = [3, 2, 1, 5, 6, 4]
    k = 2
    print(kthlargeheap(vs, k))
    hs = Heap(vs)
    hs.sort()
    pass









