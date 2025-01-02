"""

1306. Jump Game III
Medium

Given an array of non-negative integers arr, you are initially positioned at start index of the array. When you are at index i, you can jump to i + arr[i] or i - arr[i], check if you can reach any index with value 0.

Notice that you can not jump outside of the array at any time.

 

Example 1:

Input: arr = [4,2,3,0,3,1,2], start = 5
Output: true
Explanation: 
All possible ways to reach at index 3 with value 0 are: 
index 5 -> index 4 -> index 1 -> index 3 
index 5 -> index 6 -> index 4 -> index 1 -> index 3 
Example 2:

Input: arr = [4,2,3,0,3,1,2], start = 0
Output: true 
Explanation: 
One possible way to reach at index 3 with value 0 is: 
index 0 -> index 4 -> index 1 -> index 3
Example 3:

Input: arr = [3,0,2,1,2], start = 2
Output: false
Explanation: There is no way to reach at index 1 with value 0.
 

Constraints:

1 <= arr.length <= 5 * 104
0 <= arr[i] < arr.length
0 <= start < arr.length

Performance

Runtime 7 ms Beats 97.42%
Memory 28.71 MB Beats 33.25%

"""

"""

Recursive Approach

"""

def reach(ps, i, n):
    if i < 0 or i >= n: return False
    if ps[i] == -1:     return False
    if ps[i] == 0:      return True
    
    s = ps[i]; ps[i] = -1
    return reach(ps, i + s, n) or reach(ps, i - s, n)

class Solution:
    def canReach(self, ps: List[int], s: int) -> bool:
        return reach(ps, s, len(ps))





















