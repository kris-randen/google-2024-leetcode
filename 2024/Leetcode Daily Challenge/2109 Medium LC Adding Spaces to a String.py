"""

2109. Adding Spaces to a String
Solved
Medium
Topics
Companies
Hint
You are given a 0-indexed string s and a 0-indexed integer array spaces that describes the indices in the original string where spaces will be added. Each space should be inserted before the character at the given index.

For example, given s = "EnjoyYourCoffee" and spaces = [5, 9], we place spaces before 'Y' and 'C', which are at indices 5 and 9 respectively. Thus, we obtain "Enjoy Your Coffee".
Return the modified string after the spaces have been added.



Example 1:

Input: s = "LeetcodeHelpsMeLearn", spaces = [8,13,15]
Output: "Leetcode Helps Me Learn"
Explanation:
The indices 8, 13, and 15 correspond to the underlined characters in "LeetcodeHelpsMeLearn".
We then place spaces before those characters.
Example 2:

Input: s = "icodeinpython", spaces = [1,5,7,9]
Output: "i code in py thon"
Explanation:
The indices 1, 5, 7, and 9 correspond to the underlined characters in "icodeinpython".
We then place spaces before those characters.
Example 3:

Input: s = "spacing", spaces = [0,1,2,3,4,5,6]
Output: " s p a c i n g"
Explanation:
We are also able to place spaces before the first character of the string.


Constraints:

1 <= s.length <= 3 * 105
s consists only of lowercase and uppercase English letters.
1 <= spaces.length <= 3 * 105
0 <= spaces[i] <= s.length - 1
All the values of spaces are strictly increasing.

"""

"""
Recursion

Accepted
Krishnaswami Rajendren
submitted at Dec 03, 2024 10:46

Runtime 175 ms Beats 10.50%
Memory 114.61 MB Beats 5.06%
"""

from collections import deque

def spaces(s, ps):
    def rec(s, ps, sk, rs):
        if not ps: return rs + s[sk:]
        pk = ps.popleft()
        for i in range(sk, pk):
            rs.append(s[i])
        rs.append(' ')
        return rec(s, ps, pk, rs)
    return ''.join(rec(list(s), deque(ps), 0, []))

"""
2-Pointers

Accepted
Krishnaswami Rajendren
submitted at Dec 03, 2024 10:42

Runtime 95 ms Beats 61.81%
Memory 49.09 MB Beats 36.87%
"""

def spaces_2p(s, ps):
    if not ps: return s
    l, r, rs = 0, 0, []
    while r < len(ps):
        while l < ps[r]:
            rs.append(s[l]); l += 1
        rs.append(' '); r += 1
    rs += list(s[l:])
    return ''.join(rs)

