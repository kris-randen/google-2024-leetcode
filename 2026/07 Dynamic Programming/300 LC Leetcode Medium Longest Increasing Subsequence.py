"""

300. Longest Increasing Subsequence
Solved
Medium
Topics
conpanies icon
Companies
Given an integer array nums, return the length of the longest strictly increasing subsequence.



Example 1:

Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.
Example 2:

Input: nums = [0,1,0,3,2,3]
Output: 4
Example 3:

Input: nums = [7,7,7,7,7,7,7]
Output: 1


Constraints:

1 <= nums.length <= 2500
-104 <= nums[i] <= 104


Follow up: Can you come up with an algorithm that runs in O(n log(n)) time complexity?


Seen this question in a real interview before?
1/6
Yes
No
Accepted
2,629,121/4.4M
Acceptance Rate
59.4%

"""

from typing import List

def lis(vs) -> int:
    if (n := len(vs)) == 0:
        return 0

    dp = [1] * n

    for i in reversed(range(n)):
        dp[i] = max((dp[k] for k in reversed(range(i + 1, n)) if vs[k] > vs[i]), default=0) + 1

    return max(dp)

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        return lis(nums)