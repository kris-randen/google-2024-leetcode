"""

198. House Robber
Solved
Medium
Topics
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
1/5
Yes
No
Accepted
2.4M
Submissions
4.7M
Acceptance Rate
51.4%

Runtime 26 ms Beats 97.27%
Memory 16.56 MB Beats 27.30%

"""

def max_loot(hs):
    if not (n := len(hs)): return 0
    lt = [(hs[i] if i == n - 1 else 0)
          for i in range(n + 1)]
    for i in reversed(range(n - 1)):
        lt[i] = max(
                    lt[i + 2] + hs[i],
                    hs[i + 1]
                   )
    return lt[0]
