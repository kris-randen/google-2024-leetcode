"""

494. Target Sum
Solved
Medium

You are given an integer array nums and an integer target.

You want to build an expression out of nums by adding one of the symbols '+' and '-' before each integer in nums and then concatenate all the integers.

For example, if nums = [2, 1], you can add a '+' before 2 and a '-' before 1 and concatenate them to build the expression "+2-1".
Return the number of different expressions that you can build, which evaluates to target.

 

Example 1:

Input: nums = [1,1,1,1,1], target = 3
Output: 5
Explanation: There are 5 ways to assign symbols to make the sum of nums be target 3.
-1 + 1 + 1 + 1 + 1 = 3
+1 - 1 + 1 + 1 + 1 = 3
+1 + 1 - 1 + 1 + 1 = 3
+1 + 1 + 1 - 1 + 1 = 3
+1 + 1 + 1 + 1 - 1 = 3
Example 2:

Input: nums = [1], target = 1
Output: 1
 

Constraints:

1 <= nums.length <= 20
0 <= nums[i] <= 1000
0 <= sum(nums[i]) <= 1000
-1000 <= target <= 1000


Performance Top Down Recursion waysrec

Time Limit Exceeded

Performance Dynamic Programming waysdp

Runtime 386 ms Beats 5.54%
Memory 20.13 MB Beats 57.73%


Performance of Subset Sum Reduction 2D DP
Runtime 47 ms Beats 89.49%
Memory 18.14 MB Beats 60.69%


Performance of Subset Sum Reduction 1D DP

Runtime 31 ms Beats 91.90%
Memory 17.87 MB Beats 65.50%

"""


def waysrec(vs, t):
    if (n := len(vs)) == 0: return 1 if t == 0 else 0
    v = vs.pop()
    return ways(vs.copy(), t - v) + ways(vs.copy(), t + v)


def waysdp(vs, t):
    n, s = len(vs), sum(vs); lT, hT = t - s, t + s
    dp = [
            {
                td: 0 
                for td in range(lT, hT + 1)
            } 
            for _ in range(n)
         ]

    for td in range(lT, hT + 1):
        dp[0][td] = (2 if td == 0 else 1) \
                    if vs[0] == td or vs[0] == -td \
                    else 0

    for i in range(1, n):
        for td in range(lT + vs[i], hT + 1 - vs[i]):
            dp[i][td] = dp[i - 1][td - vs[i]] + \
                        dp[i - 1][td + vs[i]]

    return dp[n - 1][t]


"""

Chat-GPT's (o1) Insight
Reduce the problem to subset sum

Notice if P = sum of positives and N = sum of negatives

P - N = t and P + N = sum(vs)

Therefore by adding the two equations

2P = t + sum(vs)

Therefore t + sum(vs) has to be even

"""

def subset2d(vs, p):
    if (n := len(vs)) == 0: return 1 if p == 0 else 0
    dp = [[0] * (p + 1) for _ in range(n)]
    dp[0][0] = 2 if vs[0] == 0 else 1
    for q in range(1, p + 1):
        dp[0][q] = 1 if vs[0] == q else 0
    for i in range(1, n):
        for q in range(p + 1):
            dp[i][q] = dp[i - 1][q] + (dp[i - 1][q - vs[i]] if 0 <= q - vs[i] <= p else 0)
    return dp[n - 1][p]


def subset1d(vs, p):
    if (n := len(vs)) == 0: return 1 if p == 0 else 0
    pdp = [0] * (p + 1)
    pdp[0] = 2 if vs[0] == 0 else 1
    for q in range(1, p + 1):
        pdp[q] = 1 if vs[0] == q else 0
    ndp = pdp.copy()
    for i in range(1, n):
        for q in range(p + 1):
            ndp[q] = pdp[q]
            if (r := q - vs[i]) >= 0: ndp[q] += pdp[r]
        pdp = ndp.copy()
    return ndp[p]




class Solution:
    def findTargetSumWays(self, vs: List[int], t: int) -> int:
        if not (P := (t + sum(vs))) % 2 == 0 or P < 0: return 0
        return subset1d(vs, P)





















