"""

72. Edit Distance
Solved
Medium
Topics
conpanies icon
Companies
Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.

You have the following three operations permitted on a word:

Insert a character
Delete a character
Replace a character


Example 1:

Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation:
horse -> rorse (replace 'h' with 'r')
rorse -> rose (remove 'r')
rose -> ros (remove 'e')
Example 2:

Input: word1 = "intention", word2 = "execution"
Output: 5
Explanation:
intention -> inention (remove 't')
inention -> enention (replace 'i' with 'e')
enention -> exention (replace 'n' with 'x')
exention -> exection (replace 'n' with 'c')
exection -> execution (insert 'u')


Constraints:

0 <= word1.length, word2.length <= 500
word1 and word2 consist of lowercase English letters.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,459,668/2.4M
Acceptance Rate
60.6%

"""


def edit_distance(s: str, t: str) -> int:
    m, n = len(s), len(t)
    dp = [[float('inf') for _ in range(n + 1)]  for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][n] = m - i

    for j in range(n + 1):
        dp[m][j] = n - j

    for i in reversed(range(m + 1)):
        for j in reversed(range(n + 1)):
            dp[i][j] = min(
                dp[i + 1][j + 1] + (0 if s[i] == t[j] else 1),
                dp[i][j + 1] + 1,
                dp[i + 1][j] + 1
            )

    return dp[0][0]



class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        return edit_distance(word1, word2)