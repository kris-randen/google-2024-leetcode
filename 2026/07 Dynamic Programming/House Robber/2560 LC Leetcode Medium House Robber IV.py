"""

2560. House Robber IV
Medium

There are several consecutive houses along a street, each of which has some money inside. There is also a robber, who wants to steal money from the homes, but he refuses to steal from adjacent homes.

The capability of the robber is the maximum amount of money he steals from one house of all the houses he robbed.

You are given an integer array nums representing how much money is stashed in each house. More formally, the ith house from the left has nums[i] dollars.

You are also given an integer k, representing the minimum number of houses the robber will steal from. It is always possible to steal at least k houses.

Return the minimum capability of the robber out of all the possible ways to steal at least k houses.



Example 1:

Input: nums = [2,3,5,9], k = 2
Output: 5
Explanation:
There are three ways to rob at least 2 houses:
- Rob the houses at indices 0 and 2. Capability is max(nums[0], nums[2]) = 5.
- Rob the houses at indices 0 and 3. Capability is max(nums[0], nums[3]) = 9.
- Rob the houses at indices 1 and 3. Capability is max(nums[1], nums[3]) = 9.
Therefore, we return min(5, 9, 9) = 5.
Example 2:

Input: nums = [2,7,9,3,1], k = 2
Output: 2
Explanation: There are 7 ways to rob the houses. The way which leads to minimum capability is to rob the house at index 0 and 4. Return max(nums[0], nums[4]) = 2.


Constraints:

1 <= nums.length <= 105
1 <= nums[i] <= 109
1 <= k <= (nums.length + 1)/2

Seen this question in a real interview before?
1/6
Yes
No
Accepted
140,676/217.4K
Acceptance Rate
64.7%

"""

from typing import List


def houses(vals: List[int], ceil: int) -> int:
    n = len(vals)
    valid = [(0 if val > ceil else 1) for val in vals]

    if n == 1:
        return valid[0]

    dp  = [0] * n; dp[0] = valid[0]
    dp[1] = max(valid[0], valid[1])

    for i in range(2, n):
        dp[i] = max(
            valid[i] + dp[i - 2],
            dp[i - 1]
        )

    return dp[n - 1]

def min_cap(vals: List[int], k: int) -> int:
    caps = sorted(list(set(vals)))

    def bisect_cap(lo: int, hi: int) -> int:

        if houses(vals, caps[hi]) < k or lo > hi:
            return -1

        if lo == hi:
            return caps[lo]

        mid = lo + (hi - lo) // 2
        if houses(vals, caps[mid]) < k:
            return bisect_cap(mid + 1, hi)
        else:
            return bisect_cap(lo, mid)

    return bisect_cap(0, len(caps) - 1)


class Solution:
    def minCapability(self, nums: List[int], k: int) -> int:
        return min_cap(nums, k)