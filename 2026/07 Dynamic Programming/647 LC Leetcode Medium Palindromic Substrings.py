"""

647. Palindromic Substrings
Solved
Medium

Given a string s, return the number of palindromic substrings in it.

A string is a palindrome when it reads the same backward as forward.

A substring is a contiguous sequence of characters within the string.



Example 1:

Input: s = "abc"
Output: 3
Explanation: Three palindromic strings: "a", "b", "c".
Example 2:

Input: s = "aaa"
Output: 6
Explanation: Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".


Constraints:

1 <= s.length <= 1000
s consists of lowercase English letters.

Seen this question in a real interview before?
1/6
Yes
No
Accepted
1,183,591/1.6M
Acceptance Rate
72.8%

"""

from typing import List

def palindromes_matrix(s: str) -> List[List[bool]]:
    n = len(s)
    dp = [[i == j for j in range(n)] for i in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = (
                s[i] == s[j] and
                (
                    length == 2 or dp[i + 1][j - 1]
                )
            )

    return dp


def count_from_center(s: str, l: int, r: int) -> tuple[int, int]:
    c = 0
    while l >= 0 and r < len(s) and s[l] == s[r]:
        c += 1
        l -= 1
        r += 1
    return c

def palindromes_center(s: str) -> List[List[bool]]:
    return sum(
        count_from_center(s, center, center) +
        count_from_center(s, center, center + 1)
        for center in range(len(s))
    )

def count(dp: List[List[bool]]) -> int:
    return sum(sum(row) for row in dp)

class Solution:
    def countSubstrings(self, s: str) -> int:
        return count(palindromes_matrix(s))