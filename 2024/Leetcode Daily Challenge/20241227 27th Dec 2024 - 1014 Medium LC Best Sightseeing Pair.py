"""

1014. Best Sightseeing Pair
Medium

You are given an integer array values where values[i] represents the value of the ith sightseeing spot. Two sightseeing spots i and j have a distance j - i between them.

The score of a pair (i < j) of sightseeing spots is values[i] + values[j] + i - j: the sum of the values of the sightseeing spots, minus the distance between them.

Return the maximum score of a pair of sightseeing spots.

 

Example 1:

Input: values = [8,1,5,2,6]
Output: 11
Explanation: i = 0, j = 2, values[i] + values[j] + i - j = 8 + 5 + 0 - 2 = 11
Example 2:

Input: values = [1,2]
Output: 2
 

Constraints:

2 <= values.length <= 5 * 104
1 <= values[i] <= 1000

Performance Brute-force O(n^2) solution
Time Limit Exceeded

Performance for Dynamic Programming O(n) solution
Runtime 59 ms Beats 83.66%
Memory 23.30 MB Beats 10.49%

"""

def pair(ps):
    return max((p + q + i - j) for i, p in enumerate(ps) for j, q in enumerate(qs))


"""

Dynamic Programming Approach:

1. Subproblems: dp[n] = stores the indices of max pair up to i and also the index of the max
ps[j] + j seen so far, let's call this pm

so dp[n] is a tuple
dp = pi, pj, pv, pm

pi, pj are the indices of the best pair.
pv is the pair value of the best pair
pm is the index of the max(ps[i] + i)

2. Relationship:
When we consider the n + 1 th element = dp[n + 1]

Keep in mind that the element with the larger index j what gets added to the value is ps[j] - j

For the n + 1 th element we know we need ps[n] - n is what gets contributed

Now this n + 1 th element either belongs to the new best pair or not.

If it belongs to the new best pair:

Then we know for some 0 <= i < n the new best pair value is ps[i] + i + ps[n] - n

Since we keep track of the index of the max(ps[i] + i) in our dp

in, jn, vn, mn = dp[n]

If ps[mn] + mn + ps[n] - n is >= vn (The previous best pair value then we correct it)
else the old pair remains the best

3. Topological Order

We solve in the order of increasing 2 <= i < n

4. Base Case

For indices 0 and 1 we initialize dp with

dp = 0, 1, ps[0] + 0 + ps[1] - 1, msplt(0, 1)

msplt returns the index of the max(ps[i] + i) element


5. Original Problem

Since there's no need to store all the previous values we just store one tuple in dp and keep updating it. In a way the original problem is dp[n - 1][2] because we need to return the value which is store in the second index of the tuple. But since dp doesn't need explicit indexing we return dp[2].

6. Time:

Clearly there are n = O(n) subproblems and each subproblem takes constant time the total time complexity is O(n)

"""


"""

Brute-force O(n^2) solution = pair

"""

def pair(ps):
    return max((ps[i] + ps[j] + i - j) for i in range(len(ps)) for j in range(i + 1, len(ps)))


"""

Dynamic Programming O(n) solution

"""

def dpair(ps):
    def msplt(i, j):        return i if (ps[i] + i >= ps[j] + j) else j
    def val(l, r):          return ps[l] + l + ps[r] - r

    if (n := len(ps)) == 2: return val(0, 1)

    dp = val(0, 1), msplt(0, 1)

    for i in range(2, n):
        pv, pm = dp
        if (npv := val(pm, i)) >= pv: pv = npv
        dp = pv, msplt(pm, i)

    return dp[0]

class Solution:
    def maxScoreSightseeingPair(self, ps: List[int]) -> int:
        return dpair(ps)

















