"""

198. House Robber
Solved
Medium
Topics
conpanies icon
Companies
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.



Example 1:

Input: nums = [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.
Example 2:

Input: nums = [2,7,9,3,1]
Output: 12
Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
Total amount you can rob = 2 + 9 + 1 = 12.


Constraints:

1 <= nums.length <= 100
0 <= nums[i] <= 400

Seen this question in a real interview before?
1/6
Yes
No
Accepted
3,559,391/6.7M
Acceptance Rate
53.2%

"""

from typing import List

def max_loot(vals: List[int]) -> int:
    dp = (n := len(vals)) * [0]
    if n == 1:
        return vals[0]
    dp[0], dp[1] = vals[0], max(vals[0], vals[1])
    for i in range(2, n):
        dp[i] = max(vals[i] + dp[i - 2], dp[i - 1])

    return dp[n - 1]

class Solution:
    def rob(self, nums: List[int]) -> int:
        return max_loot(nums)