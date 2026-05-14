"""

213. House Robber II
Solved
Medium
Topics
Companies
Hint
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have a security system connected, and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.



Example 1:

Input: nums = [2,3,2]
Output: 3
Explanation: You cannot rob house 1 (money = 2) and then rob house 3 (money = 2), because they are adjacent houses.
Example 2:

Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.
Example 3:

Input: nums = [1,2,3]
Output: 3


Constraints:

1 <= nums.length <= 100
0 <= nums[i] <= 1000
Seen this question in a real interview before?
1/5
Yes
No
Accepted
825.4K
Submissions
1.9M
Acceptance Rate
42.4%

Runtime 31 ms Beats 86.43%
Memory 16.56 MB Beats 33.11%

"""

def max_loot(hs):
    if not (n := len(hs)): return 0
    lt = [(hs[i] if i == n - 1 else 0) for i in range(n + 1)]
    for i in reversed(range(n - 1)):
        lt[i] = max(
                    lt[i + 2] + hs[i],
                    lt[i + 1]
                   )
    return lt[0]

def c_max_loot(hs):
    if (n := len(hs)) < 2: return 0 if not n else hs[n - 1]
    return max(max_loot(hs[: n - 1]), max_loot(hs[1:]))
