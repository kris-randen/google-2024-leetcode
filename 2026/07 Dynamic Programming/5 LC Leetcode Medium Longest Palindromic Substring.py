"""

5. Longest Palindromic Substring
Solved
Medium

Given a string s, return the longest palindromic substring in s.



Example 1:

Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.
Example 2:

Input: s = "cbbd"
Output: "bb"


Constraints:

1 <= s.length <= 1000
s consist of only digits and English letters.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
4,734,168/12.5M
Acceptance Rate
37.8%

"""

def palindromes(s: str) -> str:
    if (n := len(s)) <= 1:
        return s

    dp = [[i == j for j in range(n)] for i in range(n)]


    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = (
                s[i] == s[j] and
                (
                    length == 2 or
                    dp[i + 1][j - 1]
                )
            )

    return dp

def longest(dp):
    n, maxl, l, r = len(dp), 0, 0, 0

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if dp[i][j] and (j - i + 1) > maxl:
                maxl = max(maxl, j - i + 1)
                l, r = i, j

    return l, r

def longest_palindrom(s):
    if (n := len(s)) < 2:
        return s

    best = (0, 0)
    dp = [[i >= j for j in range(n)] for i in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = (
                s[i] == s[j] and
                dp[i + 1][j -1]
            )

            if dp[i][j] and length > best[1] - best[0] + 1:
                best = i, j

    return s[best[0]:best[1] + 1]

def pad(s: str) -> str:
    return "#" + "#".join(s) + "#"

def expand(t: str, c: int) -> tuple[int, int]:
    l = r = c

    while l >= 0 and r < len(t) and t[l] == t[r]:
        l -= 1
        r += 1

    return l + 1, r - 1

def center_longest(s: str) -> str:
    t, best = pad(s), (0, 0)

    for c in range(len(t)):
        l, r = expand(t, c)

        if r - l > best[1] - best[0]:
            best = l, r

    return t[best[0]:best[1] + 1].replace("#", "")

class Solution:
    def longestPalindrome(self, s: str) -> str:
        return center_longest(s)