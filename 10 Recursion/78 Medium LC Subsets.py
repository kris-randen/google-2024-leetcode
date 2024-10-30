"""

78. Subsets
Solved
Medium
Topics
Companies
Given an integer array nums of unique elements, return all possible
subsets
 (the power set).

The solution set must not contain duplicate subsets. Return the solution in any order.



Example 1:

Input: nums = [1,2,3]
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
Example 2:

Input: nums = [0]
Output: [[],[0]]


Constraints:

1 <= nums.length <= 10
-10 <= nums[i] <= 10
All the numbers of nums are unique.
Seen this question in a real interview before?
1/5
Yes
No
Accepted
2.1M
Submissions
2.6M
Acceptance Rate
79.0%

Runtime 30 ms Beats 97.67%
Memory 17.09 MB Beats 23.82%

"""

from typing import List
from functools import reduce
from collections import deque

def mul(d, dss):
    return reduce(lambda ess, es: ess.add((d,) + es) or ess, dss, set())

def subs(vs):
    if not vs: return {()}
    v = vs.pop()
    ds = subs(vs)
    es = mul(v, ds)
    return ds.union(es)

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        return [list(ss) for ss in subs(nums)]