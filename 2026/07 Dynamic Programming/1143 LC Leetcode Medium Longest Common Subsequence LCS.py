"""

1143. Longest Common Subsequence
Solved
Medium
Topics
conpanies icon
Companies
Hint
Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.

For example, "ace" is a subsequence of "abcde".
A common subsequence of two strings is a subsequence that is common to both strings.



Example 1:

Input: text1 = "abcde", text2 = "ace"
Output: 3
Explanation: The longest common subsequence is "ace" and its length is 3.
Example 2:

Input: text1 = "abc", text2 = "abc"
Output: 3
Explanation: The longest common subsequence is "abc" and its length is 3.
Example 3:

Input: text1 = "abc", text2 = "def"
Output: 0
Explanation: There is no such common subsequence, so the result is 0.


Constraints:

1 <= text1.length, text2.length <= 1000
text1 and text2 consist of only lowercase English characters.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,839,824/3.1M
Acceptance Rate
59.1%

"""

def lcs(bs, cs):
    if not bs or not cs:
        return 0

    m, n = len(bs), len(cs)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    for i in reversed(range(m)):
        for j in reversed(range(n)):
            dp[i][j] = (
                dp[i + 1][j + 1] + 1 if bs[i] == cs[j] else
                max(dp[i + 1][j], dp[i][j + 1])
            )

    return dp[0][0]

def lcs_inc(bs, cs):
    if not bs or not cs:
        return 0

    m, n = len(bs), len(cs)
    dp = [[0 for _ in range(n)] for _ in range(m)]

    for i in range(m):
        for j in range(n):
            dp[i][j] = (
                1 + dp[i - 1][j - 1]
                if bs[i] == cs[j] else
                max(dp[i - 1][j], dp[i][j - 1])
            )

    return dp[m - 1][n - 1]

class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        return lcs_inc(text1, text2)
