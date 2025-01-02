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

Performance jumpd

Runtime 47 ms Beats 25.23%
Memory 18.75 MB Beats 13.25%

Performance jump

Runtime 23 ms Beats 58.10%
Memory 18.85 MB Beats 9.18%

"""


def jumpd(ps):
    l = 0; maxp = l + ps[l]
    while l < (n := len(ps)) - 1 and l < maxp:
        l += 1
        maxp = max(maxp, l + ps[l])
    return maxp >= n - 1

def jump(ps):
    m, n = 0, len(ps)
    for i, p in enumerate(ps):
        if i > m:       return False
        m = max(m, i + p)
        if m >= n - 1:  return True

class Solution:
    def canJump(self, ps: List[int]) -> bool:
        return jump(ps)





















