"""

3264. Final Array State After K Multiplication Operations I
Easy
You are given an integer array nums, an integer k, and an integer multiplier.

You need to perform k operations on nums. In each operation:

Find the minimum value x in nums. If there are multiple occurrences of the minimum value, select the one that appears first.
Replace the selected minimum value x with x * multiplier.
Return an integer array denoting the final state of nums after performing all k operations.

 

Example 1:

Input: nums = [2,1,3,5,6], k = 5, multiplier = 2

Output: [8,4,6,5,6]

Explanation:

Operation   Result
After operation 1   [2, 2, 3, 5, 6]
After operation 2   [4, 2, 3, 5, 6]
After operation 3   [4, 4, 3, 5, 6]
After operation 4   [4, 4, 6, 5, 6]
After operation 5   [8, 4, 6, 5, 6]
Example 2:

Input: nums = [1,2], k = 3, multiplier = 4

Output: [16,8]

Explanation:

Operation   Result
After operation 1   [4, 2]
After operation 2   [4, 8]
After operation 3   [16, 8]
 

Constraints:

1 <= nums.length <= 100
1 <= nums[i] <= 100
1 <= k <= 10
1 <= multiplier <= 5



Performance using inbuilt heapq

Runtime 0 ms Beats 100.00%
Memory 17.34 MB Beats 18.11%



Performance using my custom Heap class

Runtime 93 ms Beats 5.92%
Memory 17.82 MB Beats 11.77%

"""

from heapq import *
from typing import List


class Heap:
    def __init__(self, vs=None, cmp=lambda x, y: x > y):
        self.pq = [None] + (vs if vs else [])
        self.cmp = cmp; self.heapify()

    def __iter__(self):
        hs = Heap(self.pq[1:], self.cmp)
        while hs: yield hs.pop()
    def __len__(self):      return len(self.pq) - 1
    def __bool__(self):     return len(self) > 0
    

    def heapify(self):      
        for p in reversed(range(1, len(self) // 2 + 1)): self.sink(p)
    def swim(self, c):
        while p := self.unbalup(c): c = self.swap(c, p)
    def sink(self, p):
        while c := self.unbaldn(p): p = self.swap(p, c)
    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]; return j
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
    def val(self, i):       return self.pq[i]
    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j
    def peek(self):
        return self.pq[1] if self else None
    def pop(self):
        if (top := self.peek()) is None: return None
        self.swap(1, len(self))
        self.pq.pop()
        self.sink(1)
        return top
    def push(self, v):
        self.pq.append(v); self.swim(len(self))
    def sorted(self):
        return list(self)



def revmax(ks):
    heapify(ks := [(-k, -i) for k, i in ks]); return ks

def ksmalld(vs, k, i, ks):
    if i >= len(vs): return revmax(ks)
    heappush(ks, (-vs[i], -i))
    heappop(ks) if len(ks) > k else None
    return ksmall(vs, k, i + 1, ks)

def multkd(vs, k, f):
    ps = ksmall(vs, k, 0, [])
    for _ in range(k):
        p, i = heappop(ps)
        vs[i] = p * f
        heappush(ps, (vs[i], i))
    return vs

def ksmall(vs, k, i, ps):
    if i >= len(vs): return ps
    ps.push((vs[i], i))
    ps.pop() if len(ps) > k else None
    return ksmall(vs, k, i + 1, ps)

def multk(vs, k, f):
    ps = ksmall(vs, k, 0, Heap())
    ps = Heap(ps.pq[1:], cmp=lambda x, y: x < y)
    for _ in range(k):
        p, i = ps.pop()
        vs[i] = p * f
        ps.push((vs[i], i))
    return vs

class Solution:
    def getFinalState(self, vs: List[int], k: int, f: int) -> List[int]:
        return multk(vs, k, f)



















