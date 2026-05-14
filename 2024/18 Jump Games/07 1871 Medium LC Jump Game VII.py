"""

1871. Jump Game VII
Medium

You are given a 0-indexed binary string s and two integers minJump and maxJump. In the beginning, you are standing at index 0, which is equal to '0'. You can move from index i to index j if the following conditions are fulfilled:

i + minJump <= j <= min(i + maxJump, s.length - 1), and
s[j] == '0'.
Return true if you can reach index s.length - 1 in s, or false otherwise.

 

Example 1:

Input: s = "011010", minJump = 2, maxJump = 3
Output: true
Explanation:
In the first step, move from index 0 to index 3. 
In the second step, move from index 3 to index 5.
Example 2:

Input: s = "01101110", minJump = 2, maxJump = 3
Output: false
 

Constraints:

2 <= s.length <= 105
s[i] is either '0' or '1'.
s[0] == '0'
1 <= minJump <= maxJump < s.length

Performance jumpd:
Time Limit Exceeded


Performance jump:

Runtime 206 ms Beats 49.67%
Memory 19.77 MB Beats 70.46%


"""


"""

Recursion

"""


def jumpd(s, n, lo, hi, ml, mh):
    if not ml and not mh: return False
    if ml <= n - 1 <= mh: return True
    mlz, mhz = None, None
    for i in range(ml + lo, min(mh + hi + 1, n)):
        if s[i] == 0:
            mlz = i; break
    for i in range(min(mh + hi, n - 1), ml + lo - 1, -1):
        if s[i] == 0:
            mhz = i; break
    return jump(s, n, lo, hi, mlz, mhz)


"""

Dynamic Programming + Prefix Sum (Approach)

"""


def jump(s, lo, hi):
    n = len(s); dp = [0] * n; dp[0] = 1; ss = 0
    for i in range(1, n):
        if i > hi:      ss -= dp[i - hi - 1]
        if i >= lo:     ss += dp[i - lo]
        if s[i] == 1:   continue
        if ss > 0:      dp[i] = 1
    return dp[n - 1] == 1
















