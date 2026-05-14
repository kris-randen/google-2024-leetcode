"""

Sliding Window Maximum
Statement

Given an integer list, nums, find the maximum values in all the contiguous subarrays (windows) of size w.

"""

from collections import deque


class Current:
    def __init__(self, ns):
        self.dq = deque()
        self.ns = ns
        self.n = len(self.ns)

    def valid(self, i): return 0 <= i < self.n

    def val(self, i):
        return None if not self.valid(i) else self.ns[i]

    def mink(self):
        return None if not self.dq else self.dq[-1]

    def minv(self):
        return None if not self.dq else self.ns[self.mink()]

    def maxk(self):
        return None if not self.dq else self.dq[0]

    def maxv(self):
        return None if not self.dq else self.ns[self.maxk()]

    def popmax(self): self.dq.popleft()

    def popmin(self): self.dq.pop()

    def drop(self, l, r):
        while self.dq and self.maxk() < l: self.popmax()

    def comp(self, r):
        return self.minv() <= self.val(r)

    def delete(self, r):
        while self.dq and self.comp(r): self.popmin()

    def update(self, l, r):
        self.drop(l, r)
        self.delete(r)
        self.dq.append(r)


def find_max_sliding_window(nums, w):
    if (n := len(nums)) <= w: return [max(nums)]
    if w == 1: return nums
    l, r, window, maxs = 0, 0, Current(nums), []
    while r < w - 1: window.update(l, r); r += 1
    while r < n:
        window.update(l, r)
        maxs.append(window.maxv())
        l += 1; r += 1
    return maxs

if __name__ == '__main__':
    pass



