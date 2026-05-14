"""

11. Container With Most Water
Solved
Medium

You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

 

Example 1:


Input: height = [1,8,6,2,5,4,8,3,7]
Output: 49
Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.
Example 2:

Input: height = [1,1]
Output: 1
 

Constraints:

n == height.length
2 <= n <= 105
0 <= height[i] <= 104


"""



def area(hs, l, r): return min(hs[l], hs[r]) * (r - l)

def max_water(hs):
    l, r = 0, (n := len(hs)) - 1
    maxw = area(hs, l, r)
    while l < r:
        while hs[l] <= hs[r] and l < n - 1:
            l += 1
            maxw = max(maxw, area(hs, l, r))
        while hs[r] <= hs[l] and r > 0:
            r -= 1
            maxw = max(maxw, area(hs, l, r))
    return maxw

class Solution:
    def maxArea(self, hs: List[int]) -> int:
        return max_water(hs)





































