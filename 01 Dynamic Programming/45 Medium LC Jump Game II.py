"""

45. Jump Game II
Solved
Medium

You are given a 0-indexed array of integers nums of length n. You are initially positioned at nums[0].

Each element nums[i] represents the maximum length of a forward jump from index i. In other words, if you are at nums[i], you can jump to any nums[i + j] where:

0 <= j <= nums[i] and
i + j < n
Return the minimum number of jumps to reach nums[n - 1]. The test cases are generated such that you can reach nums[n - 1].

 

Example 1:

Input: nums = [2,3,1,1,4]
Output: 2
Explanation: The minimum number of jumps to reach the last index is 2. Jump 1 step from index 0 to 1, then 3 steps to the last index.
Example 2:

Input: nums = [2,3,0,1,4]
Output: 2
 

Constraints:

1 <= nums.length <= 104
0 <= nums[i] <= 1000
It's guaranteed that you can reach nums[n - 1].

"""


"""

Dynamic Programming Approach

1. Subproblems
dp[i] = min jumps to get to the end for prefix ps[:i]
We keep track of the following state
jp[i] = min jumps
maxp = max index to which we can jump in ps[:i]
p = the last index at which maxp was updated

2. Relationships
We are at position i
We take a look at maxp[i - 1]
if maxp[i - 1] >= i then we don't need an extra jump
if maxp[i - 1] < i we need an extra jump and we also need to update p[i] and maxp[i]
for updating p[i] and maxp[i] we iterate from p[i - 1] to i and find the new maxp and the p at which it gets updated


3. Topological Order
Prefixes in the increasing order of i. We solve from i = 1, n - 1

4. Base Case(s)
When len(ps) == 1 we return 0 as we are already at the end
We initialize jp = 1, p = 0, maxp = 0 + ps[0]

5. Original Problem
jp[n - 1]

6. Time
n - 1 = O(n) Subproblems
O(n) time / subproblem (since we scan for all points from p to i it could be O(n) in the worst case)
Therefore O(n^2) total time

"""

def jumps(ps):
    if (n := len(ps)) == 1: return 0
    jp, p, mp = 1, 0, ps[0]
    for i in range(1, n):
        if mp >= i:         continue
        for j in range(p, i):
            if mp < j + ps[j]: p = j; mp = p + ps[p]
        jp += 1
    return jp

class Solution:
    def jump(self, ps: List[int]) -> int:
        return jumps(ps)




























