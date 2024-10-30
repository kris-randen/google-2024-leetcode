"""

516. Longest Palindromic Subsequence
Solved
Medium
Topics
Companies
Given a string s, find the longest palindromic subsequence's length in s.

A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.



Example 1:

Input: s = "bbbab"
Output: 4
Explanation: One possible longest palindromic subsequence is "bbbb".
Example 2:

Input: s = "cbbd"
Output: 2
Explanation: One possible longest palindromic subsequence is "bb".


Constraints:

1 <= s.length <= 1000
s consists only of lowercase English letters.

"""

def initialize2D(s):
    n = len(s); dp = [[1 for _ in range(n)] for _ in range(n)]
    for i in range(n - 1):
        if s[i] == s[i + 1]: dp[i][i + 1] = 2
    return dp, n

def isBaseCase(s):
    return len(s) < 3

def baseCase(s):
    if not s: return 0
    return 1 if len(s) == 1 else (2 if s[0] == s[1] else 1)

def longestPalindromicSubseq(s):
    if isBaseCase(s): return baseCase(s)
    dp, n = initialize2D(s)
    for d in range(3, n + 1):
        for i in range(n + 1 - d):
            j = i + d - 1
            if s[i] == s[j]:
                dp[i][j] = 2 + dp[i + 1][j - 1]
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1]


if __name__ == '__main__':
    dp = [1, 2, 3]
    print(dp)