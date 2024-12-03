"""

1167. Minimum Cost to Connect Sticks
Solved
Medium
Topics
Companies
Hint
You have some number of sticks with positive integer lengths. These lengths are given as an array sticks, where sticks[i] is the length of the ith stick.

You can connect any two sticks of lengths x and y into one stick by paying a cost of x + y. You must connect all the sticks until there is only one stick remaining.

Return the minimum cost of connecting all the given sticks into one stick in this way.



Example 1:

Input: sticks = [2,4,3]
Output: 14
Explanation: You start with sticks = [2,4,3].
1. Combine sticks 2 and 3 for a cost of 2 + 3 = 5. Now you have sticks = [5,4].
2. Combine sticks 5 and 4 for a cost of 5 + 4 = 9. Now you have sticks = [9].
There is only one stick left, so you are done. The total cost is 5 + 9 = 14.
Example 2:

Input: sticks = [1,8,3,5]
Output: 30
Explanation: You start with sticks = [1,8,3,5].
1. Combine sticks 1 and 3 for a cost of 1 + 3 = 4. Now you have sticks = [4,8,5].
2. Combine sticks 4 and 5 for a cost of 4 + 5 = 9. Now you have sticks = [9,8].
3. Combine sticks 9 and 8 for a cost of 9 + 8 = 17. Now you have sticks = [17].
There is only one stick left, so you are done. The total cost is 4 + 9 + 17 = 30.
Example 3:

Input: sticks = [5]
Output: 0
Explanation: There is only one stick, so you don't need to do anything. The total cost is 0.


Constraints:

1 <= sticks.length <= 104
1 <= sticks[i] <= 104

"""

from typing import List

class Heap:
    def __init__(self, vs=None, cmp=lambda x, y: x < y):
        self.pq = [None] + (vs if vs else [])
        self.cmp = cmp; self.heapify()

    def __len__(self):
        return len(self.pq) - 1

    def __bool__(self):
        return len(self) > 0

    def __iter__(self):
        heap = Heap(self.pq[1:].copy(), self.cmp)
        while heap:
            yield heap.pop()

    def pref(self, i, j):
        if i and j: return self.prior(i, j)
        return i if not j else j

    def prior(self, i, j):
        return i if self.cmp(self.val(i), self.val(j)) else j

    def val(self, i):
        return self.pq[i]

    def isvalid(self, i):
        return 1 <= i <= len(self)

    def valid(self, i):
        return i if self.isvalid(i) else None

    def up(self, i):
        return i // 2

    def lt(self, i):
        return i * 2

    def rt(self, i):
        return i * 2 + 1

    def parent(self, c):
        return self.valid(self.up(c))

    def left(self, p):
        return self.valid(self.lt(p))

    def right(self, p):
        return self.valid(self.rt(p))

    def child(self, p):
        return self.pref(self.left(p), self.right(p))

    def balup(self, c):
        return self.pref(p := self.parent(c), c) == p

    def baldn(self, p):
        return self.pref(c := self.child(p), p) == p

    def unbalup(self, c):
        return self.parent(c) if not self.balup(c) else None

    def unbaldn(self, p):
        return self.child(p) if not self.baldn(p) else None

    def swap(self, i, j):
        self.pq[i], self.pq[j] = self.pq[j], self.pq[i]
        return j

    def swim(self, c):
        while p := self.unbalup(c):
            c = self.swap(c, p)

    def sink(self, p):
        while c := self.unbaldn(p):
            p = self.swap(p, c)

    def swapend(self):
        self.swap(1, len(self))

    def swimbot(self):
        self.swim(len(self))

    def sinktop(self):
        self.sink(1)

    def sinkswim(self, p):
        self.sink(p); self.swim(p)

    def peek(self):
        return self.pq[1]

    def pop(self):
        top = self.peek()
        self.swapend()
        self.pq.pop()
        self.sinktop()
        return top

    def push(self, v):
        self.pq.append(v)
        self.swimbot()

    def heapify(self):
        for p in reversed(range(1, len(self))): self.sink(p)

def connecth(ts):
    hs = Heap(ts); c = 0
    while len(hs) > 1:
        x, y = hs.pop(), hs.pop()
        c += x + y; hs.push(x + y)
    return c

class Solution:
    def connectSticks(self, ts: List[int]) -> int:
        return connecth(ts)
