"""

875. Koko Eating Bananas
Solved
Medium
Topics
Companies
Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas. The guards have gone and will come back in h hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile of bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.

Return the minimum integer k such that she can eat all the bananas within h hours.

 

Example 1:

Input: piles = [3,6,7,11], h = 8
Output: 4
Example 2:

Input: piles = [30,11,23,4,20], h = 5
Output: 30
Example 3:

Input: piles = [30,11,23,4,20], h = 6
Output: 23
 

Constraints:

1 <= piles.length <= 104
piles.length <= h <= 109
1 <= piles[i] <= 109

Performance of recursive can:

Runtime 3682 ms Beats 5.10%
Memory 26.68 MB Beats 5.21%


"""


from heapq import heapify, heappop as pop, heappush as push

def minspeed(ps, h):
    def cand(s, h, psc):
        if s == 0 or h == 0: return False
        if len(psc) == 0: return True
        if len(psc) == 1: return h >= ceil(psc[0] / s)
        bn = pop(psc)
        if bn > s:
            h -= bn // s
            if not bn % s == 0: push(psc, bn % s)
        else:
            h -= 1
        return can(s, h, psc)

    def can(s):
        return h >= sum(ceil(p / s) for p in ps)

    def bs(lo, hi):
        if can(lo): return lo
        if hi <= lo + 1: return lo + 1
        if can(s := (lo + hi) // 2):
            return bs(lo, s)
        else:
            return bs(s, hi)

    maxs, mins = max(ps), 0
    return bs(mins, maxs)


class Solution:
    def minEatingSpeed(self, ps: List[int], h: int) -> int:
        return minspeed(ps, h)
