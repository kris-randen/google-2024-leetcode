"""

5. Longest Palindromic Substring
Solved
Medium
Topics
Companies
Hint
Given a string s, return the longest
palindromic

substring
 in s.

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

"""

def longestPalindromicSubstring(s):
    if len(s) < 2: return s
    n = len(s); dic = dict(); longest = (0,0)
    for i in range(n - 1):
        dic[(i,i)] = 1; dic[(i + 1, i)] = 1
    dic[(n-1, n-1)] = 1
    for d in range(2, n + 1):
        for i in range(n - d + 1):
            if dic[(i + 1, i + d - 2)] and s[i] == s[i + d - 1]:
                dic[(i, i + d - 1)] = 1
                longest = (i, i + d - 1)
            else:
                dic[(i, i + d - 1)] = 0
    return s[longest[0]: longest[1] + 1]

class Solution:
    def longestPalindrome(self, s: str) -> str:
        return longestPalindromicSubstring(s)

if __name__ == '__main__':
    ps = longestPalindromicSubstring("babad")
    print(ps)