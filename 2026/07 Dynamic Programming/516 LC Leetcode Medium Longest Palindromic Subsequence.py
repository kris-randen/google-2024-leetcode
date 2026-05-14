"""

516. Longest Palindromic Subsequence
Solved
Medium

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

Seen this question in a real interview before?
1/6
Yes
No
Accepted
765,063/1.2M
Acceptance Rate
65.4%

"""

def longest_palindromic_subsequence(s: str) -> int:
    if (n := len(s)) < 2:
        return n

    dp = \
    [
        [
            int(i == j) for j in range(n)
        ]
        for i in range(n)
    ]
    longest = 0

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = (
                2 + dp[i + 1][j - 1] if s[i] == s[j]
                else
                max(dp[i + 1][j], dp[i][j - 1])
            )
            longest = max(longest, dp[i][j])

    return longest

class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        return longest_palindromic_subsequence(s)