"""

55. Jump Game
Solved
Medium

You are given an integer array nums. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.

Return true if you can reach the last index, or false otherwise.



Example 1:

Input: nums = [2,3,1,1,4]
Output: true
Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.
Example 2:

Input: nums = [3,2,1,0,4]
Output: false
Explanation: You will always arrive at index 3 no matter what. Its maximum jump length is 0, which makes it impossible to reach the last index.


Constraints:

1 <= nums.length <= 104
0 <= nums[i] <= 105

Seen this question in a real interview before?
1/6
Yes
No
Accepted
3,202,683/7.8M
Acceptance Rate
40.9%

"""

from typing import List

def can_jump(jumps: List[int]) -> bool:
    farthest, n = 0, len(jumps)

    for i, jump in enumerate(jumps):
        if i > farthest:
            return False
        farthest = max(farthest, i + jump)
    return True

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        return can_jump(nums)
