"""

15. 3Sum
Solved
Medium

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

 

Example 1:

Input: nums = [-1,0,1,2,-1,-4]
Output: [[-1,-1,2],[-1,0,1]]
Explanation: 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.
Example 2:

Input: nums = [0,1,1]
Output: []
Explanation: The only possible triplet does not sum up to 0.
Example 3:

Input: nums = [0,0,0]
Output: [[0,0,0]]
Explanation: The only possible triplet sums up to 0.
 

Constraints:

3 <= nums.length <= 3000
-105 <= nums[i] <= 105

Performance

Runtime 1129 ms Beats 16.76%
Memory 20.40 MB Beats 34.23%

"""


def two(vs, t):
    l, r = 0, len(vs) - 1; sums = set()
    while l < r:
        if (s := vs[l] + vs[r]) == t:
            sums.add((vs[l], vs[r])); l += 1
        if s < t: l += 1
        if s > t: r -= 1
    return sums

def join(xs, x, yss):
    def adds(x, yss):
        def add(x, ys): return tuple(sorted((x,) + ys))
        return set(add(x, ys) for ys in yss) if yss else set()
    xs.update(adds(x, yss))

def three(vs, t):
    if t < sum(vs[:3]) or \
       t > sum(vs[-3:]): return []

    sums, ns = set(), set()
    for i, v in enumerate(vs):
        if not vs[i] in ns:
            ws, s = vs[:i] + vs[i + 1:], t - v
            join(sums, v, two(ws, s)); ns.add(v)

    return list(sums)


class Solution:
    def threeSum(self, vs: List[int]) -> List[List[int]]:
        return three(sorted(vs), 0)















